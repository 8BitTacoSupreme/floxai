"""
FloxAI Learning Service - Continuous improvement from user feedback
"""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from app.core.config import get_settings

class FloxLearningService:
    """Service for learning from user feedback and improving responses"""
    
    def __init__(self):
        self.settings = get_settings()
        self.db_path = self.settings.db_path
        self.learning_data_path = Path(self.settings.docs_path) / "learning"
        self.learning_data_path.mkdir(parents=True, exist_ok=True)
    
    def analyze_feedback_patterns(self) -> Dict:
        """Analyze feedback patterns to identify improvement opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent feedback (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        cursor.execute('''
            SELECT 
                query_text,
                response_text,
                worked,
                COUNT(*) as frequency,
                AVG(CASE WHEN worked = 1 THEN 1.0 ELSE 0.0 END) as success_rate
            FROM feedback 
            WHERE timestamp > ?
            GROUP BY query_text, response_text
            HAVING COUNT(*) > 1
            ORDER BY frequency DESC, success_rate ASC
        ''', (thirty_days_ago,))
        
        patterns = cursor.fetchall()
        
        # Analyze patterns
        high_frequency_low_success = [
            p for p in patterns 
            if p[3] >= 3 and p[4] < 0.5  # 3+ occurrences, <50% success
        ]
        
        successful_patterns = [
            p for p in patterns 
            if p[3] >= 2 and p[4] >= 0.8  # 2+ occurrences, >=80% success
        ]
        
        conn.close()
        
        return {
            "problem_areas": high_frequency_low_success,
            "successful_patterns": successful_patterns,
            "total_patterns": len(patterns),
            "analysis_date": datetime.now().isoformat()
        }
    
    def generate_learning_insights(self) -> Dict:
        """Generate actionable insights from feedback analysis"""
        patterns = self.analyze_feedback_patterns()
        
        insights = {
            "summary": {
                "total_patterns_analyzed": patterns["total_patterns"],
                "problem_areas_count": len(patterns["problem_areas"]),
                "successful_patterns_count": len(patterns["successful_patterns"])
            },
            "recommendations": [],
            "knowledge_gaps": [],
            "successful_approaches": []
        }
        
        # Identify knowledge gaps
        for pattern in patterns["problem_areas"]:
            query, response, worked, freq, success_rate = pattern
            insights["knowledge_gaps"].append({
                "query": query,
                "current_success_rate": round(success_rate * 100, 1),
                "frequency": freq,
                "suggestion": "Consider adding more specific documentation for this topic"
            })
        
        # Identify successful approaches
        for pattern in patterns["successful_patterns"]:
            query, response, worked, freq, success_rate = pattern
            insights["successful_approaches"].append({
                "query": query,
                "success_rate": round(success_rate * 100, 1),
                "frequency": freq,
                "approach": "This response pattern works well - consider using as template"
            })
        
        # Generate recommendations
        if patterns["problem_areas"]:
            insights["recommendations"].append({
                "type": "knowledge_expansion",
                "priority": "high",
                "description": f"Found {len(patterns['problem_areas'])} topics with low success rates",
                "action": "Review and expand documentation for these topics"
            })
        
        if patterns["successful_patterns"]:
            insights["recommendations"].append({
                "type": "pattern_replication",
                "priority": "medium", 
                "description": f"Found {len(patterns['successful_patterns'])} highly successful response patterns",
                "action": "Use these patterns as templates for similar queries"
            })
        
        return insights
    
    def save_learning_insights(self, insights: Dict) -> str:
        """Save learning insights to file for review"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"learning_insights_{timestamp}.json"
        filepath = self.learning_data_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(insights, f, indent=2)
        
        return str(filepath)
    
    def get_response_improvements(self, query: str) -> List[str]:
        """Get improvement suggestions for a specific query based on past feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Look for similar queries and their success rates
        cursor.execute('''
            SELECT 
                response_text,
                AVG(CASE WHEN worked = 1 THEN 1.0 ELSE 0.0 END) as success_rate,
                COUNT(*) as frequency
            FROM feedback 
            WHERE query_text LIKE ? OR query_text LIKE ?
            GROUP BY response_text
            HAVING COUNT(*) >= 2
            ORDER BY success_rate DESC, frequency DESC
            LIMIT 3
        ''', (f"%{query[:20]}%", f"%{query[-20:]}%"))
        
        improvements = cursor.fetchall()
        conn.close()
        
        suggestions = []
        for response, success_rate, freq in improvements:
            if success_rate >= 0.7:  # 70%+ success rate
                suggestions.append({
                    "response_pattern": response[:200] + "..." if len(response) > 200 else response,
                    "success_rate": round(success_rate * 100, 1),
                    "frequency": freq,
                    "confidence": "high" if success_rate >= 0.9 else "medium"
                })
        
        return suggestions
    
    def update_knowledge_base_from_feedback(self) -> Dict:
        """Update knowledge base based on feedback patterns"""
        insights = self.generate_learning_insights()
        
        # Save insights
        insights_file = self.save_learning_insights(insights)
        
        # Create learning summary
        summary = {
            "learning_session": datetime.now().isoformat(),
            "insights_file": insights_file,
            "recommendations_count": len(insights["recommendations"]),
            "knowledge_gaps_identified": len(insights["knowledge_gaps"]),
            "successful_patterns_found": len(insights["successful_approaches"]),
            "next_actions": [
                "Review knowledge gaps and expand documentation",
                "Use successful patterns as response templates",
                "Consider adding specific examples for problematic topics"
            ]
        }
        
        return summary
    
    def get_learning_stats(self) -> Dict:
        """Get learning statistics for monitoring"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get feedback stats
        cursor.execute('SELECT COUNT(*) FROM feedback')
        total_feedback = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM feedback WHERE worked = 1')
        positive_feedback = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM feedback WHERE timestamp > ?', 
                      ((datetime.now() - timedelta(days=7)).isoformat(),))
        recent_feedback = cursor.fetchone()[0]
        
        # Get unique queries
        cursor.execute('SELECT COUNT(DISTINCT query_text) FROM feedback')
        unique_queries = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_feedback": total_feedback,
            "positive_feedback": positive_feedback,
            "recent_feedback_7d": recent_feedback,
            "unique_queries": unique_queries,
            "overall_success_rate": round(positive_feedback / max(total_feedback, 1) * 100, 1),
            "learning_active": total_feedback > 0
        }
