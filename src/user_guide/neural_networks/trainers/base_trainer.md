# Base Trainer Class

The abstract `Trainer` base class provides the core functionality for all trainers in FENN. It is not meant to be used directly—instead, use one of the specialized trainer classes:

- [ClassificationTrainer](classification_trainer.md)
- [RegressionTrainer](regression_trainer.md)
- [LoRATrainer](lora_trainer.md)

## Overview

The base `Trainer` class handles:
- Device management and model setup
- Checkpoint configuration and loading
- Early stopping logic
- Training state management
- Model summary logging

## Core Methods

### fit()

Executes the complete training cycle. Implemented by concrete trainer classes.

```python
def fit(
    train_loader: DataLoader,
    epochs: int,
    val_loader: Optional[DataLoader] = None,
    val_epochs: int = 1
) -> None:
    """Train the model with optional validation and early stopping.
    
    Args:
        train_loader: DataLoader for training data
        epochs: Total number of epochs to train for
        val_loader: DataLoader for validation data (optional)
        val_epochs: How often to evaluate on validation set (in epochs)
    """
```

### predict()

Performs inference on a dataset or batch. Implemented by concrete trainer classes.

```python
def predict(dataloader_or_batch: Union[DataLoader, torch.Tensor]):
    """Predicts the output of the model for a given dataloader or batch.
    
    Args:
        dataloader_or_batch: A DataLoader or a torch tensor.
    
    Returns:
        list: A list of predictions.
    """
```

## Life Cycle

1. **Initialization**: Model is moved to device, checkpoint config is setup, early stopping is configured
2. **Training**: `fit()` trains the model for specified epochs
3. **Checkpointing**: Checkpoints are saved according to configuration
4. **Prediction**: `predict()` can be called on trained models
5. **Resuming**: Use `load_checkpoint()` methods to resume from saved states

## Internal State Management

The trainer maintains a `TrainingState` object that tracks:

- Current epoch
- Training loss per epoch
- Validation loss per epoch
- Model and optimizer states
- Best validation parameters
- Metrics (accuracy, F1, etc.)

This state is automatically saved to checkpoints and restored when loading.

## Checkpoint Methods

All trainers inherit checkpoint management methods:

```python
def load_checkpoint(checkpoint_path: Union[str, Path]):
    """Load a checkpoint from a given path."""
    
def load_checkpoint_at_epoch(epoch: int):
    """Load the checkpoint at the given epoch."""
    
def load_best_checkpoint():
    """Load the best checkpoint."""
```

See [Checkpoint Management](checkpoint_management.md) for detailed usage.

## Device Management

```python
# Model is automatically moved to device during initialization
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    device="cuda"  # or "cpu", "mps"
)
```

The trainer automatically:
- Moves the model to the specified device
- Moves batches to the device during training
- Handles variable batch shapes

## Early Stopping

Configure early stopping via `early_stopping_patience`:

```python
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    early_stopping_patience=5  # Stop after 5 epochs without improvement
)
```

See [Advanced Features](features.md) for detailed early stopping behavior.
