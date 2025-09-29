# PowerShell script to remove sensitive file from git history
Set-Location "C:\Users\omnis\OneDrive\Documents\PP5\Avagen_v1"

Write-Host "Removing gcs-key.json from entire git history..."

# Remove the file from git history completely
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch gcs-key.json' --prune-empty --tag-name-filter cat -- --all

Write-Host "Force pushing to GitHub..."
git push origin main --force

Write-Host "Done! The sensitive file has been removed from git history."
