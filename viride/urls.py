from django.contrib import admin
from django.http import Http404
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render
from contacts.views import contacts
from favorites.views import favorites
from index.views import index
from other.views import (
    BookProductDetail, BookProductList, RelatedProductDetail, RelatedProductList)
from profiles.allauth.views import PersistLogoutView, RedirectedPasswordChangeView
from search.views import SearchView
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found

admin.site.site_header = admin.site.site_title = 'Питомник «Вириде»'

#--

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login'), name='logout'),
    path('admin/', admin.site.urls),
    path("accounts/email/", page_not_found,
         kwargs={"exception": Exception("Page not Found")},),
    path('accounts/password/change/', RedirectedPasswordChangeView.as_view(),
         name="account_change_password"),

    # path('login/', PersistLoginView.as_view(), name='account_login'),
    path('accounts/logout/', PersistLogoutView.as_view(), name='account_logout'),

    # path('account/login/', RedirectView.as_view(permanent=True, url='/accounts/login/')), #seems allauth bug
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', include(('profiles.urls', 'profiles'), namespace='profiles')),

    path('', index, name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('contacts/', contacts, name='contacts'),

    path('catalog/', TemplateView.as_view(
        template_name="catalog/index.html"), name="catalog_template"),
    path('catalog/conifers/', include(('conifers.urls','conifers'), namespace='conifers')),
    path('catalog/deciduous/',
         include(('deciduous.urls', 'deciduous'), namespace='decs')),
    path('catalog/fruits/', include(('fruits.urls', 'fruits'), namespace='fruits')),
    path('catalog/perennials/',
         include(('perennials.urls', 'perennials'), namespace='pers')),
    
    path('catalog/roses/', include(('roses.urls', 'roses'), namespace='roses')),

    path('catalog/books/',
         BookProductList.as_view(), name='book_list'),
    path('catalog/books/<slug:slug>/',
         BookProductDetail.as_view(), name='book_detail'),

    path('catalog/related/',
         RelatedProductList.as_view(), name='related_list'),
    path('catalog/related/<slug:slug>/',
         RelatedProductDetail.as_view(), name='related_detail'),

    path('favorites/', favorites, name='favorites'),

    path('cart/', include(('carts.urls', 'carts'), namespace='carts')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),

    path('privacy-policy/', TemplateView.as_view(
        template_name="privacy-policy/index.html"), name="p-p_template"),


    # path('accounts/login/', RedirectView.as_view(pattern_name='', permanent=False)),
    # path('chaining/', include('smart_selects.urls')),
    # path("select2/", include("django_select2.urls")),
]

#--


def handler400(request, exception, template_name='errors/400.html'):
    response = render(request, template_name)
    response.status_code = 400
    return response


def handler403(request, exception, template_name='errors/403.html'):
    response = render(request, template_name)
    response.status_code = 403
    return response


def handler404(request, exception, template_name='errors/404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name='errors/500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return response

# --

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += [
        path('400/', TemplateView.as_view(template_name="errors/400.html")),
        path('403/', TemplateView.as_view(template_name="errors/403.html")),
        path('404/', TemplateView.as_view(template_name="errors/404.html")),
        path('500/', TemplateView.as_view(template_name="errors/500.html")),
    ]
        
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(r'/favicon.ico', document_root='static/favicon.ico')
