class CompetitorBenchmark:
    def get_comparison(self, region):
        """
        Compare own uptime/speed vs industry average (mocked data).
        """
        # Mock data
        return {
            'our_uptime': 99.9,
            'industry_avg_uptime': 97.5,
            'our_speed_avg': 25.0,
            'competitor_speed_avg': 15.0,
            'region': region
        }
