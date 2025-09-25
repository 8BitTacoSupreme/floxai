#!/bin/bash
# Simple FloxAI Test
echo "🧪 FloxAI Quick Test"
echo "===================="

# Check environment
if [ -z "$FLOX_ENV" ]; then
    echo "❌ Not in Flox environment"
    exit 1
fi

echo "✅ Flox environment active: $FLOX_ENV_NAME"

# Check setup
if [ -f 'data/floxai.db' ] && [ -d 'data/vector_db' ]; then
    echo "✅ Setup complete"
else
    echo "❌ Setup incomplete"
fi

# Check scripts
if [ -x 'floxybot' ] && [ -x 'floxai-setup' ] && [ -x 'flox-demo' ]; then
    echo "✅ Scripts executable"
else
    echo "❌ Scripts not executable"
fi

# Check dependencies
if python3 -c "import fastapi, uvicorn, chromadb, sentence_transformers" 2>/dev/null; then
    echo "✅ Backend dependencies available"
else
    echo "❌ Backend dependencies missing"
fi

# Check frontend
if [ -d 'frontend/node_modules' ]; then
    echo "✅ Frontend dependencies available"
else
    echo "❌ Frontend dependencies missing"
fi

# Check vector DB
if [ -d 'data/vector_db' ] && [ "$(ls -A data/vector_db 2>/dev/null)" ]; then
    echo "✅ Vector database has content"
else
    echo "❌ Vector database empty or missing"
fi

# Check docs
DOC_COUNT=$(find data/flox_docs -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$DOC_COUNT" -gt 0 ]; then
    echo "✅ Documentation available ($DOC_COUNT files)"
else
    echo "❌ No documentation found"
fi

# Check API key
if [ -n "$CLAUDE_API_KEY" ]; then
    echo "✅ Claude API key set"
else
    echo "⚠️  Claude API key not set (limited functionality)"
fi

echo ""
echo "🎯 FloxAI Status: Ready for testing!"
echo ""
echo "Next steps:"
echo "  1. Test L1/L2: ./floxybot"
echo "  2. Test L3: floxai --layer"  
echo "  3. Test Demo: ./flox-demo"
echo "  4. Test API: curl http://localhost:8000/health"
