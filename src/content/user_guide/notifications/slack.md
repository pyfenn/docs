# Slack Setup

Slack notifications use incoming webhooks to send messages to specific channels.

## Create the Webhook
1. Go to [Slack API: Incoming Webhooks](https://api.api.slack.com/messaging/webhooks).
2. Click **Create your Slack app** -> **From scratch**.
3. Name your app (e.g., "Fenn Notifications") and select your workspace.
4. Go to **Incoming Webhooks** in the sidebar and toggle it **On**.
5. Click **Add New Webhook to Workspace**, select a channel, and click **Allow**.

## Copy the Webhook URL
Copy the URL from the settings page. It will look like:
`https://hooks.slack.com/services/T000/B000/XXXX`

## Environment Configuration
```bash
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```