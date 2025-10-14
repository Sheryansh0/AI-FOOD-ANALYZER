# GitHub Push Instructions

## ✅ Git Repository Initialized Successfully!

Your code has been committed locally. Now follow these steps to push to GitHub:

## Step 1: Create a New Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `ai-food-analyzer` (or your preferred name)
3. Description: "AI-powered food analyzer with local PyTorch models and Gemini API integration"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have them)
6. Click **"Create repository"**

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
cd "d:\chandramouli project"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Replace the Placeholders

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with your repository name (e.g., `ai-food-analyzer`)

## Example:

If your username is `john` and repo is `ai-food-analyzer`:

```powershell
cd "d:\chandramouli project"
git remote add origin https://github.com/john/ai-food-analyzer.git
git branch -M main
git push -u origin main
```

## ⚠️ Important: Before Pushing

Your `.env` file with the API key is already in `.gitignore`, so it won't be pushed to GitHub. ✅

**Files that will be pushed:**
- ✅ All source code
- ✅ README and documentation
- ✅ Requirements and configs
- ✅ Frontend and backend code
- ❌ .env (protected by .gitignore)
- ❌ venv/ (protected by .gitignore)
- ❌ node_modules/ (protected by .gitignore)
- ❌ Model files (.pth files - too large, add separately if needed)

## Step 4: Verify .gitignore

Your `.gitignore` already includes:
```
venv/
__pycache__/
*.pyc
.env
node_modules/
dist/
build/
.DS_Store
uploads/
*.log
```

## Step 5: Handle Large Model Files

Your PyTorch models (*.pth files) are large. Options:

**Option A: Don't push them (recommended)**
Add to `.gitignore`:
```
*.pth
```

**Option B: Use Git LFS (Large File Storage)**
```powershell
git lfs install
git lfs track "*.pth"
git add .gitattributes
git add *.pth
git commit -m "Add model files"
git push
```

**Option C: Upload to cloud storage**
Upload models to Google Drive/Dropbox and add download link in README

## Quick Command Sequence

1. Create repo on GitHub first
2. Then run:

```powershell
cd "d:\chandramouli project"

# Add *.pth to gitignore (recommended)
Add-Content .gitignore "`n*.pth"
git add .gitignore
git commit -m "Ignore model files"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## 🎉 After Pushing

Your repository will be live at:
`https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`

## Common Issues:

**"remote origin already exists":**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

**Authentication required:**
- Use Personal Access Token instead of password
- Generate at: https://github.com/settings/tokens

**Permission denied:**
- Check if you have write access to the repository
- Verify you're logged in to the correct GitHub account

---

**Current Status:**
✅ Git initialized
✅ Files committed locally (22 files, 5468 insertions)
✅ Ready to push to GitHub

**Next:** Create GitHub repository and run the push commands!
