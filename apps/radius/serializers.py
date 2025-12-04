from rest_framework import serializers
from .models import Nas, Radcheck, Radreply, Radacct, Radusergroup, Radgroupreply, Radgroupcheck

class NasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nas
        fields = '__all__'

class RadcheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radcheck
        fields = '__all__'

class RadreplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Radreply
        fields = '__all__'

class RadacctSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radacct
        fields = '__all__'

class RadusergroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radusergroup
        fields = '__all__'

class RadgroupreplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Radgroupreply
        fields = '__all__'

class RadgroupcheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radgroupcheck
        fields = '__all__'
