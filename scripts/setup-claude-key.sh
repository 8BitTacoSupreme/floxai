#!/bin/bash
# FloxAI Claude API Key Setup
# Interactive prompt and session management for Claude API key

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Session key storage (temporary, not committed to git)
SESSION_KEY_FILE="$PROJECT_ROOT/.claude-session-key"
ENV_FILE="$PROJECT_ROOT/.env.local"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${BLUE}"
    echo "  🔐 FloxAI Claude API Key Setup"
    echo "  ═══════════════════════════════"
    echo -e "${NC}"
}

check_existing_key() {
    # Check if key is already set in environment
    if [ -n "$CLAUDE_API_KEY" ]; then
        echo -e "${GREEN}✅ Claude API key is already set in environment${NC}"
        return 0
    fi

    # Check session file
    if [ -f "$SESSION_KEY_FILE" ]; then
        echo -e "${GREEN}✅ Using Claude API key from current session${NC}"
        export CLAUDE_API_KEY="$(cat "$SESSION_KEY_FILE")"
        return 0
    fi

    # Check .env.local file
    if [ -f "$ENV_FILE" ] && grep -q "CLAUDE_API_KEY=" "$ENV_FILE"; then
        echo -e "${YELLOW}📁 Found saved Claude API key in .env.local${NC}"
        echo -n "Use saved key? (y/n): "
        read -r use_saved
        if [ "$use_saved" = "y" ] || [ "$use_saved" = "Y" ]; then
            # Load from .env.local
            export $(grep "CLAUDE_API_KEY=" "$ENV_FILE" | xargs)
            # Save to session
            echo "$CLAUDE_API_KEY" > "$SESSION_KEY_FILE"
            chmod 600 "$SESSION_KEY_FILE"
            echo -e "${GREEN}✅ Loaded Claude API key from saved file${NC}"
            return 0
        fi
    fi

    return 1
}

prompt_for_key() {
    echo -e "${YELLOW}🔑 Claude API Key Required${NC}"
    echo ""
    echo "FloxAI needs your Claude API key to provide AI-powered assistance."
    echo ""
    echo -e "${BLUE}To get your API key:${NC}"
    echo "1. Visit: https://console.anthropic.com/settings/keys"
    echo "2. Create a new API key"
    echo "3. Copy the key (starts with 'sk-ant-api03-')"
    echo ""

    # Prompt for key with hidden input
    echo -n "🔐 Enter your Claude API key: "
    read -r -s api_key
    echo ""

    # Validate key format
    if [[ ! "$api_key" =~ ^sk-ant-api03-.* ]]; then
        echo -e "${RED}❌ Invalid API key format. Key should start with 'sk-ant-api03-'${NC}"
        return 1
    fi

    # Test the key
    echo -e "${BLUE}🧪 Testing API key...${NC}"
    if ! test_api_key "$api_key"; then
        echo -e "${RED}❌ API key test failed. Please check your key and try again.${NC}"
        return 1
    fi

    # Save to session
    echo "$api_key" > "$SESSION_KEY_FILE"
    chmod 600 "$SESSION_KEY_FILE"
    export CLAUDE_API_KEY="$api_key"

    echo -e "${GREEN}✅ Claude API key validated and saved for this session${NC}"

    # Ask about persistent storage
    echo ""
    echo -e "${YELLOW}💾 Save key for future sessions?${NC}"
    echo "This will store the key in .env.local (excluded from git)"
    echo -n "Save key? (y/n): "
    read -r save_key

    if [ "$save_key" = "y" ] || [ "$save_key" = "Y" ]; then
        # Remove any existing CLAUDE_API_KEY line
        if [ -f "$ENV_FILE" ]; then
            grep -v "CLAUDE_API_KEY=" "$ENV_FILE" > "$ENV_FILE.tmp" && mv "$ENV_FILE.tmp" "$ENV_FILE"
        fi
        # Add new key
        echo "CLAUDE_API_KEY=$api_key" >> "$ENV_FILE"
        chmod 600 "$ENV_FILE"
        echo -e "${GREEN}✅ API key saved to .env.local${NC}"
    fi

    return 0
}

test_api_key() {
    local key="$1"
    # Simple test - try to make a minimal API call
    local response
    response=$(curl -s -w "%{http_code}" \
        -H "x-api-key: $key" \
        -H "Content-Type: application/json" \
        -H "anthropic-version: 2023-06-01" \
        -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}' \
        https://api.anthropic.com/v1/messages)

    local http_code="${response: -3}"
    if [ "$http_code" = "200" ]; then
        return 0
    else
        return 1
    fi
}

setup_cleanup_hook() {
    # Set up cleanup on exit
    cleanup() {
        echo ""
        echo -e "${YELLOW}🛑 FloxAI shutting down...${NC}"

        if [ -f "$SESSION_KEY_FILE" ]; then
            if [ ! -f "$ENV_FILE" ] || ! grep -q "CLAUDE_API_KEY=" "$ENV_FILE"; then
                echo -n "💾 Save Claude API key for next session? (y/n): "
                read -r save_on_exit
                if [ "$save_on_exit" = "y" ] || [ "$save_on_exit" = "Y" ]; then
                    local session_key="$(cat "$SESSION_KEY_FILE")"
                    # Remove any existing CLAUDE_API_KEY line
                    if [ -f "$ENV_FILE" ]; then
                        grep -v "CLAUDE_API_KEY=" "$ENV_FILE" > "$ENV_FILE.tmp" && mv "$ENV_FILE.tmp" "$ENV_FILE"
                    fi
                    echo "CLAUDE_API_KEY=$session_key" >> "$ENV_FILE"
                    chmod 600 "$ENV_FILE"
                    echo -e "${GREEN}✅ API key saved for next session${NC}"
                fi
            fi

            # Clean up session file
            rm -f "$SESSION_KEY_FILE"
        fi

        echo -e "${BLUE}👋 Thanks for using FloxAI!${NC}"
    }

    trap cleanup EXIT SIGINT SIGTERM
}

main() {
    print_banner

    # Check if we already have a key
    if check_existing_key; then
        return 0
    fi

    # Prompt for new key
    if ! prompt_for_key; then
        echo -e "${RED}❌ Failed to set up Claude API key${NC}"
        return 1
    fi

    # Set up cleanup for when FloxAI shuts down
    setup_cleanup_hook

    return 0
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi