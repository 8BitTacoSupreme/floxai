#!/bin/bash
# FloxAI Learning Update Script
# Runs learning analysis and updates knowledge base from user feedback

set -e

echo "🧠 FloxAI Learning Update"
echo "========================"

if [ -z "$FLOX_ENV" ]; then
    echo "❌ Must run inside Flox environment"
    echo "   Run: flox activate"
    exit 1
fi

PROJECT_DIR="${FLOX_ENV_PROJECT:-/Users/jhogan/floxai}"

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ FloxAI backend not running"
    echo "   Start with: floxybot or floxybotdev"
    exit 1
fi

echo "📊 Analyzing user feedback patterns..."

# Get learning insights
INSIGHTS=$(curl -s http://localhost:8000/api/chat/learning/insights)
echo "✅ Learning insights generated"

# Update knowledge base from feedback
echo "🔄 Updating knowledge base from feedback..."
UPDATE_RESULT=$(curl -s -X POST http://localhost:8000/api/chat/learning/update)
echo "✅ Knowledge base updated"

# Get learning stats
STATS=$(curl -s http://localhost:8000/api/chat/learning/stats)
echo "📈 Learning Statistics:"
echo "$STATS" | jq -r '
  "   Total Feedback: \(.total_feedback)
   Positive Feedback: \(.positive_feedback)
   Recent Feedback (7d): \(.recent_feedback_7d)
   Unique Queries: \(.unique_queries)
   Success Rate: \(.overall_success_rate)%
   Learning Active: \(.learning_active)"
'

echo ""
echo "🎯 Learning Update Complete!"
echo "   Insights saved to: $PROJECT_DIR/data/flox_docs/learning/"
echo "   Next update: Run this script again or set up cron job"
echo ""
echo "💡 To set up automatic learning updates:"
echo "   Add to crontab: 0 2 * * * $PROJECT_DIR/update_learning.sh"
