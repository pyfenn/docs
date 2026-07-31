=== "Managing Sessions"

    # Managing Sessions

    Every run of your entrypoint is logged as a session. The dashboard provides tools to browse, organize, inspect, and visualize those sessions without touching the underlying log files.

    ## Browsing

    The **Overview** page lists every project with logged sessions. Open a project to see its individual sessions, or open a session directly to see its full logs and metadata.

    Each session has a status:

    - `running` — currently in progress
    - `completed` — finished normally
    - `failed` — finished with an error
    - `crashed` — stopped writing without a proper close (e.g. the process died)

    ## Filtering

    From a project or the overview, sessions can be filtered by:

    - **Project**
    - **Status** (`running`, `crashed`, `completed`, `failed`)
    - **Date range** — sessions started after/before a given `YYYY-MM-DD HH:MM:SS` timestamp
    - **Sort** — by start time, end time, duration, warning count, or exception count (ascending or descending)

    Archived sessions are hidden by default; toggle **Include archived** to bring them back into the list.

    ## Renaming

    Give a session a more memorable display name than its generated ID directly from the session or project view. The underlying `.fn` file and session ID are untouched—only the display name changes.

    ## Archiving

    Archiving hides a session from the default view without deleting anything, making it useful for tidying up old or exploratory runs you want to keep around but not see day-to-day.

    Archived sessions can be restored at any time from the **Include archived** view.

    ## Deleting

    Deleting a session removes it permanently.

    Unlike archiving, deletion cannot be undone. Use archiving instead if you simply want a session out of the way.

=== "Metrics and Graphs"

    # Metrics and Graphs

    In addition to free-text log messages, fenn supports structured numeric metrics through `logger.log_metric()`. These metrics are stored alongside the session log and power the **Graphs** tab in the dashboard.

    ## Logging metrics

    ```python
    from fenn.logging import logger

    logger.log_metric(name, value, step)
    ```

    Parameters:

    - `name` — identifies the metric. The dashboard currently recognizes and renders:
      - `train_loss`
      - `val_loss`
      - `acc`
    - `value` — numeric value to record
    - `step` — x-axis position, typically the training epoch or iteration

    Example:

    ```python
    for epoch in range(epochs):
        train_loss = run_train_epoch(...)
        logger.log_metric("train_loss", train_loss, step=epoch)

        if epoch % val_epochs == 0:
            val_loss, acc = run_validation(...)
            logger.log_metric("val_loss", val_loss, step=epoch)
            logger.log_metric("acc", acc, step=epoch)
    ```

    ## Automatic metric logging

    The built-in trainers log metrics automatically during `fit()`:

    - `ClassificationTrainer`
    - `RegressionTrainer`
    - `LoRATrainer`

    These trainers record:

    - `train_loss` every training epoch
    - `val_loss` and `acc` on validation epochs

    No additional logging code is required when using these trainers.

    ## Metric storage

    Each call to `log_metric()` appends a `<metric>` element to the session's `.fn` file:

    ```xml
    <metric name="train_loss" step="3" value="0.482" ts="2026-07-30 10:04:12" />
    ```

    Metrics are additive and independent of the free-text log entries stored in the same session.

    Sessions created before metric logging was introduced—or sessions that never call `log_metric()`—remain fully compatible. They simply contain no metric data.

    If `log_metric()` is called before the logger has been configured (for example, when using a trainer outside an `@app.entrypoint` execution), the call silently does nothing instead of raising an exception.

    ## Viewing graphs

    Open a session and switch from the **Logs** tab to the **Graphs** tab.

    While a session is still `running`, the Graphs tab displays a placeholder. Once the session finishes, the dashboard renders any available metrics as SVG line charts.

    Currently, three graphs are supported:

    - **Train Loss**
    - **Validation Loss**
    - **Accuracy**

    Sessions without metric data simply display an empty state in the Graphs tab.