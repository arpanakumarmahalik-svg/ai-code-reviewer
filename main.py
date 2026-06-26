from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import os
from dotenv import load_dotenv
from github_app import get_installation_token, get_pr_diff
from claude_review import review_code_with_claude
from github_comments import post_pr_comment

load_dotenv()

app = FastAPI()

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")


def verify_signature(payload_body: bytes, signature_header: str):
    """Checks that this request really came from GitHub."""
    if not signature_header:
        raise HTTPException(status_code=403, detail="Missing signature")

    hash_object = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Signature mismatch")


@app.get("/")
def home():
    return {"status": "AI Code Review Bot is running 🤖"}


@app.post("/webhook")
async def github_webhook(request: Request):
    payload_body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256")

    # Step 1: Verify request is from GitHub
    verify_signature(payload_body, signature_header)

    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event")

    # Step 2: Only handle pull request events
    if event_type == "pull_request" and payload.get("action") in ["opened", "synchronize", "reopened"]:
        pr_number = payload["pull_request"]["number"]
        repo_name = payload["repository"]["full_name"]
        installation_id = payload["installation"]["id"]

        print(f"📥 PR #{pr_number} received from {repo_name}")

        # Step 3: Get GitHub access token
        token = await get_installation_token(installation_id)

        # Step 4: Fetch the code diff
        diff = await get_pr_diff(repo_name, pr_number, token)
        print(f"📄 Got diff ({len(diff)} characters)")

        # Step 5: Send diff to Claude for review
        print("🤖 Sending to Claude for review...")
        review = await review_code_with_claude(diff)
        print("✅ Claude review received!")

        # Step 6: Post review as PR comment
        await post_pr_comment(repo_name, pr_number, review, token)

    return {"status": "received"}