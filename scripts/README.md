# Scripts Directory

Helper scripts for managing Confer Agent Kit.

## sync_agent_os.sh

**Purpose:** Sync the `agent-os` submodule with the latest upstream changes from [buildermethods/agent-os](https://github.com/buildermethods/agent-os.git).

**Usage:**
```bash
./scripts/sync_agent_os.sh
```

**What it does:**
1. Initializes the `agent-os` submodule if not already initialized
2. Fetches latest changes from upstream
3. Shows current vs. latest commit
4. Prompts to update to latest upstream
5. Stages the submodule update for commit

**After running:**
- Review the changes: `git diff agent-os`
- Commit the update: `git commit -m 'chore: update agent-os submodule to latest upstream'`
- Push: `git push`

**Why submodules?**
- Allows `agent-os` to be synced independently with upstream
- Keeps `agent-os` as a reference without mixing its history with ours
- Easy to update: just run the sync script

## Manual Submodule Commands

If you prefer to manage the submodule manually:

**Initialize submodule:**
```bash
git submodule update --init --recursive
```

**Update submodule to latest:**
```bash
cd agent-os
git checkout main
git pull origin main
cd ..
git add agent-os
git commit -m 'chore: update agent-os submodule'
```

**Clone repo with submodules:**
```bash
git clone --recursive <repo-url>
```

**Or after cloning:**
```bash
git submodule update --init --recursive
```

