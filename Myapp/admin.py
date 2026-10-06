from django.contrib import admin
from .models import User, Website, HomePage, AboutUs, Enquiry, Activity

admin.site.register(User)

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not Website.objects.exists()

admin.site.register(AboutUs)
admin.site.register(HomePage)
admin.site.register(Enquiry)
admin.site.register(Activity)


