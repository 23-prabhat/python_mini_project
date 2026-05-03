#!/bin/bash

# Auto-detect the absolute path to the directory where this script is located
TOOL_DIR=$( cd "$( dirname "$0" )" && pwd )
BIN_PATH="/usr/local/bin/gcr"

echo "Setting up Git Conflict Resolver (gcr) for Mac/Linux..."

# 1. Create the shell script at /usr/local/bin/gcr
# Using sudo to ensure we have permissions to write to /usr/local/bin
cat <<EOF | sudo tee "$BIN_PATH" > /dev/null
#!/bin/bash
python3 "$TOOL_DIR/main.py" "\$@"
EOF

# 2. Make it executable
sudo chmod +x "$BIN_PATH"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║ SUCCESS: Git Conflict Resolver (gcr) is installed!  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "How to use:"
echo "  1. Navigate to any Git repository with merge conflicts."
echo "  2. Run 'gcr --all' to resolve everything."
echo "  3. Run 'gcr filename' to resolve a specific file."
echo ""
echo "Installation Path: $BIN_PATH"
echo "Script Source: $TOOL_DIR/main.py"
echo ""
