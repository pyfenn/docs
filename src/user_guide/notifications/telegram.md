# Telegram Setup

Telegram requires a `TELEGRAM_BOT_TOKEN` and a `TELEGRAM_CHAT_ID`.

## 1. Get the Bot Token
1. Open Telegram and search for `@BotFather`.
2. Start the chat and send `/newbot`.
3. Follow the prompts to set a display name and username (e.g., `my_test_bot`).
4. Copy the token provided (e.g., `123456:ABC-DEF...`). This is your `YOUR_BOT_TOKEN`.

## 2. Get your Chat ID
1. Start a chat with your new bot and send any message (e.g., "hi").
2. In a browser, open: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. In the JSON response, find the numeric `id` inside the `chat` object.

## Environment Configuration
Add these to your `.env` file:
```bash
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
```