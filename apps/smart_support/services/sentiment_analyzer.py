class SentimentAnalyzer:
    def analyze(self, text):
        """
        Returns sentiment (POSITIVE, NEUTRAL, NEGATIVE) and urgency score (1-10).
        """
        text_lower = text.lower()
        
        # Basic keyword matching
        negative_keywords = ['hate', 'down', 'broken', 'slow', 'terrible', 'fail', 'error']
        urgent_keywords = ['immediately', 'now', 'urgent', 'emergency', 'outage']
        
        sentiment = 'NEUTRAL'
        urgency = 5
        
        if any(word in text_lower for word in negative_keywords):
            sentiment = 'NEGATIVE'
            urgency = 7
            
        if any(word in text_lower for word in urgent_keywords):
            urgency = min(10, urgency + 3)
            
        if 'love' in text_lower or 'great' in text_lower or 'thanks' in text_lower:
            sentiment = 'POSITIVE'
            urgency = 3
            
        return {
            'sentiment': sentiment,
            'urgency_score': urgency
        }
