from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from admin_profile import models
from django.db.models import Sum

class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', self.dashboard),
        ]
        return my_urls + urls

    def dashboard(self, request):
        # getting total earning by admin
        total_earning = models.AdminProfile.objects.all().aggregate(Sum('total_earning'))['total_earning__sum']
        total_earning = '{:0.2f}'.format(total_earning)
        context = {
            "total_earning": total_earning
        }
        return TemplateResponse(request, "admin_dashboard.html", context)


# Register your models here.
admin.site.register(models.AdminProfile, MyModelAdmin)