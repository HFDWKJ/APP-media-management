Media Manager — portable data folder (dev / portal edition)
============================================================

When `portable.marker` exists beside the app, files are stored here:

- config.json — settings and library roots
- catalog.db — catalog database
- Runtime logs are stored under .log/ at the source/portable application root; installed builds use %APPDATA%/MediaManager/.log/.

These files are **not** committed to Git (see `.gitignore`).
Use Tools → Export database for backups.
