#!/bin/bash
# Sync agent-os submodule with upstream repository
# Run this script to update agent-os to the latest from upstream

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

echo "🔄 Syncing agent-os submodule with upstream..."
echo ""

# Initialize submodule if not already initialized
if [ ! -f agent-os/.git ]; then
    echo "📦 Initializing agent-os submodule..."
    git submodule update --init --recursive
fi

cd agent-os

# Fetch latest from upstream
echo "📥 Fetching latest changes from upstream..."
git fetch origin

# Get current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Show what would change
echo ""
echo "Current commit:"
git log -1 --oneline

echo ""
echo "Latest upstream commit:"
git log -1 --oneline origin/main

echo ""
read -p "Update agent-os to latest upstream (origin/main)? [y/N] " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Updating agent-os to latest upstream..."
    git checkout main
    git pull origin main
    
    cd "$REPO_ROOT"
    
    # Stage the submodule update
    git add agent-os
    
    echo ""
    echo "✅ agent-os updated to latest upstream"
    echo ""
    echo "To commit this update:"
    echo "  git commit -m 'chore: update agent-os submodule to latest upstream'"
    echo ""
    echo "To push the submodule update:"
    echo "  git push"
else
    echo "❌ Update cancelled"
    cd "$REPO_ROOT"
    exit 1
fi

