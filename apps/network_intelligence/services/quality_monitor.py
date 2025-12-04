from network_intelligence.models import NetworkQualityMetric

class QualityMonitor:
    def ingest_metrics(self, data):
        """
        Process incoming metrics from network devices.
        data: dict containing router_id, region, latency, etc.
        """
        metric = NetworkQualityMetric.objects.create(
            router_id=data['router_id'],
            region=data['region'],
            latency_ms=data['latency_ms'],
            jitter_ms=data['jitter_ms'],
            packet_loss_percent=data['packet_loss_percent'],
            cpu_usage_percent=data.get('cpu_usage_percent', 0.0),
            memory_usage_percent=data.get('memory_usage_percent', 0.0)
        )
        return metric

    def calculate_score(self, region):
        """
        Aggregate score (0-100) for a region based on recent metrics.
        """
        metrics = NetworkQualityMetric.objects.filter(region=region).order_by('-timestamp')[:50]
        if not metrics:
            return 100.0 # Default perfect score
            
        total_score = 0
        count = 0
        
        for m in metrics:
            # Simple scoring logic
            score = 100
            if m.latency_ms > 100: score -= 20
            if m.packet_loss_percent > 1: score -= 30
            if m.jitter_ms > 20: score -= 10
            
            total_score += max(0, score)
            count += 1
            
        return round(total_score / count, 1)
