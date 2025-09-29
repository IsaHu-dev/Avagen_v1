# PowerShell script to push changes to GitHub
Set-Location "C:\Users\omnis\OneDrive\Documents\PP5\Avagen_v1"

Write-Host "Adding all changes..."
git add .

Write-Host "Committing changes..."
git commit -m "security: Remove gcs-key.json from tracking

- Remove sensitive Google Cloud credentials from git history
- File remains in .gitignore for local development
- Prevents credential exposure in repository"

Write-Host "Pushing to GitHub..."
git push origin main

Write-Host "Done!"
