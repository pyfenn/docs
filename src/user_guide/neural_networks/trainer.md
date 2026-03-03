# Trainer Class

## Overview

The `Trainer` class is the main component for training deep learning models. It provides a comprehensive interface for managing the training cycle, including checkpointing, early stopping, validation, and prediction.

## Initialization

```python
    Trainer(
        model,
        loss_fn,
        optim,
        epochs,
        num_classes,
        device="cpu",
        checkpoint_dir=None,
        checkpoint_epochs=None,
        checkpoint_name="checkpoint",
        save_best=False,
        early_stopping_patience=None
    )
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `model` | torch.nn.Module | The deep learning model to train | Required |
| `loss_fn` | torch.nn loss | Loss function to use | Required |
| `optim` | torch.optim Optimizer | Optimizer for weight updates | Required |
| `epochs` | int | Number of training epochs | Required |
| `num_classes` | int | Number of classes in the classification problem | Required |
| `device` | str | Device to run training on (cpu, cuda, mps) | "cpu" |
| `checkpoint_dir` | Path or str | Directory to save checkpoints | None |
| `checkpoint_epochs` | int or list | Frequency or list of epochs for checkpoint saving | None |
| `checkpoint_name` | str | Base name for checkpoint files | "checkpoint" |
| `save_best` | bool | If True, saves the best model during training | False |
| `early_stopping_patience` | int | Number of epochs without improvement before stopping training | None |

## Main Features

### 1. Training: `fit()`

Executes the complete training cycle.

```python
def fit(train_loader, val_loader=None, val_epoch: int = 5, start_epoch: int = 0):
    """
    Args:
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data (optional)
        val_epoch: Validation frequency (every N epochs)
        start_epoch: Epoch to resume training from (for checkpoint resumption)

    Returns:
        model: The trained model
    """
```

**Features:**

- Training loop with backward pass and weight updates
- Average loss calculation per epoch
- Periodic validation with metrics (accuracy, precision, recall, F1)
- Automatic checkpointing
- Automatic early stopping

### 2. Prediction: `predict()`

Performs predictions on a dataset.

```python
def predict(data_loader):
    """
    Args:
        data_loader: DataLoader containing data to predict

    Returns:
        predictions: List of predictions
    """
```

**Automatically selects:**
- Binary predictions (sigmoid) for 2 classes
- Multiclass predictions (argmax) for more classes

### 3. Checkpoint Management: `load_checkpoint()`

Loads a saved checkpoint to resume training.

```python
def load_checkpoint(checkpoint_path):
    """
    Args:
        checkpoint_path: Path to the checkpoint file

    Returns:
        epoch: The epoch to resume training from

    Loads:
        - Model weights
        - Optimizer state
        - Best loss up to that point
    """
```

## Advanced Features

### Early Stopping

If `early_stopping_patience` is set, training automatically stops when:
- The validation loss doesn't improve for N consecutive epochs
- Example: `early_stopping_patience=5` stops after 5 epochs without improvement

```python
    trainer = Trainer(
        model=model,
        loss_fn=loss_fn,
        optim=optimizer,
        epochs=100,
        num_classes=2,
        early_stopping_patience=5  # Stops if no improvement for 5 epochs
    )
```

### Checkpointing

The trainer supports two checkpoint strategies:

#### 1. Periodic Checkpointing
Saves every N epochs:

```python
    trainer = Trainer(
        ...,
        checkpoint_dir="checkpoints",
        checkpoint_epochs=10,  # Saves every 10 epochs
        checkpoint_name="my_model"
    )
```

#### 2. Best Model Checkpointing
Saves only the model with the best validation loss:

```python
    trainer = Trainer(
        ...,
        checkpoint_dir="checkpoints",
        save_best=True,
        checkpoint_name="my_model"
    )
```

#### 3. Checkpointing at Specific Epochs
Saves at specific epochs:

```python
    trainer = Trainer(
        ...,
        checkpoint_dir="checkpoints",
        checkpoint_epochs=[10, 25, 50, 75],  # Saves at these epochs
        checkpoint_name="my_model"
    )
```

## Validation Metrics

During validation, the trainer automatically calculates:

- **Loss**: Loss function value
- **Accuracy**: Proportion of correct predictions
- **Precision**: Proportion of correct positive predictions
- **Recall**: Proportion of true positives identified
- **F1 Score**: Harmonic mean between precision and recall

## Complete Usage Example

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from fenn.nn.trainers import Trainer

# Setup
model = MyModel()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Create trainer with all features
trainer = Trainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    epochs=100,
    num_classes=10,
    device="cuda",
    checkpoint_dir="./checkpoints",
    save_best=True,
    early_stopping_patience=10
)

# Training
trained_model = trainer.fit(
    train_loader=train_dataloader,
    val_loader=val_dataloader,
    val_epoch=5  # Validates every 5 epochs
)

# Prediction
predictions = trainer.predict(test_dataloader)

# Resume from checkpoint
start_epoch = trainer.load_checkpoint("./checkpoints/my_model_best.pt")
trainer.fit(
    train_loader=train_dataloader,
    val_loader=val_dataloader,
    start_epoch=start_epoch + 1
)
```

## Internal State

The class maintains the following states during training:

- `_model`: The PyTorch model
- `_device`: Computing device
- `_best_loss`: The best validation loss seen so far
- `_patience_counter`: Counter of epochs without improvement (for early stopping)
- `_logger`: Logger for system messages

## Private Methods

| Method | Description |
|--------|-------------|
| `_should_save_checkpoint(epoch)` | Determines if a checkpoint should be saved at this epoch |
| `_save_checkpoint(epoch, loss, is_best)` | Saves a checkpoint to disk |
| `_binary_predict(data_loader)` | Predictions for binary problems (2 classes) |
| `_multiclass_predict(data_loader)` | Predictions for multiclass problems (>2 classes) |

## Important Notes

1. The model is automatically moved to the specified device during initialization
2. Validation loss is used to determine the best model and for early stopping
3. Checkpoints include both model weights and optimizer state
4. The system logger provides detailed information about checkpointing and early stopping
