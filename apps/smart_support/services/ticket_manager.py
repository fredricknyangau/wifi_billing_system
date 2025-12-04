from smart_support.models import SupportTicket, TicketAnalysis
from smart_support.services.sentiment_analyzer import SentimentAnalyzer
from smart_support.services.auto_resolution import AutoResolutionService

class TicketManager:
    def create_ticket(self, customer, subject, message):
        """
        Create a ticket and trigger analysis.
        """
        ticket = SupportTicket.objects.create(
            customer=customer,
            subject=subject,
            message=message
        )
        
        # 1. Analyze Sentiment
        analyzer = SentimentAnalyzer()
        analysis_result = analyzer.analyze(f"{subject} {message}")
        
        # 2. Attempt Auto-Resolution
        resolver = AutoResolutionService()
        resolution = resolver.attempt_fix(ticket)
        
        suggested_action = ""
        if resolution:
            suggested_action = f"Auto-Diagnosis: {resolution['diagnosis']} Action: {resolution['action']}"
        
        # 3. Save Analysis
        TicketAnalysis.objects.create(
            ticket=ticket,
            sentiment=analysis_result['sentiment'],
            urgency_score=analysis_result['urgency_score'],
            suggested_action=suggested_action
        )
        
        # Update priority based on urgency
        if analysis_result['urgency_score'] >= 8:
            ticket.priority = 'CRITICAL'
        elif analysis_result['urgency_score'] >= 6:
            ticket.priority = 'HIGH'
        ticket.save()
        
        return ticket

    def resolve_ticket(self, ticket, resolution_message):
        """
        Mark as resolved.
        """
        ticket.status = 'RESOLVED'
        ticket.save()
        # Log resolution message (omitted for brevity)
