@echo off
echo Removing sensitive file from git history...
cd /d "C:\Users\omnis\OneDrive\Documents\PP5\Avagen_v1"

echo Step 1: Removing gcs-key.json from git history...
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch gcs-key.json" --prune-empty --tag-name-filter cat -- --all

echo Step 2: Cleaning up git references...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo Step 3: Force pushing to GitHub...
git push origin main --force

echo Done! The sensitive file has been removed from git history.
pause
