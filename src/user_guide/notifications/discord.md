# Discord Setup

To enable Discord notifications, you need a Webhook URL.

## Create the Webhook
1. Open Discord and go to the server where you want to receive messages.
2. Click the server name (top-left) and choose **Server Settings**.
3. In the left sidebar, go to **Integrations** and **Webhooks**.
4. Click **New Webhook / Create Webhook**.

## Copy the Webhook URL
1. In the same Webhook screen, click **Copy Webhook URL**.
2. The copied string will look like:
   `https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXXXXXXXXXX`

## Environment Configuration
Add this key to your `.env` file:
```bash
DISCORD_WEBHOOK="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```