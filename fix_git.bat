@echo off
cd /d "C:\Users\omnis\OneDrive\Documents\PP5\Avagen_v1"
git status
git add .
git commit -m "security: Remove gcs-key.json from tracking

- Remove sensitive Google Cloud credentials from git history
- File remains in .gitignore for local development
- Prevents credential exposure in repository"
git push origin main
