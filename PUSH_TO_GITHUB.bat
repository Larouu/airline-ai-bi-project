@echo off
REM Quick script to push to GitHub - Edit the variables below!

REM ============== EDIT THESE VARIABLES ==============
set GITHUB_USERNAME=YOUR_USERNAME
set REPO_NAME=airline-ai-bi-project
REM ==================================================

echo.
echo ======================================================
echo Pushing to GitHub...
echo ======================================================
echo.
echo Repository: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.

REM Set remote URL
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

REM Rename branch to main
git branch -M main

REM Push to GitHub
echo Pushing files to GitHub (this may take a moment)...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================
    echo SUCCESS! Your repository is now on GitHub!
    echo ======================================================
    echo.
    echo Your GitHub URL:
    echo https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo.
) else (
    echo.
    echo ERROR: Push failed. Check your credentials and try again.
    echo.
)

pause
