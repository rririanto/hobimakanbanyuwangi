from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView


from django.urls import include, path
#import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from main.views import feed, search, popular, rating, andreyongz, offline, getculinary, getrating, getrating, hashtag, detail


urlpatterns = [
    path('', feed, name='feed'),
    path('search/keyword', search, name='search'),
    path('populer', popular, name='popular'),
    path('rating', rating, name='rating'),
    path('andreyongz/', andreyongz, name='andreyongz'),
    path('offline/', offline, name='offline'),
    path('getculinary/', getculinary, name='getculinary'),
    path('getrating/', getrating, name='getrating'),
    path('sw', (TemplateView.as_view(template_name="sw.js", content_type='application/x-javascript', )), name='sw.js'),
    path('manifest\.json', (TemplateView.as_view(template_name="manifest.json", content_type='application/json', )), name='manifest.json'),
    path('browserconfig\.xml', TemplateView.as_view(template_name='browserconfig.xml', content_type='text/xml')),

    #url('siw.js', (TemplateView.as_view(template_name="sw.js", content_type='text/javascript', )), name='siw.js'),

    #url('sw(.*.js)(?:/(?P<params>[a-zA-Z]+)/)?', (TemplateView.as_view(template_name="sw.js", content_type='application/x-javascript', )), name='sw.js'),

    #url('sw\.js$', 'sw_js', name='sw_js'),

    path('hashtag/<slug:slug>', hashtag, name='hashtag'),
    #url('(?P<slug>[\w\d\-\.]+)$',
    #    'detail', name='detail'),
    path('kuliner/<slug:slug>', detail, name='detail'),

    path('googlebaf940c8653177af.html', lambda r: HttpResponse("google-site-verification: googlebaf940c8653177af.html", content_type="text/plain")),
    
    #url('service_worker(.*.js)(?:/(?P<params>[a-zA-Z]+)/)?', 
    #       TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
