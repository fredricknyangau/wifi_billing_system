from django.contrib import admin
from .models import Nas, Radcheck, Radreply, Radacct, Radusergroup, Radgroupreply, Radgroupcheck

@admin.register(Nas)
class NasAdmin(admin.ModelAdmin):
    list_display = ('nasname', 'shortname', 'type', 'secret')
    search_fields = ('nasname', 'shortname')

@admin.register(Radcheck)
class RadcheckAdmin(admin.ModelAdmin):
    list_display = ('username', 'attribute', 'op', 'value')
    search_fields = ('username', 'attribute')

@admin.register(Radreply)
class RadreplyAdmin(admin.ModelAdmin):
    list_display = ('username', 'attribute', 'op', 'value')
    search_fields = ('username', 'attribute')

@admin.register(Radacct)
class RadacctAdmin(admin.ModelAdmin):
    list_display = ('username', 'acctstarttime', 'acctstoptime', 'acctinputoctets', 'acctoutputoctets')
    list_filter = ('acctstarttime',)
    search_fields = ('username',)

@admin.register(Radusergroup)
class RadusergroupAdmin(admin.ModelAdmin):
    list_display = ('username', 'groupname', 'priority')
    search_fields = ('username', 'groupname')

@admin.register(Radgroupreply)
class RadgroupreplyAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'attribute', 'op', 'value')
    search_fields = ('groupname', 'attribute')

@admin.register(Radgroupcheck)
class RadgroupcheckAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'attribute', 'op', 'value')
    search_fields = ('groupname', 'attribute')
