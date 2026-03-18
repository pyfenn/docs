# ClassificationTrainer

The `ClassificationTrainer` is used for binary, multi-class, and multi-label classification tasks. It automatically detects the classification mode and applies appropriate prediction methods.

## Initialization

```python
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=num_classes,
    multi_label=False,
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
| `num_classes` | int | Number of classes to predict | Required |
| `multi_label` | bool | Whether to use multi-label classification | False |
| `device` | str/torch.device | Device to run training on (cpu, cuda, mps) | "cpu" |
| `early_stopping_patience` | int | Epochs without improvement before early stopping | None |
| `checkpoint_config` | Checkpoint | Checkpoint configuration object | None |

## Automatic Mode Detection

The trainer automatically detects the classification mode:

- **Binary**: `num_classes == 2`
  - Uses sigmoid activation
  - Applies threshold at 0.5 for predictions
  
- **Multi-class**: `num_classes > 2`
  - Uses softmax activation
  - Uses argmax for predictions
  
- **Multi-label**: `multi_label=True` and `num_classes >= 2`
  - Uses sigmoid activation
  - Applies threshold at 0.5 for each label

## Training

### fit() Method

```python
def fit(
    train_loader: DataLoader,
    epochs: int,
    val_loader: Optional[DataLoader] = None,
    val_epochs: int = 1
) -> None:
    """Train the classifier with optional validation and early stopping."""
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

# Train with validation every 5 epochs
trainer.fit(train_loader, epochs=100, val_loader=val_loader, val_epochs=5)
```

## Prediction

### predict() Method

```python
def predict(
    dataloader_or_batch: Union[DataLoader, torch.Tensor],
    return_proba: bool = False
) -> Union[List, Tuple[List, List]]:
    """Predict labels for given data."""
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `dataloader_or_batch` | DataLoader/Tensor | Input data | Required |
| `return_proba` | bool | Return probabilities alongside predictions | False |

### Return Values

- If `return_proba=False`: List of predicted labels
- If `return_proba=True`: Tuple of (predictions, probabilities)

### Usage Examples

```python
# Get predictions
predictions = trainer.predict(test_loader)

# Get predictions with probabilities (binary classification)
predictions, probs = trainer.predict(test_loader, return_proba=True)

# Predict on a single batch
batch_tensor = torch.randn(32, 784)
predictions = trainer.predict(batch_tensor)

# Get multi-label predictions
predictions = trainer.predict(test_loader)  # List of label sets
```

## Validation Metrics

During validation, the trainer automatically calculates:

| Metric | Description |
|--------|-------------|
| **Loss** | Classification loss (e.g., CrossEntropyLoss) |
| **Accuracy** | Proportion of correct predictions |
| **Precision** | Proportion of correct positive predictions |
| **Recall** | Proportion of true positives identified |
| **F1 Score** | Harmonic mean between precision and recall |

These metrics are printed at each validation epoch and logged for later analysis.

## Complete Example

### Binary Classification

```python
import torch
from torch import nn
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup
model = SimpleBinaryClassifier()
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Checkpoint configuration
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    save_best=True,
)

# Create trainer
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=2,
    device="cuda",
    checkpoint_config=checkpoint_config,
    early_stopping_patience=5
)

# Training
trainer.fit(
    train_loader=train_dataloader,
    epochs=50,
    val_loader=val_dataloader,
    val_epochs=1
)

# Prediction
predictions = trainer.predict(test_dataloader)
predictions, probs = trainer.predict(test_dataloader, return_proba=True)
```

### Multi-class Classification

```python
import torch
from torch import nn
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup
model = ResNetClassifier(num_classes=10)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Checkpoint configuration
checkpoint_config = Checkpoint(
    directory=Path("./checkpoints"),
    epochs=10,  # Save every 10 epochs
)

# Create trainer
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=10,
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

# Prediction
predictions = trainer.predict(test_dataloader)
```

### Multi-label Classification

```python
import torch
from torch import nn
from fenn.nn.trainers import ClassificationTrainer
from fenn.nn.utils import Checkpoint
from pathlib import Path

# Setup
model = MultiLabelClassifier()
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Create trainer with multi_label=True
trainer = ClassificationTrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    num_classes=50,  # Number of labels
    multi_label=True,
    device="cuda",
    early_stopping_patience=5
)

# Training
trainer.fit(
    train_loader=train_dataloader,
    epochs=100,
    val_loader=val_dataloader,
    val_epochs=1
)

# Prediction
predictions = trainer.predict(test_dataloader)
```

## See Also

- [Base Trainer](base_trainer.md): Core trainer functionality
- [Checkpoint Management](checkpoint_management.md): Saving and loading checkpoints
- [Advanced Features](features.md): Early stopping and validation metrics
