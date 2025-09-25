# FloxAI Local Testing Checklist

## 🧪 Pre-FloxHub Testing Steps

### 1. **Environment Setup Test**
```bash
# Clean start - exit any existing Flox environment
exit

# Clone fresh copy (simulate new user)
cd /tmp
git clone <your-repo-url> floxai-test
cd floxai-test

# Initialize Flox environment
flox init
flox activate

# Run setup
./floxai-setup
```

**✅ Expected Results:**
- Setup completes without errors
- All dependencies install via `flox install`
- Vector database is created
- `floxai-check` shows all green checkmarks

### 2. **L1/L2 Support Mode Test**
```bash
# Test standalone mode
./floxybot
```

**✅ Expected Results:**
- Backend starts on port 8000
- Frontend starts on port 4173 (production build)
- Health check: http://localhost:8000/health
- Can ask questions about Flox/Nix
- Vector search works (semantic responses)

### 3. **L3 Layer Mode Test**
```bash
# Test layer mode
floxai --layer
```

**✅ Expected Results:**
- Environment analysis works
- Manifest validation suggestions
- Context-aware responses
- Full web interface available

### 4. **Interactive Demo Test**
```bash
# Test learning journey
./flox-demo
```

**✅ Expected Results:**
- Interactive menu works
- All 4 learning paths function
- Can complete a full learning journey
- No errors during execution

### 5. **Update System Test**
```bash
# Test manual update
./floxai-update

# Test automated update (simulate 7 days)
touch data/.last_update
# Edit timestamp to be 8 days ago
echo "0" > data/.last_update
flox activate  # Should trigger background update
```

**✅ Expected Results:**
- Manual update works
- Automated update triggers on activation
- Vector database updates
- No blocking during activation

### 6. **FloxHub Package Test**
```bash
# Test packaging
cd floxhub
./package.sh

# Test installation
./install.sh --help
```

**✅ Expected Results:**
- Package script creates valid FloxHub package
- Install script shows help
- All binaries are executable
- Floxfile.toml is valid

### 7. **API Endpoints Test**
```bash
# Start FloxAI
./floxybot

# Test endpoints (in another terminal)
curl http://localhost:8000/health
curl http://localhost:8000/docs
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Flox?"}'
```

**✅ Expected Results:**
- Health endpoint returns status
- API docs load correctly
- Chat endpoint returns AI response
- All endpoints respond within 5 seconds

### 8. **Error Handling Test**
```bash
# Test without Claude API key
unset CLAUDE_API_KEY
./floxybot
# Should show warning but still start

# Test with invalid API key
export CLAUDE_API_KEY="invalid-key"
./floxybot
# Should handle gracefully

# Test with missing data
rm -rf data/
./floxybot
# Should recreate data or show helpful error
```

**✅ Expected Results:**
- Graceful degradation without API key
- Helpful error messages
- System doesn't crash
- Recovery instructions provided

### 9. **Performance Test**
```bash
# Test startup time
time ./floxybot
# Should start within 30 seconds

# Test response time
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I create a Flox environment?"}' \
  -w "Time: %{time_total}s\n"
# Should respond within 10 seconds
```

**✅ Expected Results:**
- Startup under 30 seconds
- API responses under 10 seconds
- No memory leaks during extended use

### 10. **Cross-Platform Test**
```bash
# Test on different architectures (if available)
# macOS ARM64, macOS x86_64, Linux x86_64
# Each should work identically
```

**✅ Expected Results:**
- Identical behavior across platforms
- Flox handles platform differences
- No architecture-specific issues

## 🚨 Common Issues to Check

### **Dependency Issues**
- [ ] All Python packages install via `flox install`
- [ ] No `pip install` required
- [ ] Node.js dependencies install correctly
- [ ] ChromaDB initializes without errors

### **Path Issues**
- [ ] All scripts use `$FLOX_ENV_PROJECT` correctly
- [ ] Relative paths work from any directory
- [ ] Data directories are created in correct location

### **Permission Issues**
- [ ] All scripts are executable (`chmod +x`)
- [ ] Data directories are writable
- [ ] No sudo required

### **Configuration Issues**
- [ ] `manifest.toml` syntax is correct for Flox 1.7.3
- [ ] Environment variables are set correctly
- [ ] API keys are handled securely

## 📋 Final Checklist

- [ ] **Setup works**: `./floxai-setup` completes successfully
- [ ] **All modes work**: `floxybot`, `floxai --layer`, `./flox-demo`
- [ ] **Updates work**: Manual and automated updates function
- [ ] **API works**: All endpoints respond correctly
- [ ] **Error handling**: Graceful degradation and helpful messages
- [ ] **Performance**: Fast startup and response times
- [ ] **Documentation**: README and quick start guide are accurate
- [ ] **Packaging**: FloxHub package is valid and installable

## 🎯 Success Criteria

**Ready for FloxHub if:**
- ✅ All tests pass on clean environment
- ✅ No manual intervention required
- ✅ Clear error messages for common issues
- ✅ Performance meets expectations
- ✅ Documentation is complete and accurate

**Not ready if:**
- ❌ Any test fails
- ❌ Manual steps required beyond `flox activate` + `./floxai-setup`
- ❌ Unclear error messages
- ❌ Performance issues
- ❌ Missing documentation

## 🚀 Quick Test Command

```bash
# One-liner to test everything
./floxai-setup && ./floxai-check && echo "✅ Ready for FloxHub!"
```
