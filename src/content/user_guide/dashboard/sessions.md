# Managing Sessions

Every run of your entrypoint is logged as a session, and the dashboard gives you tools to browse, organize, and clean up those sessions without touching the log files by hand.

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

Archived sessions are hidden by default; toggle "include archived" to bring them back into the list.

## Renaming

Give a session a more memorable display name than its generated ID directly from the session or project view. The underlying `.fn` file and session ID are untouched - only the display name changes.

## Archiving

Archiving hides a session from the default view without deleting anything - useful for tidying up old or exploratory runs you want to keep around but not see day-to-day. Archived sessions can be restored at any time from the "include archived" view, which brings them back into the normal listing.

## Deleting

Deleting a session removes it permanently. Unlike archiving, this cannot be undone - use archiving instead if you just want a session out of the way.
