# Checkpoint Management

Checkpoints allow you to save and resume training. FENN provides a unified checkpoint system across all trainers using the `Checkpoint` configuration object.

## Overview

Checkpointing saves:
- Model weights
- Optimizer state
- Training state (epoch, losses, metrics)
- Best model information

This allows you to:
- Resume training from a saved point
- Save the best model during training
- Recover from interruptions
- Compare models from different epochs

## Creating a Checkpoint Configuration

The `Checkpoint` class defines how checkpoints are managed:

```python
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Periodic checkpointing (every N epochs)
checkpoint_config = Checkpoint(
    directory=Path("checkpoints"),
    epochs=10,  # Save every 10 epochs
)

# Save at specific epochs
checkpoint_config = Checkpoint(
    directory=Path("checkpoints"),
    epochs=[10, 25, 50, 75],
)

# Always save best model
checkpoint_config = Checkpoint(
    directory=Path("checkpoints"),
    save_best=True,
)

# Combined: save every 10 epochs AND best model
checkpoint_config = Checkpoint(
    directory=Path("checkpoints"),
    epochs=10,
    save_best=True,
)
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `directory` | Path/str | Directory to save checkpoints | Required |
| `epochs` | int/list | Checkpoint saving strategy | Required |
| `save_best` | bool | Save best model (lowest validation loss) | False |

### epochs Parameter

- **int (N)**: Save every N epochs
- **list**: Save at specific epoch numbers (e.g., `[10, 25, 50, 75]`)
- **Single value**: Combined with `save_best` to enable both strategies

## Using Checkpoint Configuration

Pass the checkpoint config when creating a trainer:

```python
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    epochs=10,
    save_best=True,
)

trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    checkpoint_config=checkpoint_config
)

trainer.fit(train_loader, epochs=100, val_loader=val_loader)
```

## Loading Checkpoints

### 1. Load a Specific Checkpoint Path

```python
trainer.load_checkpoint("checkpoints/checkpoint_epoch_50.pt")
# Trainer now contains state from epoch 50
trainer.fit(train_loader, epochs=100, val_loader=val_loader)
```

### 2. Load Checkpoint at Specific Epoch

```python
trainer.load_checkpoint_at_epoch(50)
# Resume training from epoch 50
trainer.fit(train_loader, epochs=100, val_loader=val_loader)
```

### 3. Load Best Checkpoint

```python
trainer.load_best_checkpoint()
# Resume training from best model (lowest validation loss)
trainer.fit(train_loader, epochs=100, val_loader=val_loader)
```

## Checkpoint File Format

Checkpoints are saved as `.pt` files containing:

- **model_state_dict**: Model weights
- **optimizer_state_dict**: Optimizer state
- **epoch**: Current epoch
- **train_loss**: Training loss at this epoch
- **val_loss**: Validation loss (if applicable)
- **best_val_loss**: Best validation loss so far
- **metrics**: Accuracy, precision, recall, F1, R², etc.

## Strategies

### Strategy 1: Periodic Checkpointing

Save checkpoints at regular intervals:

```python
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    epochs=10,  # Save every 10 epochs
)

trainer = ClassificationTrainer(
    ...,
    checkpoint_config=checkpoint_config
)

trainer.fit(train_loader, epochs=100)
# Creates: checkpoint_epoch_10.pt, checkpoint_epoch_20.pt, ..., checkpoint_epoch_100.pt
```

**Use when:**
- You want to compare models at different training stages
- Training is stable but you want recovery points

### Strategy 2: Best Model Checkpointing

Only save the best model based on validation loss:

```python
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    save_best=True,
)

trainer = ClassificationTrainer(
    ...,
    checkpoint_config=checkpoint_config
)

trainer.fit(train_loader, epochs=100, val_loader=val_loader)
# Creates: checkpoint_best.pt
```

**Use when:**
- You only care about the best performing model
- Storage is limited
- Validation loss is your primary metric

### Strategy 3: Specific Epochs

Save checkpoints at manually chosen epochs:

```python
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    epochs=[10, 25, 50, 75],
)

trainer = ClassificationTrainer(
    ...,
    checkpoint_config=checkpoint_config
)

trainer.fit(train_loader, epochs=100)
# Creates: checkpoint_epoch_10.pt, checkpoint_epoch_25.pt, etc.
```

**Use when:**
- You want to compare specific training milestones
- You're experimenting with different epoch counts

### Strategy 4: Combined Approach

Save both periodically and the best:

```python
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    epochs=20,
    save_best=True,
)

trainer = ClassificationTrainer(
    ...,
    checkpoint_config=checkpoint_config
)

trainer.fit(train_loader, epochs=100, val_loader=val_loader)
# Creates: checkpoint_epoch_20.pt, checkpoint_epoch_40.pt, ..., checkpoint_best.pt
```

**Use when:**
- You want both recovery points and the best model
- Storage allows for multiple checkpoints

## Complete Examples

### Training with Checkpointing

```python
import torch
from torch import nn
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup
model = MyClassifier()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

# Create checkpoint config
checkpoint_config = Checkpoint(
    directory=Path("./experiment_1/checkpoints"),
    epochs=5,
    save_best=True,
)

# Create trainer
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    checkpoint_config=checkpoint_config,
    early_stopping_patience=10
)

# Train
trainer.fit(
    train_loader=train_dataloader,
    epochs=100,
    val_loader=val_dataloader,
    val_epochs=1
)

# Resume from best checkpoint
trainer.load_best_checkpoint()
print("Resuming from best checkpoint...")

trainer.fit(
    train_loader=train_dataloader,
    epochs=100,
    val_loader=val_dataloader,
    val_epochs=1
)
```

### Evaluating Different Checkpoints

```python
import torch
from pathlib import Path
from fenn.nn.trainers import ClassificationTrainer

# Load different checkpoints and evaluate
checkpoints = [
    "checkpoints/checkpoint_epoch_10.pt",
    "checkpoints/checkpoint_epoch_20.pt",
    "checkpoints/checkpoint_best.pt"
]

for ckpt in checkpoints:
    trainer = ClassificationTrainer(...)
    trainer.load_checkpoint(ckpt)
    
    predictions = trainer.predict(test_loader)
    accuracy = compute_accuracy(predictions, test_labels)
    print(f"{ckpt}: {accuracy:.4f}")
```

### Multi-Stage Training

```python
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Stage 1: Coarse training
checkpoint_config = Checkpoint(
    directory=Path("./stage1/checkpoints"),
    save_best=True,
)

trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
    checkpoint_config=checkpoint_config
)

trainer.fit(train_loader, epochs=50, val_loader=val_loader)

# Stage 2: Fine-tuning with best model from stage 1
trainer.load_best_checkpoint()

# Reduce learning rate for fine-tuning
for param_group in trainer._optimizer.param_groups:
    param_group['lr'] = 1e-5

checkpoint_config = Checkpoint(
    directory=Path("./stage2/checkpoints"),
    save_best=True,
)
trainer._checkpoint = checkpoint_config

trainer.fit(train_loader, epochs=50, val_loader=val_loader)
```

## Tips & Best Practices

1. **Always use validation**: Checkpointing is most useful with validation data
2. **Monitor checkpoint size**: Large models create large checkpoints
3. **Use best model checkpointing**: Prevents accidental overfitting
4. **Organize checkpoints**: Use descriptive directory names
5. **Backup important experiments**: Copy final checkpoints to safe location

## Working with Different Devices

```python
# Save on GPU, load on CPU
trainer_gpu = ClassificationTrainer(..., device="cuda")
trainer_gpu.fit(train_loader, epochs=10)
trainer_gpu.load_best_checkpoint()  # Saved on GPU

# Load and evaluate on CPU
trainer_cpu = ClassificationTrainer(..., device="cpu")
trainer_cpu.load_checkpoint("checkpoints/checkpoint_best.pt")
predictions = trainer_cpu.predict(test_loader)
```

## See Also

- [Base Trainer](base_trainer.md): Core trainer functionality
- [ClassificationTrainer](classification_trainer.md): Classification-specific training
- [RegressionTrainer](regression_trainer.md): Regression-specific training
