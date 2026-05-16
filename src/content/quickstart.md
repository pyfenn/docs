# Quickstart

Install the fenn library using

```bash
pip install fenn
```

or 

```bash
uv pip install fenn
```

### Initialize a Project

Use the CLI to discover and download a project template.

#### 1. List available templates

```bash
fenn list
```

This fetches the directory listing from [`pyfenn/templates`](https://github.com/pyfenn/templates) and prints the templates you can use.

#### 2. Pull a template

```bash
fenn pull <template> [path]
```

Examples:

```bash
fenn pull empty            # pull into the current directory
fenn pull empty ./my-proj  # pull into ./my-proj (created if missing)
```

Each template ships at least a `main.py` entrypoint and a `fenn.yaml` configuration file in the target directory. Most templates also include a `README.md`, a `requirements.txt`, and a `modules/` directory with example model and dataset code.

To avoid clobbering work, `fenn pull` refuses to write into a non-empty target directory. Pass `--force` to overwrite existing files:

```bash
fenn pull empty --force
```

Hidden entries (those starting with `.`, such as `.git`) do not count as "non-empty".

#### 3. Customize and run

Open the generated `fenn.yaml` and adjust hyperparameters, paths, logging, and integrations for your project (see [Configuration](#configuration) below). Then run the entrypoint:

```bash
python main.py
```

#### Common issues

- **`Template <name> not found`** — The template name doesn't match a directory in [`pyfenn/templates`](https://github.com/pyfenn/templates). Run `fenn list` to see valid names.
- **`Refusing to pull into non-empty directory`** — Either pull into an empty directory, point `path` at a fresh one, or pass `--force` to overwrite.
- **`Network error` / `Failed to check template existence`** — Check connectivity. The CLI uses the unauthenticated GitHub API to look up and download templates, which is subject to GitHub's rate limit.

### Configuration

fenn relies on a simple YAML structure to define hyperparameters, paths, logging options, and integrations. You can configure the ``fenn.yaml`` file with the hyperparameters and options for your project.

The structure of the ``fenn.yaml`` file is:

```yaml
# ---------------------------------------
# Fenn Configuration (Modify Carefully)
# ---------------------------------------

project: empty

# ---------------------------
# Logging & Tracking
# ---------------------------

logger:
  dir: logger

export:
  dir: exports

# ---------------------------------------
# Example of User Section
# ---------------------------------------

train:
    lr: 0.001
```

### Write Your Code

Use the `@app.entrypoint` decorator. Your configuration variables are automatically passed via `args`.

```python
from fenn import Fenn

app = Fenn()

@app.entrypoint
def main(args):
    # 'args' contains your fenn.yaml configurations
    print(f"Training with learning rate: {args['train']['lr']}")

    # Your logic here...

if __name__ == "__main__":
    app.run()
```

By default, fenn will look for a configuration file named `fenn.yaml` in the current directory. If you would like to use a different name, a different location, or have multiple configuration files for different configurations, you can call `set_config_file()` and update the path or the name of your configuration file. You must assign the filename before calling `run()`.

The optional `export.dir` setting centralizes where artifacts are written. Components that export files can use this shared directory instead of requiring an output path to be passed through every call.

```python
app = Fenn()
app.set_config_file("my_file.yaml")
```

### Run It

You can run your code as usual

```bash
python main.py
```

and fenn will take care of the rest for you.

### Training Models

Use built-in trainers to handle your training loops with minimal boilerplate.

```python
import torch.nn as nn
import torch.optim as optim

from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint

@app.entrypoint
def main(args):
        
    # Define your data
    train_loader = DataLoader(train_dataset, batch_size=args["train"]["batch"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args["test"]["batch"], shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=args["test"]["batch"], shuffle=False)
    
    # Define your model
    model = nn.Sequential( ... )     
    loss = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(),
                            lr=float(args["train"]["lr"]))

    # Initialize a ClassificationTrainer
    trainer = ClassificationTrainer(
        model=model,
        loss_fn=loss,
        optim=optimizer,
        num_classes=4
    )

    # Train and predict your model
    trainer.fit(train_loader, epochs=10, val_loader=val_loader)
    preds = trainer.predict(test_loader)
```