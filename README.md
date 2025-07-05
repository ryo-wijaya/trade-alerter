# trade-alerter

A lightweight Python service that receives webhook alerts from external platforms, e.g. TradingView, and forwards them to you via a Telegram bot.

You may host it on cloud e.g. Azure App Service or Google Cloud Run. Its Dockerized, so just build the image, publish it to the cloud container registry, and deploy from there.

### Setup

#### Pre-requisites

1. Ensure that you have a paid version of TradingView that supports webhooks. You may replace TradingView with another price alert service that can call webhooks.
2. For best results, ensure that you are subscribed to some form of real-time market data.
3. Setup a telegram bot via BotFather. Retrieve the bot token, start a chat, and retrieve the chat id.

#### Local Application Setup

Requirements: Python 3.9 or later, pip, venv, and OpenSSL (optional)

1. Clone repository

```bash
git clone https://github.com/ryo-wijaya/trade-alerter
cd trade-alerter
```

2. Create and activate virtual environment

```bash
python -m venv env
.\env\Scripts\activate (windows) or source ./env/bin/activate (Linux/Mac)
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Define or export environment variables

```bash
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
WEBHOOK_SECRET=your-secure-webhook-secret
TIMEZONE=Asia/Singapore
CORS_WHITELIST=<comma-separated-list-of-ips>
```

IMPORTANT:

- If no timezone is specified, it defaults to UTC.
- If no CORS whitelist is specified, the server defaults to allowing all origins.

#### Run application

With uvicorn

```bash
uvicorn main:app --reload --port 8080
```

With docker

```bash
docker build -t trade-alerter .
docker run -p 8080:8080 trade-alerter
```

With docker-compose

```bash
docker-compose up --build
```

#### Usage

1. Generate a webhook secret to act as an API key

```bash
  openssl rand -hex 32 (this generates a 32 byte hexadecimal string)
```

2. Host the application somewhere (preferably on cloud)

3. In TradingView (or any other alternative), create a price alert for a stock you own.

For a buy alert, set up a webhook call to:

`https://<hostname>/webhook/buy-signal/<ticker>/` with payload:
`json
      {
        "webhook_secret": "<your-webhook-secret>",
        "current_price": "<shorthand-for-price>",
        "note": "<your-note-if-any>"
      }
    `
For a sell alert, send to `https://<hostname>/webhook/buy-signal/<ticker>/` with the same payload.
