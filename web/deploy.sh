#!/usr/bin/env bash

# This script builds the project and pushes the 'dist' folder to the 'gh-pages' branch.
# Usage: ./deploy.sh

# 1. Build the project
echo "Building project..."
npm run build

# 2. Navigate to the build output
cd dist

# 3. Initialize git in dist (if not already)
git init
git add -A
git commit -m "Deploy to GitHub Pages"

# 4. Prompt for the repository URL if not provided
# Replace <YOUR_REPO_URL> with your actual repository URL
# git push -f <YOUR_REPO_URL> master:gh-pages

echo "----------------------------------------------------"
echo "Build complete! The 'dist' folder is ready."
echo "To deploy to GitHub Pages, run:"
echo "cd dist"
echo "git init"
echo "git remote add origin <YOUR_GITHUB_REPO_URL>"
echo "git push -f origin master:gh-pages"
echo "----------------------------------------------------"
