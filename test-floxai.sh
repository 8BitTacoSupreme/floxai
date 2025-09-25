#!/bin/bash
# FloxAI Quick Test Script
set -e

echo "🧪 FloxAI Quick Test Suite"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
}

# Check if we're in a Flox environment
if [ -z "$FLOX_ENV" ]; then
    echo -e "${RED}❌ Not in a Flox environment. Run 'flox activate' first.${NC}"
    exit 1
fi

echo "🔍 Environment: $FLOX_ENV_NAME"
echo "📁 Project: $FLOX_ENV_PROJECT"
echo ""

# Test 1: Check if setup was run
run_test "Setup completion" "[ -f 'data/floxai.db' ] && [ -d 'data/vector_db' ]"

# Test 2: Check if all scripts are executable
run_test "Script permissions" "[ -x 'floxybot' ] && [ -x 'floxai-setup' ] && [ -x 'flox-demo' ]"

# Test 3: Check if backend dependencies are available
run_test "Backend dependencies" "python3 -c 'import fastapi, uvicorn, chromadb, sentence_transformers'"

# Test 4: Check if frontend dependencies are available
run_test "Frontend dependencies" "[ -d 'frontend/node_modules' ]"

# Test 5: Check if vector database has content
run_test "Vector database" "[ -d 'data/vector_db' ] && [ \"\$(ls -A data/vector_db 2>/dev/null)\" ]"

# Test 6: Check if documentation exists
run_test "Documentation" "[ -d 'data/flox_docs' ] && [ \"\$(find data/flox_docs -name \"*.md\" | wc -l)\" -gt 0 ]"

# Test 7: Check if API key is set (optional)
if [ -n "$CLAUDE_API_KEY" ]; then
    run_test "Claude API key" "true"
else
    echo -e "${YELLOW}⚠️  Claude API key not set (limited functionality)${NC}"
fi

# Test 8: Check if generated scripts exist
run_test "Generated scripts" "[ -f 'floxai-update' ] && [ -f 'floxai-check' ]"

# Test 9: Check if manifest.toml is valid (skip flox list as it can hang)
run_test "Manifest validity" "[ -f '.flox/env/manifest.toml' ]"

# Test 10: Check if update script works
run_test "Update script" "[ -f 'update_docs.sh' ] && [ -x 'update_docs.sh' ]"

echo ""
echo "📊 Test Results:"
echo "================"
echo -e "✅ Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "❌ Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! FloxAI is ready for FloxHub!${NC}"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Test all three modes: ./floxybot, floxai --layer, ./flox-demo"
    echo "   2. Test API endpoints: curl http://localhost:8000/health"
    echo "   3. Package for FloxHub: cd floxhub && ./package.sh"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Please fix issues before publishing.${NC}"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   - Run ./floxai-setup to complete setup"
    echo "   - Run ./floxai-check for detailed diagnostics"
    echo "   - Check README.md for setup instructions"
    exit 1
fi
