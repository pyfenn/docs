# Advanced Features

This page covers advanced trainer features available across all trainer types.

## Table of Contents

- [Early Stopping](#early-stopping)
- [Training State Management](#training-state-management)
- [Progress Tracking](#progress-tracking)
- [Validation Metrics](#validation-metrics)

## Early Stopping

Early stopping automatically terminates training when the model stops improving. This prevents overfitting and saves computational resources.

### Configuration

Set `early_stopping_patience` when creating a trainer:

```python
from fenn.nn.trainers import ClassificationTrainer

trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    early_stopping_patience=5  # Stop after 5 epochs without improvement
)
```

### How It Works

The trainer maintains a patience counter:
- Counter increments by 1 each epoch without improvement
- Counter resets to 0 when loss improves
- Training stops when counter reaches `early_stopping_patience`

```
Epoch 1: Loss = 0.500 → Best loss = 0.500, Patience = 0
Epoch 2: Loss = 0.480 → Best loss = 0.480, Patience = 0
Epoch 3: Loss = 0.485 → No improvement, Patience = 1
Epoch 4: Loss = 0.490 → No improvement, Patience = 2
Epoch 5: Loss = 0.475 → Best loss = 0.475, Patience = 0
Epoch 6: Loss = 0.478 → No improvement, Patience = 1
...
Epoch 10: Loss = 0.476 → No improvement, Patience = 5 → STOP
```

### Behavior Modes

The early stopping behavior depends on whether you provide a validation loader:

#### Mode 1: No Validation Loader

Monitors **training loss**:

```python
trainer = ClassificationTrainer(
    ...,
    early_stopping_patience=5
)
trainer.fit(train_loader, epochs=100)
```

**When to use:**
- Validation data unavailable
- Quick experiments
- **Note:** Less reliable than validation-based stopping

#### Mode 2: With Validation Loader

Monitors **validation loss**:

```python
trainer = ClassificationTrainer(
    ...,
    early_stopping_patience=5
)
trainer.fit(train_loader, epochs=100, val_loader=val_loader)
```

**When to use:**
- You have validation data (recommended)
- Preventing overfitting is a priority
- **Note:** Most reliable approach

### Examples

#### Basic Early Stopping

```python
from fenn.nn.trainers import ClassificationTrainer

trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    early_stopping_patience=10
)

trainer.fit(
    train_loader=train_loader,
    epochs=200,  # May terminate early
    val_loader=val_loader
)
```

#### With Best Model Saving

```python
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    save_best=True,
)

trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    early_stopping_patience=10,
    checkpoint_config=checkpoint_config
)

trainer.fit(
    train_loader=train_loader,
    epochs=200,
    val_loader=val_loader
)

# Model automatically contains best weights
# Checkpoint also saved as checkpoint_best.pt
```

#### Aggressive vs. Patient Early Stopping

```python
# Aggressive: Stop quickly if not improving
aggressive_trainer = ClassificationTrainer(
    ...,
    early_stopping_patience=3  # Stop after 3 epochs
)

# Patient: Give model more time to improve
patient_trainer = ClassificationTrainer(
    ...,
    early_stopping_patience=20  # Stop after 20 epochs
)
```

### Tips

- **Start with 5-10 epochs**: Good default for most problems
- **Increase for noisy validation**: If validation loss is volatile, use higher patience
- **Decrease for clear improvement**: If validation quickly plateaus, use lower patience
- **Always use validation data**: Early stopping based on validation is more reliable

## Training State Management

The trainer automatically manages training state through a `TrainingState` object.

### What Gets Tracked

The `TrainingState` object tracks:

```python
TrainingState(
    epoch=10,                          # Current epoch
    train_loss=0.245,                  # Training loss
    val_loss=0.312,                    # Validation loss (if applicable)
    best_train_loss=0.240,             # Best training loss
    best_val_loss=0.305,               # Best validation loss
    best_epoch=8,                      # Epoch with best validation loss
    patience_counter=2,                # Epochs without improvement
    model_state_dict={...},            # Model weights
    optimizer_state_dict={...},        # Optimizer state
    acc=0.94,                          # Accuracy (classification)
    best_acc=0.95,                     # Best accuracy
    # ... other metrics
)
```

### Accessing Training State

Training state is automatically saved to checkpoints. To access it:

```python
# After training
trainer.fit(train_loader, epochs=100)

# State is in trainer._state
print(f"Final epoch: {trainer._state.epoch}")
print(f"Best validation loss: {trainer._state.best_val_loss}")
print(f"Best accuracy: {trainer._state.best_acc}")
```

### State Restoration

When loading checkpoints, state is automatically restored:

```python
trainer.load_checkpoint_at_epoch(50)
# Trainer state now matches epoch 50

print(f"Current epoch: {trainer._state.epoch}")  # 50
print(f"Current loss: {trainer._state.val_loss}")  # Loss at epoch 50
```

## Progress Tracking

Training progress is displayed using a rich progress bar:

```
Epoch 45/100 [████████████░░░░░░] 45% | Train Mean Loss: 0.3245
Epoch 45/100 [████████████░░░░░░] 45% | Train Loss: 0.3245 | Val Loss: 0.3512 | Val Acc: 0.9421
```

### Information Displayed

- **Epoch counter**: Current epoch / total epochs
- **Progress bar**: Visual representation of training progress
- **Time elapsed**: Time spent training so far
- **Training loss**: Average loss on training set
- **Validation loss**: Loss on validation set (if applicable)
- **Validation accuracy**: Accuracy on validation set (for classification)

## Validation Metrics

Different trainers calculate different validation metrics.

### ClassificationTrainer Metrics

During validation, calculates:

| Metric | Description | Range |
|--------|-------------|-------|
| **Loss** | Classification loss function value | 0-∞ |
| **Accuracy** | % of correct predictions | 0-1 |
| **Precision** | % of correct positive predictions | 0-1 |
| **Recall** | % of true positives found | 0-1 |
| **F1 Score** | Harmonic mean of precision & recall | 0-1 |

**Example output:**
```
Epoch 10/100 - Train Loss: 0.3245 | Val Loss: 0.3102 | Val Acc: 0.9512
```

### RegressionTrainer Metrics

During validation, calculates:

| Metric | Description | Range |
|--------|-------------|-------|
| **Loss** | Regression loss function value | 0-∞ |
| **R² Score** | Coefficient of determination | -∞ to 1 |

**Example output:**
```
Epoch 10/100 - Train Loss: 0.0245 | Val Loss: 0.0312 | R² Score: 0.8945
```

### Understanding Metrics

#### Accuracy
- **What it means**: Proportion of correct predictions
- **When it matters**: Good overall metric for balanced datasets
- **Limitation**: Can be misleading with imbalanced data

#### Precision
- **What it means**: Of all positive predictions, how many were correct?
- **Formula**: `TP / (TP + FP)`
- **Use when**: False positives are costly (e.g., cancer diagnosis)

#### Recall
- **What it means**: Of all true positives, how many did we find?
- **Formula**: `TP / (TP + FN)`
- **Use when**: False negatives are costly (e.g., disease detection)

#### F1 Score
- **What it means**: Balanced harmonic mean of precision and recall
- **Formula**: `2 * (precision * recall) / (precision + recall)`
- **Use when**: You want to balance precision and recall

#### R² Score
- **What it means**: Proportion of variance explained by model
- **Range**: -∞ to 1 (1 is perfect, 0 is baseline, <0 is worse than baseline)
- **Use when**: Evaluating regression models

## Complete Example: Early Stopping with All Features

```python
import torch
from torch import nn
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup
model = ResNet50(num_classes=10)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Checkpoint configuration with best model saving
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    save_best=True,
)

# Create trainer with early stopping
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    device="cuda",
    checkpoint_config=checkpoint_config,
    early_stopping_patience=10  # Stop after 10 epochs without improvement
)

# Train with validation every epoch
trainer.fit(
    train_loader=train_dataloader,
    epochs=200,  # May stop early
    val_loader=val_dataloader,
    val_epochs=1
)

# Access final state
print(f"Stopped at epoch: {trainer._state.epoch}")
print(f"Best validation loss: {trainer._state.best_val_loss:.4f}")
print(f"Best accuracy: {trainer._state.best_acc:.4f}")

# Get predictions (using best model)
predictions = trainer.predict(test_dataloader)
```

## See Also

- [Base Trainer](base_trainer.md): Core trainer functionality
- [ClassificationTrainer](classification_trainer.md): Classification training
- [RegressionTrainer](regression_trainer.md): Regression training
- [Checkpoint Management](checkpoint_management.md): Saving and loading states
