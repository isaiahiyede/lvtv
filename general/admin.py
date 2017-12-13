from django.contrib import admin
from models import UserAccount, Referrals


# Register your models here.

#class PackageAdmin(admin.ModelAdmin):
#    list_display = ('user', 'status', 'id', 'box_weight_Actual', 'box_weight_Dim', 'ordered', )
#    search_fields = ['user__username', 'id']
#    list_filter  = ['status']
#
#
#
#
#admin.site.register(Package, PackageAdmin)

# class TemplateContentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug',)
#
# admin.site.register(TemplateContent, TemplateContentAdmin)
# admin.site.register(TemplateContentImage)
#

class UserAccountAdmin(admin.ModelAdmin):
    search_fields = ['user__email']

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Referrals)




