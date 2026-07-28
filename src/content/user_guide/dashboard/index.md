# The Dashboard

The Fenn dashboard is a local web UI for browsing your experiment sessions, viewing logs, and managing the templates you've pulled - all without leaving your browser.

## Starting the Dashboard

```bash
fenn dashboard
```

By default this starts a server at `http://127.0.0.1:5000`. The dashboard only ever binds to `127.0.0.1` - it serves your local logs and is not meant to be exposed on your network.

### Options

| Flag | Description |
|---|---|
| `--port <PORT>` | Port to bind (default: `5000`) |
| `--log-dir <DIR> [DIR ...]` | Extra directories to scan for `.fn` session files, in addition to the current directory |
| `--debug` | Run Flask in debug mode |

Example:

```bash
fenn dashboard --port 8080 --log-dir ./experiments ./archived-runs
```

## Signing In

The first time you open the dashboard, you'll be redirected to a **Connect** page with a "Sign in with pyfenn.com" button. This opens a browser tab for a normal OAuth sign-in and consent flow, then hands control back to the dashboard.

Once you've signed in, your session is cached locally so future launches of `fenn dashboard` skip the sign-in step and re-validate silently in the background. If your saved session is ever revoked or expires, you'll be sent back to the Connect page to sign in again.

## Pages

| Page | What it shows |
|---|---|
| **Overview** (`/`) | All projects with logged sessions, at a glance |
| **Project** (`/project/<name>`) | All sessions for a single project |
| **Session** (`/session/<project>/<id>`) | Full detail for one session - logs, metadata, status |
| **Templates** (`/templates`) | Templates you've pulled locally, with the option to launch them - see [Managing Templates](templates.md) |

For details on filtering, renaming, and archiving sessions, see [Managing Sessions](sessions.md).
