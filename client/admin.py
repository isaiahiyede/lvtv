from django.contrib import admin
from client.models import ProvideHelp, GetHelp, Testimonials


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


admin.site.register(GetHelp)
admin.site.register(ProvideHelp)
admin.site.register(Testimonials)



