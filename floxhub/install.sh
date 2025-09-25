#!/bin/bash
# FloxAI FloxHub Installation Script
# This script installs FloxAI for different usage modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

FLOXAI_VERSION="1.0.0"

echo -e "${BLUE}🚀 FloxAI FloxHub Installation${NC}"
echo "Version: $FLOXAI_VERSION"
echo "=================================="
echo ""

# Function to show help
show_help() {
    cat << EOF
FloxAI Installation Options:

1. Layer Mode (Recommended)
   Add FloxAI as a layer to your existing Flox environment
   Usage: floxai chat, floxai analyze, floxai layer

2. Standalone Mode  
   Create a dedicated FloxAI environment
   Usage: floxybot, floxai-demo, floxai-setup

3. Service Mode
   Run FloxAI as a service with full web interface
   Usage: floxai serve

Examples:
  ./install.sh layer          # Install as layer
  ./install.sh standalone     # Install standalone
  ./install.sh service        # Install service mode
  ./install.sh help           # Show this help

EOF
}

# Function to install layer mode
install_layer() {
    echo -e "${GREEN}🔧 Installing FloxAI Layer Mode...${NC}"
    echo ""
    
    # Check if we're in a Flox environment
    if [ -z "$FLOX_ENV" ]; then
        echo -e "${YELLOW}⚠️  Not in a Flox environment${NC}"
        echo "   Creating new Flox environment for FloxAI layer..."
        flox init
    fi
    
    echo "📦 Installing FloxAI packages..."
    
    # Install core packages
    flox install python313 nodejs git curl sqlite jq tree
    
    # Install Python packages
    flox install python313Packages.fastapi python313Packages.uvicorn
    flox install python313Packages.sqlalchemy python313Packages.pydantic
    flox install python313Packages.requests python313Packages.beautifulsoup4
    flox install python313Packages.anthropic python313Packages.pandas
    flox install python313Packages.numpy python313Packages.python-multipart
    flox install python313Packages.pydantic-settings python313Packages.gitpython
    flox install python313Packages.toml python313Packages.pyyaml
    flox install python313Packages.python-dotenv python313Packages.structlog
    flox install python313Packages.chromadb python313Packages.sentence-transformers
    flox install python313Packages.tiktoken
    
    # Install Node.js packages
    flox install nodePackages.npm
    
    echo ""
    echo -e "${GREEN}✅ FloxAI Layer Mode installed successfully!${NC}"
    echo ""
    echo "🎯 Available Commands:"
    echo "   floxai chat <message>    - Ask FloxAI questions"
    echo "   floxai analyze           - Analyze your environment"
    echo "   floxai suggest           - Get improvement suggestions"
    echo "   floxai layer             - Start full layer interface"
    echo "   floxai serve             - Start as service"
    echo ""
    echo "💡 This demonstrates Flox's layer composition capabilities!"
}

# Function to install standalone mode
install_standalone() {
    echo -e "${GREEN}🔧 Installing FloxAI Standalone Mode...${NC}"
    echo ""
    
    # Create FloxAI environment
    if [ ! -d ".flox" ]; then
        echo "📦 Creating FloxAI environment..."
        flox init
    fi
    
    # Install all packages
    flox install python313 nodejs git curl sqlite jq tree
    flox install python313Packages.fastapi python313Packages.uvicorn
    flox install python313Packages.sqlalchemy python313Packages.pydantic
    flox install python313Packages.requests python313Packages.beautifulsoup4
    flox install python313Packages.anthropic python313Packages.pandas
    flox install python313Packages.numpy python313Packages.python-multipart
    flox install python313Packages.pydantic-settings python313Packages.gitpython
    flox install python313Packages.toml python313Packages.pyyaml
    flox install python313Packages.python-dotenv python313Packages.structlog
    flox install python313Packages.chromadb python313Packages.sentence-transformers
    flox install python313Packages.tiktoken
    flox install nodePackages.npm
    
    # Set up environment variables
    echo "🔧 Setting up environment variables..."
    cat >> .flox/env/manifest.toml << 'EOF'

[vars]
FLOXAI_VERSION = "1.0.0"
FLOXAI_API_PORT = "8000"
FLOXAI_UI_PORT = "3000"
FLOXAI_DB_PATH = "$FLOX_ENV_PROJECT/data/floxai.db"
FLOXAI_VECTOR_DB_PATH = "$FLOX_ENV_PROJECT/data/vector_db"
FLOXAI_DOCS_PATH = "$FLOX_ENV_PROJECT/data/flox_docs"
FLOXAI_PROJECT_ROOT = "$FLOX_ENV_PROJECT"
FLOXAI_DEV_MODE = "false"
FLOXAI_LOG_LEVEL = "INFO"
PYTHONPATH = "$FLOX_ENV_PROJECT/backend:$PYTHONPATH"

[profile]
common = '''
export PATH="$FLOX_ENV_PROJECT:$PATH"
alias floxai="echo Starting FloxAI... && $FLOX_ENV_PROJECT/floxai-start"
alias start-floxai="echo Starting FloxAI... && $FLOX_ENV_PROJECT/floxai-start"
'''
EOF
    
    echo ""
    echo -e "${GREEN}✅ FloxAI Standalone Mode installed successfully!${NC}"
    echo ""
    echo "🎯 Available Commands:"
    echo "   floxybot                 - Start standalone mode"
    echo "   floxai-setup             - Interactive setup"
    echo "   floxai-demo              - Run capabilities demo"
    echo "   floxai                   - Start complete system"
    echo ""
    echo "💡 Next: Run 'floxai-setup' to configure Claude API key"
}

# Function to install service mode
install_service() {
    echo -e "${GREEN}🔧 Installing FloxAI Service Mode...${NC}"
    echo ""
    
    # Install layer mode first
    install_layer
    
    echo ""
    echo -e "${GREEN}✅ FloxAI Service Mode installed successfully!${NC}"
    echo ""
    echo "🎯 Available Commands:"
    echo "   floxai serve             - Start as service"
    echo "   floxai layer             - Start layer interface"
    echo "   floxai chat <message>    - Quick chat"
    echo ""
    echo "💡 Service mode provides full web interface at http://localhost:3000"
}

# Main installation logic
case "${1:-help}" in
    "layer")
        install_layer
        ;;
    "standalone")
        install_standalone
        ;;
    "service")
        install_service
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown installation mode: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}🎉 FloxAI Installation Complete!${NC}"
echo "   This demonstrates Flox's power for reproducible development environments!"
echo ""
echo "📚 Learn more: https://flox.dev/docs"
echo "🐛 Report issues: https://github.com/flox/floxai/issues"
