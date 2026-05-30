#!/bin/bash
# install.sh - Install BXZ on Linux/macOS

echo "=========================================="
echo "🚀 Installing BXZ Language"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.6+"
    exit 1
fi

# Install via pip
echo "📦 Installing Python package..."
python3 -m pip install -e .

# Create executable
echo "🔧 Creating executable..."
cat > bxz << 'EOF'
#!/bin/bash
python3 "$(dirname "$0")/bxz.py" "$@"
EOF
chmod +x bxz

# Copy to /usr/local/bin
echo "📋 Copying to /usr/local/bin..."
sudo cp bxz /usr/local/bin/

# Create desktop shortcut
echo "🖥️  Creating desktop shortcut..."
cat > ~/Desktop/BXZ-REPL.command << EOF
#!/bin/bash
cd "$(pwd)"
python3 bxz.py -i
EOF
chmod +x ~/Desktop/BXZ-REPL.command

echo "=========================================="
echo "✅ Installation complete!"
echo ""
echo "Usage: bxz <file.bxz>"
echo "       bxz -i"
echo "=========================================="