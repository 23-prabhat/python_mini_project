# Setup Instructions for Git Conflict Resolver (gcr)

To use the `gcr` command from anywhere in your terminal, follow these steps to add the project to your system's PATH.

## Automatic Setup (Windows)

1. Open **PowerShell** or **Command Prompt** as **Administrator**.
2. Navigate to the project directory:
   ```powershell
   cd "C:\Users\Akhilesh\Downloads\Projects_Organised\python\git-conflict-resolver"
   ```
3. Run the setup script:
   ```powershell
   .\setup.bat
   ```
4. **Restart your terminal** for the changes to take effect.

## Manual Setup (Windows)

1. Press the **Windows Key** and type **"Environment Variables"**.
2. Select **Edit the system environment variables**.
3. Click the **Environment Variables** button.
4. Under **User variables**, select **Path** and click **Edit**.
5. Click **New** and paste the following path:
   `C:\Users\Akhilesh\Downloads\Projects_Organised\python\git-conflict-resolver`
6. Click **OK** on all windows.
7. **Restart your terminal**.

## Verification

Open a new terminal and run:
```powershell
gcr --all
```
If the application banner appears, the setup was successful.
