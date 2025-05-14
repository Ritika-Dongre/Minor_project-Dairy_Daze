"""
URL configuration for DairyDaze_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from customer import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root URL points to the product page without requiring login
    path('', customer_views.productpage, name='home'),
    path('customer/', include('customer.urls', namespace='customer')),
    path('store/', include('store.urls', namespace='store')),
    path('userauths/', include('userauths.urls', namespace='userauths')),
    path('subbranch/', include('subbranch.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 