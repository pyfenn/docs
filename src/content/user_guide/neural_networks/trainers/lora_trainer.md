# LoRATrainer

The `LoRATrainer` extends the base trainer to support parameter-efficient fine-tuning using LoRA (Low-Rank Adaptation). LoRA is a technique that reduces the number of trainable parameters by approximating weight updates with low-rank matrices.

## Requirements

LoRA support requires the `peft` library to be installed:

```bash
pip install peft
```

## Initialization

```python
from fenn.nn.trainers import LoRATrainer
from peft import LoraConfig

# Define LoRA configuration
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1
)

trainer = LoRATrainer(
    model=base_model,
    loss_fn=loss_fn,
    optim=optimizer,
    lora_config=lora_config,
    device="cuda"
)
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `model` | torch.nn.Module | Base model to fine-tune | Required |
| `loss_fn` | torch.nn.Module | Loss function to use | Required |
| `optim` | torch.optim.Optimizer | Optimizer for weight updates | Required |
| `lora_config` | LoraConfig | LoRA configuration (optional) | None |
| `device` | str/torch.device | Device to run training on | "cpu" |
| `checkpoint_dir` | Path/str | Directory to save checkpoints | None |
| `checkpoint_epochs` | int/list | Checkpoint saving frequency | None |
| `checkpoint_name` | str | Base name for checkpoint files | "lora_checkpoint" |
| `save_best` | bool | Save best model during training | False |

## LoRA Configuration

The `LoraConfig` from `peft` controls which parameters are modified:

```python
from peft import LoraConfig

lora_config = LoraConfig(
    r=8,                                    # Rank of LoRA matrices
    lora_alpha=16,                          # Scaling factor
    target_modules=["q_proj", "v_proj"],    # Modules to apply LoRA to
    lora_dropout=0.1,                       # Dropout rate for LoRA layers
    bias="none",                            # Bias configuration
    task_type="CAUSAL_LM"                   # Task type (optional)
)
```

### Key Parameters

- **r**: Rank of the LoRA matrices (lower = fewer parameters)
- **lora_alpha**: Scaling factor for LoRA updates
- **target_modules**: Which model layers to apply LoRA to
- **lora_dropout**: Dropout applied to LoRA layers
- **task_type**: Task type for inference (CAUSAL_LM, SEQ_2_SEQ_LM, etc.)

## Training

### fit() Method

The LoRATrainer inherits the `fit()` method from the base Trainer:

```python
def fit(
    train_loader: DataLoader,
    epochs: int,
    val_loader: Optional[DataLoader] = None,
    val_epochs: int = 1
) -> None:
    """Train with LoRA-adapted parameters."""
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `train_loader` | DataLoader | Training data | Required |
| `epochs` | int | Number of training epochs | Required |
| `val_loader` | DataLoader | Validation data (optional) | None |
| `val_epochs` | int | Validation frequency | 1 |

### Usage Examples

```python
# Basic training
trainer.fit(train_loader, epochs=10)

# Training with validation
trainer.fit(
    train_loader=train_loader,
    epochs=10,
    val_loader=val_loader,
    val_epochs=1
)
```

## Prediction

### predict() Method

The prediction behavior depends on whether the base model is a classification or regression model:

```python
predictions = trainer.predict(test_loader)
```

## Complete Example

### Fine-tune a Language Model with LoRA

```python
import torch
from peft import LoraConfig
from fenn.nn.trainers import LoRATrainer
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Define LoRA configuration
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# Setup training components
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

# Create trainer
trainer = LoRATrainer(
    model=model,
    loss_fn=loss_fn,
    optim=optimizer,
    lora_config=lora_config,
    device="cuda"
)

# Train
trainer.fit(
    train_loader=train_dataloader,
    epochs=5,
    val_loader=val_dataloader
)

# Make predictions
predictions = trainer.predict(test_dataloader)
```

### Fine-tune with Pre-wrapped Model

If your model is already wrapped with PEFT, omit the `lora_config`:

```python
from peft import get_peft_model
from fenn.nn.trainers import LoRATrainer

# Model is already PEFT-wrapped
peft_model = get_peft_model(base_model, lora_config)

# Create trainer without passing lora_config
trainer = LoRATrainer(
    model=peft_model,
    loss_fn=loss_fn,
    optim=optimizer,
    lora_config=None,  # Already wrapped
    device="cuda"
)

trainer.fit(train_loader, epochs=10)
```

## Advantages of LoRA

- **Fewer Parameters**: LoRA adapts only a small fraction of model parameters
- **Faster Fine-tuning**: Reduced parameters → faster training
- **Easier Deployment**: Store only LoRA weights (~2-5% of original size)
- **Task Flexibility**: Fine-tune large models for multiple tasks with minimal storage

## Common Use Cases

### 1. Fine-tune Large Language Models

```python
# Fine-tune GPT-2, GPT-3, LLaMA, etc. with LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],  # For GPT-2
    task_type="CAUSAL_LM"
)
```

### 2. Fine-tune Vision Transformers

```python
# Fine-tune ViT or DINOv2 models
lora_config = LoraConfig(
    r=4,
    lora_alpha=8,
    target_modules=["qkv"],
    task_type="IMAGE_CLASSIFICATION"
)
```

### 3. Multi-task Learning

```python
# Create different LoRA configurations for different tasks
task1_config = LoraConfig(r=4, lora_alpha=8, target_modules=["q_proj"])
task2_config = LoraConfig(r=4, lora_alpha=8, target_modules=["v_proj"])

trainer1 = LoRATrainer(model, loss_fn, optim, task1_config, device="cuda")
trainer2 = LoRATrainer(model, loss_fn, optim, task2_config, device="cuda")
```

## See Also

- [Base Trainer](base_trainer.md): Core trainer functionality
- [PEFT Documentation](https://huggingface.co/docs/peft/): Detailed LoRA configuration
- [ClassificationTrainer](classification_trainer.md): For classification fine-tuning examples
- [RegressionTrainer](regression_trainer.md): For regression fine-tuning examples
