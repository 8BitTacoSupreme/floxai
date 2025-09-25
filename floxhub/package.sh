#!/bin/bash
# FloxAI FloxHub Packaging Script
set -e

echo "📦 Packaging FloxAI for FloxHub"
echo "==============================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PACKAGE_DIR="$SCRIPT_DIR/package"

# Clean and create package directory
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

echo "📁 Copying core files..."

# Copy essential files for FloxHub package
cp "$PROJECT_ROOT/.flox/env/manifest.toml" "$PACKAGE_DIR/"
cp "$PROJECT_ROOT/README.md" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/floxfile.toml" "$PACKAGE_DIR/"

# Copy scripts
echo "📜 Copying scripts..."
mkdir -p "$PACKAGE_DIR/bin"
cp "$SCRIPT_DIR/bin/floxai" "$PACKAGE_DIR/bin/"
cp "$PROJECT_ROOT/floxai-setup" "$PACKAGE_DIR/bin/"
cp "$PROJECT_ROOT/floxybot" "$PACKAGE_DIR/bin/"
cp "$PROJECT_ROOT/floxybotdev" "$PACKAGE_DIR/bin/"
cp "$PROJECT_ROOT/floxai-demo" "$PACKAGE_DIR/bin/"

# Copy backend (essential for service mode)
echo "🔧 Copying backend..."
cp -r "$PROJECT_ROOT/backend" "$PACKAGE_DIR/"

# Copy frontend build (for standalone mode)
echo "🌐 Building and copying frontend..."
cd "$PROJECT_ROOT/frontend"
npm run build
cp -r dist "$PACKAGE_DIR/frontend-dist"
cd "$PROJECT_ROOT"

# Copy documentation update script
echo "📚 Copying documentation tools..."
cp "$PROJECT_ROOT/update_docs.sh" "$PACKAGE_DIR/bin/"

# Create package metadata
echo "📋 Creating package metadata..."
cat > "$PACKAGE_DIR/FLOXAI_PACKAGE_INFO" << EOF
FloxAI Package Information
==========================

Version: 1.0.0
Built: $(date)
Modes: standalone, layer, service

Files included:
- bin/floxai         - Main CLI interface
- bin/floxybot       - Standalone mode service
- bin/floxybotdev    - Development mode service  
- bin/floxai-setup   - Interactive setup
- bin/floxai-demo    - Capabilities demo
- backend/           - Python FastAPI backend
- frontend-dist/     - React frontend (built)
- manifest.toml      - Flox environment definition

Usage:
  Layer Mode:    flox install floxai --layer
  Standalone:    flox install floxai && flox activate floxai-env
  Service:       floxai serve --port 8080

Documentation: https://flox.dev/docs/floxai
EOF

# Create installation script
echo "⚙️  Creating installation script..."
cat > "$PACKAGE_DIR/install.sh" << 'EOF'
#!/bin/bash
# FloxAI Installation Script for FloxHub

set -e

INSTALL_DIR="${FLOX_ENV_PROJECT:-$HOME/.flox/floxai}"

echo "🌟 Installing FloxAI - The Flox Development Co-pilot"
echo "===================================================="

# Create necessary directories
mkdir -p "$INSTALL_DIR/data/vector_db" "$INSTALL_DIR/data/flox_docs"

# Install Python dependencies if in Flox environment
if [ -n "$FLOX_ENV" ]; then
    echo "📦 Installing Python dependencies in Flox environment..."
    python3 -m pip install -r backend/requirements.txt
    echo "✅ Dependencies installed"
fi

# Set up basic configuration
if [ ! -f "$INSTALL_DIR/data/floxai.db" ]; then
    echo "💾 Initializing database..."
    cd backend && python3 -c "
import sys
sys.path.insert(0, '.')
from app.db.database import init_db
init_db()
print('Database initialized')
    " && cd ..
fi

echo ""
echo "✅ FloxAI installation complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Set Claude API key: export CLAUDE_API_KEY=your_key"
echo "   2. For layer mode: floxai chat 'Hello FloxAI!'"
echo "   3. For service mode: floxai serve"
echo ""
EOF

chmod +x "$PACKAGE_DIR/install.sh"

# Create archive
echo "📦 Creating package archive..."
cd "$SCRIPT_DIR"
tar -czf "floxai-1.0.0.tar.gz" -C package .

echo ""
echo "✅ FloxAI package created successfully!"
echo ""
echo "📁 Package contents:"
ls -la "$PACKAGE_DIR"
echo ""
echo "📦 Archive: $SCRIPT_DIR/floxai-1.0.0.tar.gz"
echo "📏 Size: $(du -h "$SCRIPT_DIR/floxai-1.0.0.tar.gz" | cut -f1)"
echo ""
echo "🚀 Ready for FloxHub publishing!"
