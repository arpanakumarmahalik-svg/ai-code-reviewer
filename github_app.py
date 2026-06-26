import jwt
import time
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = "private-key.pem"


def generate_jwt():
    """Creates a signed 'ID card' proving this request comes from our app."""
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        "iat": now - 60,          # issued 60 sec ago (avoids clock issues)
        "exp": now + (10 * 60),   # valid for 10 minutes
        "iss": APP_ID             # your App's ID
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


async def get_installation_token(installation_id: int):
    """Exchanges the JWT for a real access token GitHub will accept."""
    jwt_token = generate_jwt()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        response.raise_for_status()
        return response.json()["token"]


async def get_pr_diff(repo_full_name: str, pr_number: int, installation_token: str):
    """Fetches the actual code changes (the diff) from a Pull Request."""
    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.text   # raw diff text — the actual code changes