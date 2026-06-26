import httpx


async def post_pr_comment(
    repo_full_name: str,
    pr_number: int,
    comment: str,
    installation_token: str
):
    """Posts Claude's review as a comment on the Pull Request."""

    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"

    body = {
        "body": f"## 🤖 AI Code Review by Claude\n\n{comment}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()
        print(f"✅ Review posted on PR #{pr_number}")
        return response.json()