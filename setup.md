# GCR Setup Guide
**(most important two things to make project work)**
### 1. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```
#### B. Global Command (PATH)
To use the `gcr` command from any folder, add the project path to your **System PATH**:
- **Path:** `C:\Users\YourName\...\...\...\git-conflict-resolver`

**How to add it:**
1. Search for "Edit the system environment variables" in Windows.
2. Click **Environment Variables**.
3. Under **User variables**, edit **Path**.
4. Click **New** and paste the project path above.





### 2. Environment Variables
You need to set two variables for full functionality:
also you can use your api for soecific call you want on time you are on CLI

#### A. Groq API Key
```powershell
# Windows
$env:GROQ_API_KEY="your_api_key_here"
```

### 3. Usage
Now you can run the tool from anywhere using:
```bash
# Resolve all conflicts in current repo
gcr --all

# Resolve a specific file
gcr path/to/file.py
```
