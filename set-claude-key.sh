#!/bin/bash
# Set Claude API key in Flox environment

if [ -z "$1" ]; then
    echo "Usage: ./set-claude-key.sh YOUR_CLAUDE_API_KEY"
    echo ""
    echo "Example:"
    echo "  ./set-claude-key.sh sk-ant-api03-XMnUkOO7AwoicDlGFC6qWm4FPr3RJ5k6YhCQIbE3RM1I9LcrnojuXILGHV9r6epRRjl8NOc5IqcMju-pbUA-wn01SwAAe"
    exit 1
fi

export CLAUDE_API_KEY="$1"
echo "✅ Claude API key set for current session"
echo "   Key: ${CLAUDE_API_KEY:0:20}..."
echo ""
echo "💡 To make this permanent, add to your manifest.toml:"
echo "   [vars]"
echo "   CLAUDE_API_KEY = \"$1\""
echo ""
echo "🚀 Now run: floxybotdev"
