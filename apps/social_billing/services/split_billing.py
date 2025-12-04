from decimal import Decimal

class BillSplitter:
    def calculate_shares(self, group):
        """
        Calculate how much each member owes based on the CostSplitter config.
        """
        splitter = group.cost_splitter
        members = group.members.all()
        count = members.count()
        
        if count == 0:
            return {}
            
        total_cost = group.plan.price # Assuming Plan has a price field
        
        shares = {}
        
        if splitter.split_type == 'EQUAL':
            share_amount = total_cost / count
            for member in members:
                shares[member.id] = share_amount
                
        # TODO: Implement USAGE and CUSTOM split types
        
        return shares
