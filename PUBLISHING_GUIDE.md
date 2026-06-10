# Publishing Pilot Control to GitHub — step-by-step

> A complete walkthrough from "I have the files on my machine" to "the repo
> is live on github.com." Designed to be followed line by line.

**What you'll have at the end:** a public GitHub repo at
`https://github.com/willstarn/pilot-control` with CI running green, the
dataset rendered properly in the README, and everything ready to share.

**Estimated time:** 15–20 minutes the first time (longer if you need to
install git or the GitHub CLI). 2 minutes on subsequent runs.

---

## 0  ·  What you already have in your workspace folder

Open the folder `pilot_control_dataset` on your machine. It already contains:

- The 40-case dataset (`cases/`, `dev/`, `test/`, JSON + JSONL aggregates)
- The Inspect harness (`inspect_eval/pilot_control_task.py`, `tools.py`, `run_pilot_control.py`)
- The generation-discipline artifacts (`generation/`)
- The validation reports (`*_validation_report.md`, `content_audit.md`)
- The portfolio scaffolding I added: `LICENSE`, `.gitignore`, `pyproject.toml`, `CITATION.cff`, `.github/workflows/ci.yml`, `tests/test_smoke.py`
- This guide (`PUBLISHING_GUIDE.md`)
- The one-shot publish script (`publish.sh`)
- The integration plan (`INTEGRATION_PLAN.md`)

Everything you need is in this folder. Nothing else has to be downloaded.

---

## 1  ·  Prerequisites — does your machine have what it needs?

Open **Terminal** (macOS: ⌘+Space → "Terminal"; Windows: install
[Git Bash](https://git-scm.com/downloads) or use WSL).

Run these three commands one at a time. You should see version numbers,
not "command not found."

```bash
git --version
gh --version
python3 --version
```

**Expected output (your version numbers will differ):**

```
git version 2.39.3
gh version 2.40.0
Python 3.11.7
```

If `git` is missing → install at https://git-scm.com/downloads
If `gh` is missing → install at https://cli.github.com (the easiest path)
If `python3` is missing → install at https://www.python.org/downloads/

Re-open Terminal after installing anything new so the new commands are found.

---

## 2  ·  GitHub account + authentication (one-time setup)

If you don't have a GitHub account yet, create one at
https://github.com/signup. Use the username `willstarn` (or whichever
username you actually want — pass it as the argument when you run the
script).

Once you have an account, authenticate the CLI:

```bash
gh auth login
```

It will ask:

1. **What account do you want to log into?** → `GitHub.com`
2. **What is your preferred protocol?** → `HTTPS` (easiest)
3. **Authenticate Git with your GitHub credentials?** → `Yes`
4. **How would you like to authenticate GitHub CLI?** → `Login with a web browser`

A code will appear in your terminal. Copy it, press Enter, and a browser
window will open to https://github.com/login/device. Paste the code,
authorise the CLI. Return to Terminal — it will say
"✓ Authentication complete."

**Verify:**

```bash
gh auth status
```

Expected output:

```
github.com
  ✓ Logged in to github.com account willstarn (...)
  - Active account: true
  - Git operations protocol: https
```

If you see this, you're set up forever. Skip this section on future projects.

---

## 3  ·  Find the path to your `pilot_control_dataset` folder

Three ways, easiest first.

### Way A — Drag-and-drop (macOS, simplest)

1. Open **Finder**.
2. Navigate to where `pilot_control_dataset` lives.
3. Open **Terminal** alongside Finder.
4. Type `cd ` (with a trailing space — don't press Enter yet).
5. Drag the `pilot_control_dataset` folder from Finder into Terminal.
   The full path appears automatically.
6. Press Enter.

You'll now be inside the folder. To confirm, run `pwd` — it should print
the full path; and `ls` should show `README.md`, `cases/`, `data/`,
`publish.sh`, etc.

### Way B — Right-click "Copy as Pathname" (macOS)

1. In **Finder**, locate `pilot_control_dataset`.
2. Right-click the folder, hold **Option** (the menu changes), choose
   **"Copy 'pilot_control_dataset' as Pathname"**.
3. In **Terminal**:

```bash
cd "<paste the path here>"
```

(Keep the double quotes if the path contains spaces.)

### Way C — Search (any OS)

In Terminal:

```bash
find ~ -type d -name "pilot_control_dataset" 2>/dev/null
```

This prints the full path. Copy and `cd` into it.

**Sanity check** — once you're in the right folder, this should list the
expected files:

```bash
ls
```

You should see at minimum: `README.md`, `LICENSE`, `pyproject.toml`,
`publish.sh`, `cases/`, `data/`, `inspect_eval/`.

If you don't see those, you're in the wrong folder. Re-check the path.

---

## 4  ·  The one-command happy path

You're now inside `pilot_control_dataset` and logged into `gh`. Run:

```bash
chmod +x publish.sh
./publish.sh willstarn
```

That's it. The script will:

1. Replace the `<your-username>` placeholders in `pyproject.toml` and
   `CITATION.cff` with `willstarn`.
2. Run `git init -b main` if the folder isn't already a git repo.
3. Stage all files (`git add .`) and create the initial commit.
4. Create a public repo `willstarn/pilot-control` on GitHub via `gh`.
5. Add the remote and push the commit.

**Expected output (final two lines):**

```
==> Done.
    Repo:  https://github.com/willstarn/pilot-control
    CI:    https://github.com/willstarn/pilot-control/actions
```

Open the URL. You should see the dataset README rendered, with all files
visible in the file tree. Done.

If you see an error instead, jump to Section 7 (common errors).

---

## 5  ·  Manual fallback — if `publish.sh` fails

If the script breaks for any reason, you can do the same work manually.
Run these commands one at a time, inside `pilot_control_dataset`:

```bash
# 1. Replace placeholders manually (macOS sed syntax)
sed -i '' 's|<your-username>|willstarn|g' pyproject.toml CITATION.cff

# (Linux: drop the '' — sed -i 's|<your-username>|willstarn|g' pyproject.toml CITATION.cff)

# 2. Initialise the repo on the main branch
git init -b main

# 3. Stage everything (the .gitignore prevents secrets and caches from being added)
git add .

# 4. Check what's about to be committed (optional but good practice)
git status

# 5. Make the first commit
git commit -m "initial scaffold: Pilot Control benchmark dataset, Inspect harness, scoring, and docs"

# 6. Create the public GitHub repo and push in one step
gh repo create willstarn/pilot-control \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "A maritime safety benchmark for LLM agents — TARA APAC capstone project."
```

That's the same work the script does, just spelled out. The final line
prints the repo URL.

---

## 6  ·  Verify everything worked

Three things to check, in order.

### a) The README renders correctly

Open `https://github.com/willstarn/pilot-control` in a browser. The
dataset README should display as formatted Markdown — tables visible,
links clickable, no raw `|` or `#` symbols.

### b) CI runs green

Click the **Actions** tab on the repo page. The first run starts
automatically when you push; it takes ~90 seconds.

- **Green tick (✓)** = good. Skip to step (c).
- **Red cross (✗)** = a test or lint failed. Click into the run and
  read the log. Most likely cause: a missing import in `inspect_eval/`
  because `inspect_ai` couldn't be installed in CI. The smoke tests
  (`tests/test_smoke.py`) try to import the package; if that fails,
  re-check `pyproject.toml`. Paste the error into chat and I'll help.

### c) The eval harness works locally

Back in Terminal, inside `pilot_control_dataset`:

```bash
# Create a virtual environment and install
python3 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e .[dev]

# Set the API key Inspect will use
export OPENAI_API_KEY=sk-...   # or ANTHROPIC_API_KEY for Claude

# Run two scenarios as a smoke test
inspect eval inspect_eval/pilot_control_task.py@pilot_control \
  --model openai/gpt-4o-mini \
  --log-dir ./logs \
  --limit 2 \
  -T split=dev
```

You should see a table with one row per scenario, scored on the five
deterministic scorers. Total cost: cents.

---

## 7  ·  Polish the repo on GitHub (5 minutes)

Once it's live, do these things on the GitHub web UI to make it look
professional:

### a) Add a description and homepage URL

On the repo page (`https://github.com/willstarn/pilot-control`), click
the **gear icon** next to "About" (top right). Fill in:

- **Description:** "A maritime safety benchmark for LLM agents."
- **Website:** leave blank for now, or add a LessWrong link if you
  publish a post in W14.

### b) Add topics

In the same "About" sidebar, click **Add topics**. Add (paste each, press
space between):

```
ai-safety  llm-evaluation  maritime  inspect  colregs  mass
benchmark  evaluation  ukaisi  arena
```

Topics make the repo findable on GitHub's search.

### c) Pin the repo on your profile

Go to your profile (`https://github.com/willstarn`), click
**Customize your pins**, and pin `pilot-control`. This puts it on the
front page of your profile, where recruiters look first.

### d) Optionally: enable Discussions

Repo **Settings → Features → Discussions** → check the box. This gives
you a public place for people to ask questions about the benchmark.

---

## 8  ·  Common errors and how to fix them

### "fatal: not a git repository"

You're outside the folder. `cd` back into `pilot_control_dataset` and try again.

### "Permission denied: ./publish.sh"

The script isn't marked executable. Run:

```bash
chmod +x publish.sh
./publish.sh willstarn
```

### "gh: command not found"

Install the GitHub CLI from https://cli.github.com. On macOS:

```bash
brew install gh
```

### "GraphQL: Could not resolve to a User with the login of 'willstarn'"

The username `willstarn` doesn't exist on GitHub yet. Either create the
account at https://github.com/signup or use a username you've already
registered. The script accepts any username as the argument.

### "remote origin already exists"

You've run the script before but the push failed mid-flight. Run:

```bash
git remote remove origin
./publish.sh willstarn
```

### "Updates were rejected because the remote contains work that you do not have locally"

Someone (probably you, in a previous attempt) pushed something to the
repo already. Run:

```bash
git pull origin main --rebase
git push -u origin main
```

### CI fails on `ruff check`

Your local code has a lint issue. Run:

```bash
pip install ruff
ruff check inspect_eval tests --fix
git add .
git commit -m "lint fixes"
git push
```

### CI fails on `pytest`

A test in `tests/test_smoke.py` is failing. Click into the failed run on
GitHub's Actions tab to see the exact failure. Paste it into chat and I'll
debug.

### "fatal: refusing to merge unrelated histories"

You created the repo on GitHub first with a README, then tried to push
your local commits. Two ways to fix:

**Option A (recommended):** delete the GitHub repo (Settings → Danger
Zone → Delete) and let `publish.sh` create it fresh.

**Option B (merge):** force-pull and resolve:

```bash
git pull origin main --allow-unrelated-histories
# resolve any conflicts (open the files, look for <<<<<<< markers, fix them)
git add .
git commit -m "merge GitHub-created README with local scaffold"
git push -u origin main
```

### My GitHub username has a hyphen / different spelling

No problem. Just pass it as the argument:

```bash
./publish.sh willis-tarn
# or
./publish.sh willistarn
# or whatever your actual handle is
```

---

## 9  ·  After publishing — what to do next

In priority order:

1. **Take a screenshot of the rendered repo** and add it to your CV /
   LinkedIn / personal site. This is your portfolio piece.

2. **Verify the smoke-test eval runs** (Section 6c). Confirms the
   harness is reproducible by a stranger cloning the repo.

3. **Send the repo URL to Kyle Reynoso** as part of your Week 11
   lock-in conversation. Concrete code is the strongest possible signal
   that the W12 build will land.

4. **Pick up Gap 1 from INTEGRATION_PLAN.md** — add the CoT and agent
   conditions to the Inspect Task. ~3 hours, central to the H1 question.

5. **Send the two cold emails** to DNV's autonomous-ships group and
   UK MOD Project Cabot, linking the repo. Low cost, real upside.

6. **Optionally:** post to LessWrong / Alignment Forum after W14 with
   the results notebook. Link from the repo README.

---

## 10  ·  Reference — file inventory

Files this repo contains, grouped by purpose:

**Portfolio / git essentials (added by me):**
- `LICENSE` — MIT, 2025, Willis Tarn
- `.gitignore` — excludes Python caches, env files, secrets, eval logs
- `pyproject.toml` — modern Python packaging, declares `inspect-ai` dep
- `CITATION.cff` — academic citation file GitHub renders on the repo page
- `.github/workflows/ci.yml` — runs `ruff` + `pytest` on every push
- `tests/test_smoke.py` — verifies imports, dataset shape, family balance
- `publish.sh` — the one-shot publish script
- `PUBLISHING_GUIDE.md` — this file

**The dataset and harness (you already had):**
- `README.md` — dataset README (file inventory, schema, smoke-test commands)
- `README_INSPECT.md` — Inspect-specific run instructions
- `cases/` — 40 individual case JSONs (`PC-{MD,AT,IE,ASV}-{01..10}.json`)
- `dev/`, `test/` — 20 + 20 split per-case JSONs
- `data/inspect_samples_{all,dev,test}.jsonl` — Inspect-ready records
- `data/inspect_sample_schema.json` — JSON schema for the records
- `pilot_control_cases_{all,dev,test}.{json,jsonl}` — aggregated dataset
- `pilot_control_cases_summary.csv` — compact tabular summary
- `inspect_eval/pilot_control_task.py` — Inspect Task and 5 deterministic scorers
- `inspect_eval/tools.py` — 4 agent-condition tools (added by me)
- `inspect_eval/run_pilot_control.py` — CLI helper
- `requirements-inspect.txt` — minimal requirements

**Documentation:**
- `schema.md` — dataset schema and controlled vocabularies
- `research_notes.md` — COLREGs / UNCLOS / MASS reference notes
- `validation_report.md` — schema + split validation
- `inspect_ready_validation_report.md` — Inspect-format validation
- `content_audit.md` — content audit report
- `inspect_format_gap_analysis.md` — gap analysis against Inspect requirements
- `dataset_release_notes.md` — release notes
- `INTEGRATION_PLAN.md` — what's missing for the full benchmark
- `generation/` — seed manifest, generation protocol, quality rubric,
  audit log, duplicate audit (ARENA 3.2 alignment artifacts)

That's everything. Push the lot to GitHub and you have a credible
portfolio piece.
