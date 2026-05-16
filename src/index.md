<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>

# Home

[![DOI](https://zenodo.org/badge/1098344896.svg)](https://doi.org/10.5281/zenodo.20178659)![GitHub stars](https://img.shields.io/github/stars/blkdmr/fenn?style=social) ![GitHub forks](https://img.shields.io/github/forks/blkdmr/fenn?style=social) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/261c40f69583462baa200aee959bcc8f)](https://app.codacy.com/gh/blkdmr/fenn/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) [![codecov](https://codecov.io/gh/pyfenn/fenn/graph/badge.svg?token=7RTTZ1SFMM)](https://codecov.io/gh/pyfenn/fenn)
![PyPI version](https://img.shields.io/pypi/v/fenn) ![License](https://img.shields.io/github/license/blkdmr/fenn) [![PyPI Downloads](https://img.shields.io/pypi/dm/fenn.svg?label=downloads&logo=pypi&color=blue)](https://pypi.org/project/fenn/) [![Discord Server](https://img.shields.io/badge/Discord-PyFenn-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/6v9xtJxvN7)[![Sponsor](https://img.shields.io/badge/sponsor-GitHub-pink)](https://github.com/sponsors/blkdmr)

**Stop writing boilerplate. Start training.**

Friendly Environment for Neural Networks (fenn) is a simple framework that automates ML/DL workflows by providing prebuilt trainers, templates, logging, configuration management, and much more. With fenn, you can focus on your model and data while it takes care of the rest.

## Support fenn

If fenn is useful for your work or research, consider supporting its development.

You can support the project by **starring the repository** on GitHub. It improves visibility and helps others discover fenn.

Sponsorship also helps fund maintenance, improvements, and new features.

Support the project:
https://github.com/sponsors/blkdmr

## Why fenn?

- **Auto-Configuration**: YAML files are automatically parsed and injected into your entrypoint with CLI override support. No more hardcoded hyperparameters or scattered config logic.

- **Unified Logging**: All logs, print statements, and experiment metadata are automatically captured to local files and remote tracking backends simultaneously with no manual setup required.

- **Backend Monitoring**: Native integration with industry-standard trackers like [Weights & Biases](https://wandb.ai/) (W&B) for centralized experiment tracking and [TensorBoard](https://www.tensorflow.org/tensorboard) for real-time metric visualization

- **Instant Notifications**: Get real-time alerts on **Discord** and **Telegram** when experiments start, complete, or fail—no polling or manual checks.

- **Trainers**: Built-in support for training loops, validation, and testing with minimal boilerplate. Just define your model and data, and let fenn handle the rest.

- **Template Ready**: Built-in support for reproducible, shareable experiment templates.

## Cite fenn

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

## Contributing

Contributions are welcome! 

Interested in contributing? Join the community on [Discord](https://discord.com/invite/6v9xtJxvN7).

We can then discuss a possible contribution together, answer any questions, and help you get started!

**Please consult our CONTRIBUTING.md and CODE_OF_CONDUCT.md before opening a pull request.**

## Maintainers

The development and long-term direction of **fenn** is guided by the following maintainers:

| Maintainer | Role |
|------------|------|
| [@blkdmr](https://github.com/blkdmr) | Creator & Project Administrator |
| [@giuliaOddi](https://github.com/giuliaOddi) | Project Administrator |
| [@franciscolima05](https://github.com/franciscolima05) | Core Maintainer |

Maintainers oversee the project roadmap, review pull requests, coordinate releases, and ensure the long-term stability and quality of the framework.

Thank you for supporting the project

<a href="https://www.netlify.com">
  <img src="https://www.netlify.com/assets/badges/netlify-badge-light.svg" alt="Deploys by Netlify" />
</a>