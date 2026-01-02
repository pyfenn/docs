# Basic Usage

Monitoring long-running machine learning experiments is a challenge when you aren't glued to a terminal. **Fenn Notifications** provides a centralized, lightweight solution to bridge the gap between your training scripts and your communication tools. By abstracting various service APIs into a single, unified interface, you can ensure that critical status updates—from successful model checkpoints to unexpected crashes—reach you instantly on your preferred platforms.

The system is built with a "send-and-forget" philosophy. It handles the complexities of environment variables, API requests, and network retries in the background, allowing you to focus entirely on your model development.

### Configure Environment

To begin, install the package and define your credentials in a `.env` file at the root of your project. Each service automatically looks for its specific environment variables, keeping your Python code clean and free of hard-coded secrets.


```bash
DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."
TELEGRAM_BOT_TOKEN="12345:ABC..."
TELEGRAM_CHAT_ID="12345678"

```

### Implementation

The following snippet demonstrates how to initialize the notifier and broadcast a message across multiple platforms simultaneously.

```python
from fenn.notification import Notifier
from fenn.notification.services import Discord, Telegram

# Initialize the dispatcher and register services
notifier = Notifier()
notifier.add_services([Discord, Telegram])

# Broadcast to all registered channels
notifier.notify("Training started: Experiment #42")

```

---

## Core Principles

**Resilient Architecture** The notification system is designed to be fail-safe. If one service encounters a network timeout or credential error, the `Notifier` catches the exception internally, ensuring that the failure of one channel (like Slack) does not prevent the message from reaching others (like Email).

**Developer Friendly** While the system comes with built-in support for the most popular messaging apps, it is highly extensible. By inheriting from the base `Service` class, you can implement custom logic for internal webhooks, logging databases, or proprietary enterprise tools with minimal boilerplate.

**Dynamic Management** You can modify your notification strategy at runtime. The API allows you to add or remove services dynamically based on the severity of the alert—for example, sending routine logs to Discord but escalating critical errors to both SMS and Email.