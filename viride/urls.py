from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from catalog.sitemap import CatalogSitemap
from catalog.views import CatalogItemList
from conifers.sitemap import ConiferProductSitemap
from contacts.sitemap import ContactsSitemap
from contacts.views import contacts
from deciduous.sitemap import DecProductSitemap
from favorites.views import favorites
from fruits.sitemap import FruitProductSitemap
from index.sitemap import IndexSitemap
from index.views import index
from other.sitemap import OtherProductSitemap
from other.views import (
    BookProductDetail, BookProductList, RelatedProductDetail, RelatedProductList)
from perennials.sitemap import PerProductSitemap
from pricelist.sitemap import PriceListSitemap
from pricelist.view import price_list
from profiles.allauth.views import PersistLogoutView, RedirectedPasswordChangeView
from roses.sitemap import RoseProductSitemap
from sales.sitemap import SaleSitemap
from sales.views import sale
from search.views import SearchView


admin.site.site_header = admin.site.site_title = 'Питомник растений «Вириде»'


#--

sitemaps = {
    'index': IndexSitemap,
    'catalog': CatalogSitemap,
    'sale': SaleSitemap,
    'contacts': ContactsSitemap,
    'roses': RoseProductSitemap,
    'conifers': ConiferProductSitemap,
    'decs': DecProductSitemap,
    'fruits': FruitProductSitemap,
    'pers': PerProductSitemap,
    'other': OtherProductSitemap,
    # 'pricelist': PriceListSitemap,
}

# --

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
    path('sale/', sale, name='sale_list'),
    path('price-list/', price_list, name='price_list_detail'),
    path('contacts/', contacts, name='contacts'),

    path('catalog/', CatalogItemList.as_view(), name="catalog_item_list"),
    # path('catalog/', TemplateView.as_view(
    #     template_name="catalog/index.html"), name="catalog_template"),

    path('catalog/conifers/', include(('conifers.urls','conifers'), namespace='conifers')),
    path('catalog/deciduous/',
         include(('deciduous.urls', 'deciduous'), namespace='decs')),
    path('catalog/fruits/', include(('fruits.urls', 'fruits'), namespace='fruits')),
    path('catalog/perennials/',
         include(('perennials.urls', 'perennials'), namespace='pers')),

    path('catalog/seedlings/',
         include(('seedlings.urls', 'seedlings'), namespace='seedlings')),
    
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
    path('order/', include(('orders.urls', 'orders'), namespace='orders')),

    path('privacy-policy/', TemplateView.as_view(
        template_name="privacy-policy/index.html"), name="p-p_template"),

    path('sitemap.xml', cache_page(86400, cache='sitemap')(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
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
