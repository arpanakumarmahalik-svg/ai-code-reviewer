import jwt
import time
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("GITHUB_APP_ID")


def generate_jwt():
    """Creates a signed JWT using private key from environment variable."""
    private_key = os.getenv("GITHUB_PRIVATE_KEY")

    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),
        "iss": APP_ID
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


async def get_installation_token(installation_id: int):
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
    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.text