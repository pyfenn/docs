# Local Logging

FENN streamlines output management by automatically intercepting standard `print` calls. It generates clean, timestamped logs on disk while preserving real-time output in the terminal for interactive monitoring.

### Initialization

The logging subsystem is fully managed by the framework core. It initializes automatically at the start of a run, deriving its settings directly from the `fenn.yaml` configuration file. No manual instantiation is required.

### Log file behavior

 upon starting a session, the logger performs the following actions:

*   **File Creation:** Initializes a log file at `<project>/<session_id>.log` within the directory defined in `fenn.yaml`. If the file exists, it is overwritten.
*   **Status Reporting:** Outputs the absolute path of the active log file to the console for verification.
*   **Stream Interception:** Wraps the native Python [`print()`](https://docs.python.org/3/library/functions.html#print) function. Subsequent calls are dual-streamed: they appear in the terminal and are appended to the log file with timestamps.

**Example Output**

A generated log file (`<project>/<session_id>.log`) typically follows this structure:

```text
[2025-11-25 08:48:04] project: autonomous_agent_v1
[2025-11-25 08:48:04] training/seed: 42
[2025-11-25 08:48:04] training/epochs: 100
[2025-11-25 08:48:04] training/learning_rate: 3e-4
[2025-11-25 08:48:04] training/weight_decay: 0.01
[2025-11-25 08:48:04] training/train_batch: 64
[2025-11-25 08:48:04] training/test_batch: 64
```