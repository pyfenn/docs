# RegressionTrainer

The `RegressionTrainer` is used for regression tasks where the goal is to predict continuous values. It supports choosing between returning the last model or the best model after training.

## Initialization

```python
from fenn.nn.trainers import RegressionTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

trainer = RegressionTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    return_model="last",
    device="cpu",
    early_stopping_patience=None,
    checkpoint_config=None
)
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `model` | torch.nn.Module | The neural network model to train | Required |
| `loss_fn` | torch.nn.Module | Loss function to use | Required |
| `optim` | torch.optim.Optimizer | Optimizer for weight updates | Required |
| `return_model` | str | Return 'last' or 'best' model after training | "last" |
| `device` | str/torch.device | Device to run training on (cpu, cuda, mps) | "cpu" |
| `early_stopping_patience` | int | Epochs without improvement before early stopping | None |
| `checkpoint_config` | Checkpoint | Checkpoint configuration object | None |

### return_model Parameter

- **"last"**: Use the model weights from the final training epoch
- **"best"**: Use the model weights with the best validation loss
  - Requires `val_loader` in `fit()` method
  - Useful for preventing overfitting

## Training

### fit() Method

```python
def fit(
    train_loader: DataLoader,
    epochs: int,
    val_loader: Optional[DataLoader] = None,
    val_epochs: int = 1
) -> None:
    """Train the regression model with optional validation and early stopping."""
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `train_loader` | DataLoader | DataLoader for training data | Required |
| `epochs` | int | Total number of epochs to train for | Required |
| `val_loader` | DataLoader | DataLoader for validation data | None |
| `val_epochs` | int | Evaluate every N epochs | 1 |

### Usage Examples

```python
# Train without validation
trainer.fit(train_loader, epochs=100)

# Train with validation every epoch
trainer.fit(train_loader, epochs=100, val_loader=val_loader)

# Train with validation every 2 epochs
trainer.fit(train_loader, epochs=100, val_loader=val_loader, val_epochs=2)
```

## Prediction

### predict() Method

```python
def predict(
    dataloader_or_batch: Union[DataLoader, torch.Tensor]
) -> List:
    """Predict continuous values for given data."""
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `dataloader_or_batch` | DataLoader/Tensor | Input data | Required |

### Return Values

List of predicted continuous values

### Usage Examples

```python
# Get predictions from DataLoader
predictions = trainer.predict(test_loader)

# Get predictions from batch tensor
batch_tensor = torch.randn(32, 10)
predictions = trainer.predict(batch_tensor)

# Make predictions on single sample
sample = torch.randn(1, 10)
prediction = trainer.predict(sample)[0]
```

## Validation Metrics

During validation, the trainer automatically calculates:

| Metric | Description |
|--------|-------------|
| **Loss** | Regression loss (e.g., MSELoss, MAELoss, etc.) |
| **R² Score** | Coefficient of determination (0-1, higher is better) |

These metrics are printed at each validation epoch and logged for later analysis.

## Training Behavior

### With Validation Loader

When using `return_model="best"`:
- The trainer tracks the model with the lowest validation loss
- This model is restored after training completes
- Useful for preventing overfitting on validation data

```python
trainer = RegressionTrainer(
    ...,
    return_model="best"
)
trainer.fit(train_loader, epochs=100, val_loader=val_loader)
# Model now contains weights from epoch with best validation loss
```

### Without Validation Loader

With `return_model="last"`:
- The trainer uses the final model weights regardless of performance
- Simpler but no overfitting protection

```python
trainer = RegressionTrainer(
    ...,
    return_model="last"
)
trainer.fit(train_loader, epochs=100)
# Model contains weights from final epoch
```

## Complete Examples

### Basic Regression

```python
import torch
from torch import nn
from fenn.nn.trainers import RegressionTrainer

# Setup
model = SimpleRegressor(input_size=10, output_size=1)
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Create trainer
trainer = RegressionTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    return_model="last",
    device="cuda"
)

# Training
trainer.fit(train_loader, epochs=50)

# Prediction
predictions = trainer.predict(test_loader)
```

### Regression with Validation and Checkpointing

```python
import torch
from torch import nn
from fenn.nn.trainers import RegressionTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup
model = RegressionNet(input_size=20, output_size=1)
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Checkpoint configuration
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    epochs=10,  # Save every 10 epochs
)

# Create trainer with best model selection
trainer = RegressionTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    return_model="best",
    device="cuda",
    checkpoint_config=checkpoint_config,
    early_stopping_patience=15
)

# Training with validation
trainer.fit(
    train_loader=train_dataloader,
    epochs=200,
    val_loader=val_dataloader,
    val_epochs=1
)

# Model now contains best weights from validation loss
predictions = trainer.predict(test_dataloader)

# Resume from checkpoint
trainer.load_best_checkpoint()
trainer.fit(
    train_loader=train_dataloader,
    epochs=200,
    val_loader=val_dataloader,
    val_epochs=1
)
```

### Multi-output Regression

```python
import torch
from torch import nn
from fenn.nn.trainers import RegressionTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup - model predicts 3 outputs
model = MultiOutputRegressor(input_size=50, output_size=3)
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Checkpoint configuration
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    save_best=True,
)

# Create trainer
trainer = RegressionTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    return_model="best",
    device="cuda",
    checkpoint_config=checkpoint_config,
    early_stopping_patience=10
)

# Training
trainer.fit(
    train_loader=train_dataloader,
    epochs=100,
    val_loader=val_dataloader,
    val_epochs=1
)

# Predictions will be lists of length 3 (one per output)
predictions = trainer.predict(test_dataloader)
```

## See Also

- [Base Trainer](base_trainer.md): Core trainer functionality
- [Checkpoint Management](checkpoint_management.md): Saving and loading checkpoints
- [Advanced Features](features.md): Early stopping and validation metrics
