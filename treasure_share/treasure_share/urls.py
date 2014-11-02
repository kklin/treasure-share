from django.conf.urls import patterns, include, url
from django.contrib import admin
from treasure_app import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'treasure_share.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^donate/$', views.donate, name='donate'),
    url(r'^donate/action/', views.action, name='action'),
    url(r'^auth/', views.auth),
    url(r'^auth2/', views.auth2),
    url(r'^display_oauth/', views.display_oauth),
    url(r'^withdraw/$', views.withdraw, name='donate'),
    url(r'^transaction/sign_withdraw/$', views.sign_transaction),
    url(r'^transaction/$', views.transaction),
    url(r'^withdraw/action_withdraw/', views.action_withdraw, name='action_w'),
)
