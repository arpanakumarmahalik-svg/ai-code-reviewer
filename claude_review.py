from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file!")

client = Groq(api_key=GROQ_API_KEY)

async def review_code_with_claude(diff: str) -> str:
    """Sends the PR code diff to Groq LLaMA and returns a review."""

    prompt = f"""You are an expert code reviewer. Review the following code changes (git diff format).

Provide feedback on:
1. 🐛 Bugs or errors
2. 📖 Code readability
3. ⚡ Performance improvements
4. ✅ Best practices
5. 🔒 Security issues (if any)

Be specific and helpful. For each issue, explain WHY it is a problem and HOW to fix it.
At the end, give an overall summary.

Here are the code changes:

{diff}

Provide your review in a clear, friendly format."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content