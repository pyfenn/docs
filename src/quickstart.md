# Quickstart

Get your first **fenn** experiment running in under five minutes by following these four steps.

## Installation

Install the framework via pip:

```bash
pip install fenn

```

## Initialize the Project

Fenn includes a CLI to help you jumpstart your project structure. Run this command to download the base template:

```bash
fenn pull base

```

This will generate two essential files:

* `fenn.yaml`: Your default project configuration and hyperparameters.
* `main.py`: A boilerplate entrypoint script.

## Configure Your Environment

Open `fenn.yaml` to define your project settings. Fenn separates system logic (logging) from your experiment logic (`train`).

```yaml
project: my_project

logger:
  dir: logs

train:
  lr: 0.001
```

## Write and Run the Entrypoint

Fenn uses a decorator-based approach. The `@app.entrypoint` function receives an `args` dictionary containing everything defined in your YAML.

### Standard Setup

By default, Fenn looks for a file named `fenn.yaml`.

```python
from fenn import FENN

app = FENN()

@app.entrypoint
def main(args):
    # Access config values via the 'args' object
    print(f"Training {args['project']} with LR: {args['train']['lr']}")

if __name__ == "__main__":
    app.run()

```

### Using Custom Config Files

If you want to use a specific configuration (e.g., for different models or environments), use `set_config_file()` before calling `run()`. This allows you to swap entire experiment setups instantly.

```python
app = FENN()
# Point to a specific config file
app.set_config_file("experiments/cnn_baseline.yaml")

@app.entrypoint
def main(args):
    # This will now use settings from cnn_baseline.yaml
    ...

if __name__ == "__main__":
    app.run()

```

---

## The Fenn Execution Lifecycle

When you execute `app.run()`, Fenn manages the heavy lifting in the background to ensure your experiment is reproducible and organized:

1. **Config Selection**: It identifies the target YAML file (either `fenn.yaml` or the file specified via `set_config_file`).
2. **Environment Setup**: It automatically creates your logging directory and begins capturing all console output to a timestamped file.
3. **Dependency Injection**: It starts your `main()` function, passing the configuration data directly into the `args` parameter.