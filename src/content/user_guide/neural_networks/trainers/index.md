# Trainers

FENN provides a modular trainer architecture for training deep learning models. The base `Trainer` class is abstract and provides the core functionality for managing the training cycle, including checkpointing, early stopping, validation, and prediction.

## Available Trainers

- **[Base Trainer](base_trainer.md)**: Abstract base class with core training functionality
- **[ClassificationTrainer](classification_trainer.md)**: For binary, multi-class, and multi-label classification tasks
- **[RegressionTrainer](regression_trainer.md)**: For regression tasks
- **[LoRATrainer](lora_trainer.md)**: For parameter-efficient fine-tuning with LoRA (Low-Rank Adaptation)

## Common Features

All trainers share common functionality:

### Training
- `fit()` method for training loops
- Optional validation every N epochs
- Automatic loss calculation per epoch

### Prediction
- `predict()` method for inference
- Support for DataLoaders and batch tensors

### Checkpointing
- Save and resume training from checkpoints
- Automatic best model saving
- Checkpoint loading at specific epochs

### Early Stopping
- Automatic training termination when model stops improving
- Configurable patience counter
- Tracks training or validation loss depending on configuration

### State Management
- Training state tracking through epochs
- Model and optimizer state persistence
- Metrics logging (accuracy, loss, F1, etc.)

## Shared Functionality

See the following pages for shared functionality across all trainers:

- **[Checkpoint Management](checkpoint_management.md)**: Saving, loading, and resuming from checkpoints
- **[Advanced Features](features.md)**: Early stopping, validation metrics, training state management
