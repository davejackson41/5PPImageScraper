#!/bin/bash

# Script to automate Git commits and pushes

echo "🚀 Starting Git Commit Process"

# Ask for a commit message
echo "Enter commit message:"
read commit_msg

# Ensure a message is provided
if [ -z "$commit_msg" ]; then
    echo "❌ Error: Commit message cannot be empty!"
    exit 1
fi

# Add all changes to Git
git add .

# Commit with the user-provided message
git commit -m "$commit_msg"

# Push changes to GitHub
git push origin main

echo "✅ Changes committed & pushed to GitHub."
