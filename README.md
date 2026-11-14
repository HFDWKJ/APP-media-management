<p align="center">
  <img src="assets/media_manager_app_icon.png" alt="Media Manager" width="128"/>
</p>

<h1 align="center">Media Manager</h1>

<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">Simplified Chinese</a> · <a href="README.ja.md">Japanese</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a>
</p>

<p align="center">
  <a href="https://github.com/HFDWKJ/APP-media-management/releases"><img src="https://img.shields.io/github/v/release/HFDWKJ/APP-media-management?label=release&logo=github" alt="Release"/></a>
  <a href="https://github.com/HFDWKJ/APP-media-management"><img src="https://img.shields.io/badge/platform-Windows-0078D6?logo=windows" alt="Windows"/></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://www.riverbankcomputing.com/software/pyqt/"><img src="https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt" alt="PyQt6"/></a>
</p>

<p align="center">
  Windows desktop app to catalog media across multiple drives and devices,<br/>
  detect <code>[Original Name]</code> folder duplicates, and reorganize extracted downloads.
</p>

<p align="center">
  <b>Version:</b> 0.0.4 · <b>Developer:</b> Dong, Zhexi
</p>

---

## Table of contents

- [Features](#features)
- [Download](#download)
- [Quick start](#quick-start)
- [Built with Cursor & Vibe Coding](#built-with-cursor--vibe-coding)
- [Build (Nuitka)](#build-nuitka-only)
- [Config & data paths](#config--data-paths)
- [Application updates](#application-updates)
- [Project structure](#project-structure)
- [Roadmap & docs](#roadmap--docs)
- [License](#license)

---

## Features

| Area | Description |
|------|-------------|
| **Multi-root library** | Index folders on SSD/HDD, NAS, DAS, and USB; catalog stays usable when a device is offline |
| **Duplicate detection** | Tier 1: fast `[Original Name]` fuzzy match · Tier 2: SHA-256 when you choose **Verify with Hash** |
| **Reorganize** | Flatten extraction folders into `[Collections]` with templates, progress bar, percentage, and ETA |
| **Face UID** | Short unique IDs with nicknames, region, and comments |
| **Portable edition** | `data\` beside the exe for config and database; `.log\` for logs |
| **Auto-update** | Checks [GitHub Releases](https://github.com/HFDWKJ/APP-media-management/releases) on startup |
| **UI** | DiskGenius-inspired dark theme and Office-style ribbon |

---

## Download

Pre-built binaries are published on **[GitHub Releases](https://github.com/HFDWKJ/APP-media-management/releases)**:

| Edition | File |
|---------|------|
| Installer | `MediaManagerSetup_0.0.4.exe` |
| Portable zip | `MediaManagerPortal_v0.0.4.zip` |

> [!NOTE]
> **Smart App Control:** Unsigned builds may be blocked on Windows 11. Turn off SAC on a test machine, or sign the installer for production use.

---

## Quick start

### Requirements

- Python 3.10+
- Windows 11 (Windows 10+ supported)

### Setup & run

```powershell
git clone https://github.com/HFDWKJ/APP-media-management.git MediaManager
cd MediaManager
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\create_test_data.py   # optional sample folders
python src\main.py
```

### Try the workflow

1. **Add Library Root** — point at `test_data\library` or your download folder.
2. **Discover / Scan** — index `[Original Name]` extraction folders.
3. **Review Name Matches** — dismiss, mark different, or **Verify with Hash**.
4. **Reorganize ([Collections])** — preview flatten/rename.
5. **Show in Explorer** — open the folder when the device is online.

> [!TIP]
> Running from source opens the GitHub releases page when you choose **Download and update**. Packaged builds download and install in-app.

---

## Built with Cursor & Vibe Coding

This project is a **real-world test of AI-assisted development** with [Cursor](https://cursor.com) and **Vibe Coding**: describe intent in natural language, let the Agent implement, then refine by running the app and giving feedback.

| Stage | How |
|-------|-----|
| **Planning** | [`.doc/Development-Plan.md`](.doc/Development-Plan.md) — phased prompts for each milestone |
| **Implementation** | Agent built `core/`, `gui/`, packaging scripts, and release flow step by step |
| **UI iteration** | Screenshot-driven feedback (ribbon, progress bar, filters) |
| **Release tracking** | [`.rec/Roadmap.md`](.rec/Roadmap.md) + GitHub Issues / Milestones |

**Typical loop:** Prompt → Agent edits → run `MediaManager.exe` → screenshot / error feedback → ship release.

> Historical Chinese translation: [Cursor development section](https://github.com/HFDWKJ/APP-media-management/blob/f04c9f41a4c1c9b08ea72a0c91bfe910f608669b/README.zh-CN.md#使用-cursor-与-vibe-coding-开发).

### Practical notes

- Keep a living plan (`.doc/Development-Plan.md`) for stable Agent context across sessions.
- Test **packaged** Nuitka builds early — runtime detection differs from `python src\main.py`.
- Packaging rule: **Nuitka only**, no Inno Setup (enforced via Cursor user rules).
- Public GitHub Releases simplify auto-update (no token required).

---

## Build (Nuitka only)

Build scripts install dependencies automatically. Nuitka uses MSVC when available, otherwise MinGW64.

### Application

```powershell
.\scripts\build_nuitka.ps1              # dist\MediaManager\MediaManager.exe
.\scripts\build_nuitka.ps1 -Mode onefile  # dist\MediaManager.exe
```

### Installer

```powershell
.\scripts\build_installer.ps1
# → dist_installer\MediaManagerSetup_0.0.4.exe
```

Silent flags for in-app updates: `/VERYSILENT`, `/SUPPRESSMSGBOXES`, `/NORESTART`, `/CLOSEAPPLICATIONS`, optional `/DIR=...`.

### Portable zip

```powershell
.\scripts\build_portal.ps1
# → dist_portal\MediaManagerPortal_v0.0.4.zip
```

---

## Config & data paths

**Installed edition**

| Item | Path |
|------|------|
| Config | `%APPDATA%\MediaManager\config.json` |
| Database | `%APPDATA%\MediaManager\catalog.db` |
| Logs | `%APPDATA%\MediaManager\.log\` |

**Portable edition** — `portable.marker` beside `MediaManager.exe`, or use the portal build:

| Item | Path |
|------|------|
| Config | `data\config.json` |
| Database | `data\catalog.db` |
| Logs | `.log\` |

Copy the **entire folder** (including `data\`) to move catalog and settings to another PC.

---

## Application updates

- **Startup check** (on by default) and **Options → Check for updates…**
- Disable in **Settings → Updates**
- Tag future releases `vX.Y.Z` under [.doc/Versioning.md](.doc/Versioning.md); release notes appear in the update dialog. Preserve legacy tags such as `v0.0.4.1`.
- Private repos: set `update.github_token` in config or `GITHUB_TOKEN` env var

---

## Project structure

```text
src/
  main.py              Entry point
  core/                Database, scan, match, reorganize, updates
  gui/                 PyQt6 UI
  installer/           Nuitka setup wizard
  utils/               Config, logging, paths
assets/                App icon
scripts/               Build & helper scripts
.rec/Roadmap.md        Milestone checklist
.doc/Development-Plan.md  Cursor phased development plan
CHANGELOG.md           Release notes (shown in About dialog)
```

---

## Roadmap & docs

| Document | Description |
|----------|-------------|
| [README.zh-CN.md](README.zh-CN.md) | Simplified Chinese |
| [README.ja.md](README.ja.md) | Japanese |
| [README.fr.md](README.fr.md) | Français |
| [README.de.md](README.de.md) | Deutsch |
| [README.ko.md](README.ko.md) | 한국어 |
| [README.es.md](README.es.md) | Español |
| [.rec/Roadmap.md](.rec/Roadmap.md) | Version plans and v0.0.4 checklist |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [GitHub Milestones](https://github.com/HFDWKJ/APP-media-management/milestones) | Issue tracking |
| [.doc/Development-Plan.md](.doc/Development-Plan.md) | Full Cursor development plan |

---

## License

Private / personal project by **Dong, Zhexi**. See repository settings for distribution terms.

## Versioning

Future releases follow [the project SemVer policy](.doc/Versioning.md).


## Log storage

Source and portable runs write UTC runtime logs and reorganization CSV receipts under root `.log/`. Installed builds use writable `%APPDATA%/MediaManager/.log/` with the same UTC filename format. Receipt filenames distinguish source folders and same-hour runs without overwriting prior evidence. Existing markers and catalog data keep their established locations; legacy CSV reports remain readable. `CHANGELOG.md` is a navigation index to dated `.log/` release records, which the About dialog and packaging scripts include. Windows packaging and installed-path behavior still require device acceptance.

## Repository layout and content roles

Apply the [canonical auxiliary-directory catalog](https://github.com/HFDWKJ/MyProtocol/blob/8722d0d2279337d2e414bac90bf00663afc3d7d0/System-Conventions/Repository-Auxiliary-Directories.md). Custom support categories use a dot plus three lowercase letters and are created only when needed. The following classification preserves primary project content and required consumer interfaces.

| Path | Role and boundary |
| --- | --- |
| `.doc/` | Maintained project support documentation and versioning guidance. |
| `.log/` | Dated execution evidence; existing receipt bodies are preserved. |
| `.rec/` | Current support status or publication-scope register. |
| `assets/` | Existing browser, package or published-site resource paths retained; no deployment layout change. |
| `data/` | Project dataset, preserved source input, or consumer-bound fixture; identifiers, raw payloads and established readers retained. |
| `installers/` | Installer source consumed by the current packaging workflow; not a generated installer output. |
| `scripts/` | Existing source/import/command or test-harness layout; current consumers retain their supported paths. |
| `src/` | Existing source/import/command or test-harness layout; current consumers retain their supported paths. |
| `test_data/` | Project dataset, preserved source input, or consumer-bound fixture; identifiers, raw payloads and established readers retained. |

Root README/AGENTS, licenses, version authorities, manifests and launch/configuration interfaces retain their supported locations. Versioning guidance is maintained in [.doc/Versioning.md](.doc/Versioning.md). Private local data and existing runtime settings are not relocated or uploaded by this classification. Old paths and original hashes are recoverable from the dated migration receipt and its pinned source commit. This source/layout update does not establish deployment, device acceptance or automatic synchronization.

## Work tracking

Use [Issues](https://github.com/HFDWKJ/APP-media-management/issues) for tasks and acceptance, and [milestones](https://github.com/HFDWKJ/APP-media-management/milestones) for delivery groups. The owner’s private Project provides the cross-repository view. Current task status is read from GitHub; repository files retain specifications, domain data, source/identity mappings and dated evidence. Creating a task does not execute it or establish runtime acceptance.
