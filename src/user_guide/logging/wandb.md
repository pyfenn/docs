
# Weights & Biases

FENN provides native integration with [Weights & Biases (W&B)](https://wandb.ai) for comprehensive experiment monitoring. This integration automatically tracks metrics, hyperparameters, system stats, and model artifacts without requiring boilerplate code in your training scripts.

## Prerequisites

To enable tracking, you must first authenticate the client:

1.  Log in to your [W&B account](https://wandb.ai).
2.  Navigate to **User Settings > API Keys**.
3.  Copy your personal API key.

## Configuration

Enable the W&B integration by configuring your environment credentials and project settings.

### Credentials (`.env`)
Store your API key securely in the `.env` file at the project root. FENN detects this variable automatically to authenticate the session.

```ini
WANDB_API_KEY=your_api_key_here
```

### Project Settings (`fenn.yaml`)
Add a `wandb` block to your `fenn.yaml` configuration. The presence of this section signals FENN to initialize the logger.

```yaml
wandb:
  entity: your_wandb_username_or_team
```

## Execution

Once configured, FENN manages the W&B lifecycle internally. When you execute your standard entry point:

```bash
python main.py
```

The framework automatically performs the following:
-   **Authentication:** Loads the API key from the environment.
-   **Initialization:** Calls `wandb.init` with the settings defined in `fenn.yaml`.
-   **Config Sync:** Uploads the full experiment configuration (hyperparameters, architecture settings) to the W&B dashboard.
-   **Metric Streaming:** Begins streaming loss curves, accuracy metrics, and logs in real-time.