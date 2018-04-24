from django.conf.urls import patterns, include, url
from django.contrib import admin
from cms_post import views
from django.contrib.auth.views import logout, login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.inicio_pag, name="Listado de las paginas"),
    url(r'^logout', logout,  {'next_page': '/'}),
    url(r'^login', login, {'template_name': 'registration/login.html'}),
    url(r'^edit/(.+)', views.edit_pag, name="Editar una página"),
)
