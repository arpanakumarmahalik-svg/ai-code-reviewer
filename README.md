# 🤖 AI Code Review Bot

An intelligent GitHub bot that automatically reviews Pull Requests using 
LLaMA AI. When a developer opens a PR, the bot instantly analyzes the 
code and posts detailed feedback as a comment.

## ✨ Features

- 🔍 **Automatic PR Detection** — triggers instantly when a PR is opened
- 🧠 **AI-Powered Review** — uses LLaMA 3.3 (via Groq) to analyze code
- 🐛 **Bug Detection** — identifies potential errors and issues
- 📖 **Readability Feedback** — suggests cleaner, more readable code
- ⚡ **Performance Tips** — highlights optimization opportunities
- ✅ **Best Practices** — enforces coding standards
- 🔒 **Security Checks** — flags potential security issues
- ☁️ **24/7 Cloud Deployment** — runs on Render, always active

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| AI Model | LLaMA 3.3 70B via Groq API |
| GitHub Integration | GitHub App + Webhooks |
| Authentication | JWT + RSA Private Key |
| Deployment | Render (Cloud) |

## 🔄 How It Works

Developer opens Pull Request

↓

GitHub fires webhook to FastAPI server

↓

Server verifies webhook signature

↓

Fetches PR code diff via GitHub API

↓

Sends diff to LLaMA AI for review

↓

Posts review comment back on PR ✅

## 📁 Project Structure

ai-code-review-bot/
├── main.py              # FastAPI server + webhook handler
├── github_app.py        # GitHub authentication + API calls
├── claude_review.py     # AI review logic (Groq/LLaMA)
├── github_comments.py   # Post comments to GitHub PR
├── requirements.txt     # Python dependencies
└── .env                 # Secret keys (not uploaded to GitHub)

## 🚀 Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/arpanakumarmahalik-svg/ai-code-review-bot.git
cd ai-code-review-bot
```

### 2. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` File
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_APP_ID=your_app_id
GITHUB_PRIVATE_KEY=your_private_key_content
GROQ_API_KEY=your_groq_api_key

### 4. Run Locally
```bash
uvicorn main:app --reload --port 8000
```

### 5. Deploy to Render
- Push code to GitHub
- Connect repo to Render
- Add environment variables
- Deploy!

## 🔑 Required API Keys

| Key | Where to Get |
|---|---|
| `GITHUB_APP_ID` | GitHub App Settings |
| `GITHUB_PRIVATE_KEY` | GitHub App → Generate Private Key |
| `GITHUB_WEBHOOK_SECRET` | GitHub App → Webhook Settings |
| `GROQ_API_KEY` | https://console.groq.com |

## 📸 Demo

> Bot automatically posts this comment on every Pull Request:

**🤖 AI Code Review by Claude**
- Bugs detected and explained
- Code readability suggestions  
- Performance improvements
- Best practices enforcement
- Security issue detection

## 👩‍💻 Built By

**Arpana Kumar Mahalik**
Diploma in Information Technology
SKDAV Government Polytechnic, Rourkela

[![GitHub](https://img.shields.io/badge/GitHub-arpanakumarmahalik--svg-blue)](https://github.com/arpanakumarmahalik-svg)

