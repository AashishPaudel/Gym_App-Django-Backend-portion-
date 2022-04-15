from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('customers/', include('customer.urls')),
    path('gym/', include('gym.urls')),
    path('admin-profile/', include('admin_profile.urls')),
    path('subscriptions/', include('subscription.urls')),
    path('payment/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
