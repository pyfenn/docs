# Managing Templates

The **Templates** page (`/templates`) lists every template you've pulled locally with `fenn pull`, and lets you launch one directly from the browser.

## How templates get here

Every time you run `fenn pull <template> [path]`, Fenn records the template's name, local path, source template, and pull time in a local registry (`~/.fenn/templates_registry.json` by default). The Templates page reads from this registry - pulling is still done via `fenn pull` or `fenn list`, the dashboard just shows you what's already on disk.

If a template's directory is later moved or deleted, it's automatically dropped from the list the next time the registry is read.

> The registry location can be overridden with the `FENN_TEMPLATES_REGISTRY_PATH` environment variable.

## Running a template

Click **Run** next to any listed template to launch it as a background process. The dashboard will:

1. Start the template's entrypoint (`main.py`) as a subprocess.
2. Poll for its session to appear.
3. Redirect you to that session's live view once it's found.

If the template fails to start (for example, a bad `fenn.yaml` or an early crash), the error is shown inline next to the Run button instead of failing silently.

Only templates that appear in the local registry can be launched this way - arbitrary file paths are not accepted.
