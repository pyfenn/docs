# Pull

The `fenn pull` command allows you to download and use pre-made templates from the [fenn templates repository](https://github.com/pyfenn/fenn/tree/main/templates) for your analysis projects.

## Usage

```bash
fenn pull <template> [path] [--force]
```

### Arguments

- `<template>` (required): The name of the template to download. This corresponds to a folder name in the [pyfenn/templates](https://github.com/pyfenn/fenn/tree/main/templates) repository.
- `[path]` (optional): The target directory where the template should be extracted. Defaults to the current directory (`.`).
- `[--force]` (optional): Overwrite existing files in the target directory if it is not empty.

## Examples

### Basic Usage

Download the `base` template into the current directory:

```bash
fenn pull base
```

### Specify Target Directory

Download the `base` template into a specific directory:

```bash
fenn pull base ./my-project
```

### Overwrite Existing Files

If the target directory already contains files, use the `--force` flag to overwrite them:

```bash
fenn pull base ./existing-project --force
```