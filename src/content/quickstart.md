Install the fenn library using

```bash
pip install fenn
```

or 

```bash
uv pip install fenn
```

### Initialize a Project

Run the CLI tool to see which repositories are available and to download a template together with its configuration file. First, list the available repositories:

```bash
fenn list
````

Then, download one of the available templates (here `empty` is just an example):

```bash
fenn pull empty
```

This command downloads the selected template into the current directory and generates the corresponding configuration file, which can be customized before running or extending the project.

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

```python
app = Fenn()
app.set_config_file("my_file.yaml")
```

You can run your code as usual

```bash
python main.py
```

and fenn will take care of the rest for you.

---

## Execution Lifecycle

When you execute `app.run()`, Fenn manages the heavy lifting in the background to ensure your experiment is reproducible and organized:

1. **Config Selection**: It identifies the target YAML file (either `fenn.yaml` or the file specified via `set_config_file`).
2. **Environment Setup**: It automatically creates your logging directory and begins capturing all console output to a timestamped file.
3. **Dependency Injection**: It starts your `main()` function, passing the configuration data directly into the `args` parameter.

---

## Training Models

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