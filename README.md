# modulo_ia_core – AI Content Engine (Demo)

Python-based AI content engine for generating long-form, SEO-optimised articles and exporting them as Markdown and HTML.

> This repository contains a **demo version** of the engine. All API keys, tokens and environment variables are placeholders. The full production code and configuration are kept private.

---

## Key features

- Generate long-form articles from a single JSON/CSV “topic” input.
- Multilingual content generation (up to 50+ languages in the production system).
- Automatic on-page SEO helpers: title/meta suggestions, heading structure, FAQ blocks, internal link placeholders.
- Export pipelines for Markdown and static HTML (suitable for static sites or CMS import).
- Metrics logging to CSV to analyse clicks, conversions and article performance over time.
- Pluggable modules for affiliate links and image retrieval (e.g. Pixabay, Nutriprofits, Amazon – configured via environment variables).

---

## Tech stack

- Python 3.x  
- Standard library (`pathlib`, `csv`, `json`, `logging`, etc.)  
- Optional FastAPI / CLI wrappers (not all included in this minimal demo)  
- Docker-friendly layout (configuration via env vars and `config/settings.json`)

---

## Repository layout (simplified)

- `core/` – main content engine modules (prompt building, language / locale management, generators).
- `tools/` – utilities for Markdown → HTML, performance analysis, CSV helpers and other support scripts.
- `config/` – configuration loader and `settings.example.json`.
- `data/` / `examples/` – example CSV/JSON input files and log outputs (clicks, conversions, link options).

> Folder names may differ slightly depending on the version you are running, but the idea is the same: **core engine**, **tools**, **config**, **example data**.

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/modulo_ia_core.git
cd modulo_ia_core

