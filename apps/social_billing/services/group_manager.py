from social_billing.models import GroupPlan, GroupMember, CostSplitter

class GroupManager:
    def create_group(self, name, admin, plan):
        """
        Create a new group.
        """
        group = GroupPlan.objects.create(name=name, admin=admin, plan=plan)
        # Admin is automatically a member
        GroupMember.objects.create(group=group, customer=admin)
        # Default cost splitter
        CostSplitter.objects.create(group=group, split_type='EQUAL')
        return group

    def add_member(self, group, customer):
        """
        Add a member to the group.
        """
        member, created = GroupMember.objects.get_or_create(group=group, customer=customer)
        return member

    def remove_member(self, group, customer):
        """
        Remove a member.
        """
        GroupMember.objects.filter(group=group, customer=customer).delete()
