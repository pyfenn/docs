Welcome to **fenn** (Friendly Environment for Neural Networks), a lightweight Python framework designed to strip away the repetitive boilerplate of Machine Learning development.

**Stop writing boilerplate. Start training.**

fenn is a lightweight Python framework that automates the **boring stuff** in Machine Learning projects so you can focus on the model. It handles configuration parsing, logging setup, and experiment tracking in a minimal, opinionated way.

---

## Why fenn?

In a typical ML project, developers often spend hours setting up logging directories, writing YAML parsers, and manually connecting experiment trackers. Fenn automates this entire lifecycle:

* **Auto-Configuration**: YAML files are automatically parsed and injected into your entrypoint. You get full parametrization support without writing a single line of `argparse`.
* **Unified Logging**: All logs, print statements, and experiment metadata are captured to local files and remote backends simultaneously.
* **Multi-Backend Monitoring**: Native integration with [Weights & Biases (W&B)](https://wandb.ai/) and [TensorBoard](https://www.tensorflow.org/tensorboard).
* **Instant Notifications**: Get real-time alerts on **Discord** and **Telegram** when experiments start, finish, or crash.
* **Template Ready**: Download and use reproducible experiment templates to jumpstart new projects.


## Roadmap

- **ML Templates:** Automated creation of standard project structures.
- **Model Tools:** Utilities for Neural Network creation, training, and testing.
- **Notifications:** Email notification system for completed training runs.
- **Data Tools:** Data exploration and visualization helpers.
- **Analysis:** Result analysis tools (diagrams, confusion matrices, etc.).
- **Integrations:** Support for TensorBoard and similar tracking tools.
- **Testing:** Comprehensive unit and integration tests for the framework.