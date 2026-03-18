# Email Setup

Resend is used for email notifications. You need an API key and a verified sender.

## 1. Get your API Key
1. Sign up at [resend.com](https://resend.com).
2. Go to [API Keys](https://resend.com/api-keys) and click **Create API Key**.
3. Copy the key (starts with `re_`).

## 2. Verify your Domain (Optional)
* For production: Add your domain in the [Domains](https://resend.com/domains) section.
* For testing: Use `onboarding@resend.dev`.

## Environment Configuration
```bash
RESEND_API_KEY="re_your_api_key_here"
RESEND_FROM_EMAIL="onboarding@resend.dev"
RESEND_TO_EMAILS="recipient1@example.com,recipient2@example.com"
```