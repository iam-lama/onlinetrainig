from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

]

urlpatterns += i18n_patterns(
	path('jet/', include('jet.urls', 'jet')),  
	path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', include('trainboard.url')),
    path('', include('accounts.url')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sms/', include('sms.url')),
    # prefix_default_language=False,
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)