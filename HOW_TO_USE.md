# 🚀 How to Use Git Conflict Resolver (gcr)

If you've ever tried to merge code and seen scary messages like `CONFLICT (content): Merge conflict in file.py`, don't worry! This tool was built to help you fix those errors easily and safely.

This guide will walk you through everything, even if you are a total beginner.

---

## 1. What is a "Merge Conflict"?
Imagine you and a friend are both writing a story in the same file. 
* You change the first line to: *"It was a sunny day."*
* Your friend changes the same line to: *"It was a rainy day."*

When you try to combine your work, Git gets confused and doesn't know which one to keep. It stops everything and puts "Conflict Markers" in your file that look like this:

```python
<<<<<<< HEAD
It was a sunny day.
=======
It was a rainy day.
>>>>>>> friend-branch
```

**Our tool (`gcr`) lets you pick the winner with just one click.**

---

## 2. Setting Up
Before you start, make sure you have installed the tool globally (follow the steps in `README.md`). Once installed, you can just type `gcr` in your terminal.

---

## 3. The Three Ways to Use the Tool

### A. Fix Everything at Once (The "Magic" Way)
If you have a lot of files with errors, run this:
```bash
gcr --all
```
The tool will find every broken file in your project and walk you through them one by one.

### B. Fix One Specific File
If you only want to fix one file:
```bash
gcr your_file_name.py
```

### C. The "Safe" Way (Dry Run)
If you are nervous and want to save the result to a **new** file instead of overwriting your current one:
```bash
gcr your_file_name.py --output resolved_version.py
```

---

## 4. How the Interactive Screen Works
When you run the tool, you will see two boxes:
1. **🟢 HEAD (Current)**: This is the code you already had on your computer.
2. **🔴 INCOMING**: This is the new code someone else wrote that is trying to get in.

### Your Choices:
Type a number and press Enter:
* **Press `1`**: Keep your code (HEAD) and throw away the new code.
* **Press `2`**: Keep the new code (Incoming) and throw away yours.
* **Press `3`**: Keep BOTH! It will put your code first, then the new code right after it.
* **Press `4`**: Skip it for now.
* **Press `5`**: **The AI Helper.** (See below).

---

## 5. Using the AI Helper (Smart Mode) 🤖
If the code looks too complicated and you don't know which one to pick, let the AI decide for you!

1. Select **Option `5`** during the resolution.
2. The tool will ask Gemini or Groq to read the code.
3. It will explain exactly what changed and suggest the best way to merge them.
4. You can then choose to accept the AI's suggestion.

*Note: You will need an API key for this. If you don't have one, the tool will ask you to enter it the first time you try to use this feature.*

---

## 6. Finishing the Job
After you have resolved the conflicts in a file, the tool will show you a "Preview." If it looks good, type `y` to save.

**CRITICAL STEP:** Once you save the file, the conflicts are fixed on your computer, but Git doesn't know that yet. You must run these two commands in your project folder to finish:

```bash
git add .
git commit -m "Fixed merge conflicts using gcr"
```

---

## Summary of Tips
* **Don't Panic**: No changes are permanent until you type `y` at the very end.
* **Syntax Highlighting**: The tool automatically colors your code (Python, JS, C++, etc.) to make it easier to read.
* **Backdoor**: If you make a mistake, type `back` to re-choose your resolution for that block.
* **Quit**: If you get overwhelmed, press `Ctrl+C` to cancel everything. No files will be changed.

**Happy merging!**
