<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>

# Homepage

**The open engine for deep learning workflows.**

Fenn wires up config, logging, monitoring, and notifications — without hiding PyTorch from you. You write real PyTorch code. Fenn handles the rest.

[Get Started](content/quickstart.md){ .md-button .md-button--primary }
[GitHub](https://github.com/pyfenn/fenn){ .md-button }

---

## Why Fenn?

ML projects deserve real infrastructure. Fenn automates the repetitive parts of every experiment so you can focus on the work that actually matters.

| Without Fenn | With Fenn |
|---|---|
| Copy-paste config dicts across every experiment | One YAML file drives your whole pipeline |
| Re-implement logging in each new project | Structured logging out of the box, always on |
| Forget to seed random state — reproduce nothing | Seeds, checksums, and artifacts tracked automatically |
| Find out training crashed hours later | Discord or Telegram ping the moment a run ends |

---

## Core Features

### Auto-Config via YAML

Declare your entire experiment — model arch, optimiser, scheduler, paths — in one YAML. Fenn parses, validates, and injects it. No argparse sprawl.

### Unified Logging

Structured log output — loss, metrics, hyperparams — wired up automatically. Every run gets a consistent, searchable trail without extra setup.

### Backend Monitoring

Native integration with [Weights & Biases](https://wandb.ai/) and [TensorBoard](https://www.tensorflow.org/tensorboard). Connect your dashboard with a single config flag — Fenn handles initialisation, step logging, and teardown.

### Instant Notifications

Get notified the moment your run finishes, fails, or hits a new best metric. Real-time alerts on **Discord** and **Telegram** with no polling or manual checks.

### Built-in Trainers

Classification, regression, segmentation — Fenn ships battle-tested trainer loops so you can focus on architecture and data, not training boilerplate.

### Reproducible Templates

Start any new project from a versioned, opinionated template. Seeds, environments, and artifact paths are locked in from the first commit.

---

## Fine-tune a large language model in under 100 lines of code

**Install**

```bash
pip install fenn fenn[transformers] datasets
```

**Create a config**

```yaml
# fenn.yaml
project: lora-seq-cls

general:
  device: cuda

model:
  name: distilbert-base-uncased
  num_labels: 2
  max_length: 128

train:
  seed: 42
  epochs: 3
  lr: 2e-4
  batch: 16

lora:
  r: 8
  alpha: 16
  dropout: 0.1
```

**Fine-tune**

```python
from fenn import Fenn
from fenn.nn.trainers import LoRATrainer
import torch.optim as optim
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset
from sklearn.metrics import accuracy_score

app = Fenn()

@app.entrypoint
def main(args):
    raw = load_dataset('sst2')
    tokenizer = AutoTokenizer.from_pretrained(args['model']['name'])
    # ... build SentimentDataset and DataLoaders ...

    model = AutoModelForSequenceClassification.from_pretrained(
        args['model']['name'], num_labels=args['model']['num_labels']
    )
    optimizer = optim.AdamW(
        model.parameters(), lr=float(args['train']['lr'])
    )
    trainer = LoRATrainer(
        model=model, optim=optimizer, task_type='SEQ_CLS',
        r=args['lora']['r'], lora_alpha=args['lora']['alpha'],
        lora_dropout=float(args['lora']['dropout']),
        target_modules=['q_lin', 'v_lin'],
        device=args['general']['device'],
    )
    trainer.fit(train_loader, epochs=args['train']['epochs'])
    predictions = trainer.predict(test_loader)
    print(f'Accuracy: {accuracy_score(test_labels, predictions):.4f}')

if __name__ == '__main__':
    app.run()
```

**Launch**

```bash
python main.py
```

Or pull a ready-made template directly:

```bash
fenn pull lora-cls
```

See the full [Quickstart guide](content/quickstart.md) for a complete walkthrough.

---

## Supporting Fenn

If fenn is useful for your work or research, consider supporting its development.

**Star the repository** on GitHub — it improves visibility and helps others discover the project.

Sponsorship funds maintenance, improvements, and new features

[Become a sponsor](https://github.com/sponsors/blkdmr){ .md-button .md-button--primary }

Join the community on [Discord](https://discord.com/invite/6v9xtJxvN7) to discuss ideas, ask questions, and get started.

---

## Cite Fenn

If you use **fenn** in your work or research, please cite the project as:

```bibtex
@software{fenn,
  author       = {Alessio Russo},
  title        = {pyfenn/fenn: Release v0.2.0},
  month        = may,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v0.2.0},
  doi          = {10.5281/zenodo.20178660},
  url          = {https://doi.org/10.5281/zenodo.20178660},
}
```
