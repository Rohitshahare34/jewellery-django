import os
import urllib.parse
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import FileResponse, Http404

def serve_hero_static_image(request, filename):
    static_hero_dir = os.path.join(settings.BASE_DIR, 'static', 'hero-section-imgs')
    
    # Try exact match first
    target_path = os.path.join(static_hero_dir, filename)
    if os.path.exists(target_path) and os.path.isfile(target_path):
        return FileResponse(open(target_path, 'rb'), content_type='image/jpeg')

    # Unquote URL path for UTF-8 special characters/emojis
    unquoted = urllib.parse.unquote(filename)
    
    # Fallback to clean Elegant_and_classy.jpg if requested filename refers to Elegant and classy variants
    if 'Elegant' in unquoted or 'classy' in unquoted or 'Elegant' in filename:
        clean_file = os.path.join(static_hero_dir, 'Elegant_and_classy.jpg')
        if os.path.exists(clean_file):
            return FileResponse(open(clean_file, 'rb'), content_type='image/jpeg')

    # General fallback to static serve
    return serve(request, filename, document_root=static_hero_dir)

urlpatterns = [
    re_path(r'^static/hero-section-imgs/(?P<filename>.*)$', serve_hero_static_image),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauth urls
    path('promotions/', include('promotions.urls', namespace='promotions')),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]