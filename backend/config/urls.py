from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from home.api import api_router


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("wagtail-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path('wagtail-api/', api_router.urls),
    path('django-api/contact/', include('contact.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
