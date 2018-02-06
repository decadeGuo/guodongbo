"""graduation_design URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include,handler404
from django.contrib import admin
from django.views.static import serve

from graduation_design import index, settings
from django.conf.urls.static import static
# handler404 = "index.not_fond"
# handler500 = "index.not_fond"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index.index),
    url(r'^auth/',include('auth_log.urls')),
    url(r'^car/', include('use_car.urls')),
    url(r'^user/info/$',index.info),
    url(r'^user/info/other/$',index.info_2),
    url(r'^other/',include('other.urls')),
    url(r'^leave/',include('leave.urls')),

]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
