# Classe Trainer

## Panoramica

La classe `Trainer` è il componente principale per l'addestramento di modelli di deep learning. Fornisce un'interfaccia completa per gestire il ciclo di training, inclusi checkpointing, early stopping, validazione e predizione.

## Initializzazione

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

### Parametri

| Parametro | Tipo | Descrizione | Default |
|-----------|------|-------------|---------|
| `model` | torch.nn.Module | Il modello di deep learning da addestrare | Obbligatorio |
| `loss_fn` | torch.nn loss | Funzione di loss da utilizzare | Obbligatorio |
| `optim` | torch.optim Optimizer | Ottimizzatore per l'aggiornamento dei pesi | Obbligatorio |
| `epochs` | int | Numero di epoche per l'addestramento | Obbligatorio |
| `num_classes` | int | Numero di classi nel problema di classificazione | Obbligatorio |
| `device` | str | Dispositivo su cui eseguire il training (cpu, cuda, mps) | "cpu" |
| `checkpoint_dir` | Path o str | Directory dove salvare i checkpoint | None |
| `checkpoint_epochs` | int o list | Frequenza o liste di epoche per il salvataggio dei checkpoint | None |
| `checkpoint_name` | str | Nome base per i file di checkpoint | "checkpoint" |
| `save_best` | bool | Se True, salva il miglior modello durante il training | False |
| `early_stopping_patience` | int | Numero di epoche senza miglioramento prima di fermare il training | None |

## Funzionalità Principali

### 1. Addestramento: `fit()`

Esegue il ciclo completo di training.

```python
def fit(train_loader, val_loader=None, val_epoch: int = 5, start_epoch: int = 0):
    """
    Args:
        train_loader: DataLoader per i dati di training
        val_loader: DataLoader per i dati di validazione (opzionale)
        val_epoch: Frequenza di validazione (ogni N epoche)
        start_epoch: Epoca da cui riprendere il training (per ripresa da checkpoint)

    Returns:
        model: Il modello addestrato
    """
```

**Caratteristiche:**

- Training loop con backward pass e aggiornamento pesi
- Calcolo della loss media per epoca
- Validazione periodica con metriche (accuracy, precision, recall, F1)
- Checkpointing automatico
- Early stopping automatico

### 2. Predizione: `predict()`

Esegue predizioni su un dataset.

```python
def predict(data_loader):
    """
    Args:
        data_loader: DataLoader contenente i dati da predire

    Returns:
        predictions: Lista di predizioni
    """
```

**Automaticamente seleziona:**
- Predizioni binarie (sigmoid) per 2 classi
- Predizioni multiclassi (argmax) per più classi

### 3. Gestione Checkpoint: `load_checkpoint()`

Carica un checkpoint salvato per riprendere il training.

```python
def load_checkpoint(checkpoint_path):
    """
    Args:
        checkpoint_path: Path al file di checkpoint

    Returns:
        epoch: L'epoca da cui riprendere il training

    Carica:
        - Pesi del modello
        - Stato dell'ottimizzatore
        - Loss migliore fino a quel momento
    """
```

## Funzionalità Avanzate

### Early Stopping

Se `early_stopping_patience` è impostato, il training si ferma automaticamente quando:
- La validation loss non migliora per N epoche consecutive
- Esempio: `early_stopping_patience=5` ferma dopo 5 epoche senza miglioramento

```python
    trainer = Trainer(
        model=model,
        loss_fn=loss_fn,
        optim=optimizer,
        epochs=100,
        num_classes=2,
        early_stopping_patience=5  # Ferma se non migliora per 5 epoche
    )
```

### Checkpointing

Il trainer supporta due strategie di checkpoint:

#### 1. Checkpoint Periodico
Salva ogni N epoche:

```python
    trainer = Trainer(
        ...,
        checkpoint_dir="checkpoints",
        checkpoint_epochs=10,  # Salva ogni 10 epoche
        checkpoint_name="my_model"
    )
```

#### 2. Checkpoint del Miglior Modello
Salva solo il modello con la miglior validation loss:

```python
    trainer = Trainer(
        ...,
        checkpoint_dir="checkpoints",
        save_best=True,
        checkpoint_name="my_model"
    )
```

#### 3. Checkpoint a Epoche Specifiche
Salva a epoche specifiche:

```python
    trainer = Trainer(
        ...,
        checkpoint_dir="checkpoints",
        checkpoint_epochs=[10, 25, 50, 75],  # Salva a queste epoche
        checkpoint_name="my_model"
    )
```

## Metriche di Validazione

Durante la validazione, il trainer calcola automaticamente:

- **Loss**: Valore della loss function
- **Accuracy**: Proporzione di predizioni corrette
- **Precision**: Proporzione di predizioni positive corrette
- **Recall**: Proporzione di veri positivi identificati
- **F1 Score**: Media armonica tra precision e recall

## Esempio di Utilizzo Completo

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from fenn.nn.trainers import Trainer

# Setup
model = MyModel()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Creazione trainer con tutte le feature
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
    val_epoch=5  # Valida ogni 5 epoche
)

# Predizione
predictions = trainer.predict(test_dataloader)

# Ripresa da checkpoint
start_epoch = trainer.load_checkpoint("./checkpoints/my_model_best.pt")
trainer.fit(
    train_loader=train_dataloader,
    val_loader=val_dataloader,
    start_epoch=start_epoch + 1
)
```

## Stato Interno

La classe mantiene i seguenti stati durante il training:

- `_model`: Il modello PyTorch
- `_device`: Dispositivo di computazione
- `_best_loss`: La migliore validation loss vista finora
- `_patience_counter`: Contatore di epoche senza miglioramento (per early stopping)
- `_logger`: Logger per messaggi di sistema

## Metodi Privati

| Metodo | Descrizione |
|--------|-------------|
| `_should_save_checkpoint(epoch)` | Determina se salvare un checkpoint a questa epoca |
| `_save_checkpoint(epoch, loss, is_best)` | Salva un checkpoint su disco |
| `_binary_predict(data_loader)` | Predizioni per problemi binari (2 classi) |
| `_multiclass_predict(data_loader)` | Predizioni per problemi multiclassi (>2 classi) |

## Note Importanti

1. Il modello viene automaticamente spostato sul dispositivo specificato durante l'inizializzazione
2. La validation loss è utilizzata per determinare il miglior modello e per l'early stopping
3. I checkpoint includono sia i pesi del modello che lo stato dell'ottimizzatore
4. Il logger di sistema fornisce informazioni dettagliate su checkpoint e early stopping
