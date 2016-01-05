from django.conf.urls import include, url
from django.contrib import admin
from dju_image import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^image-upload/$',
        views.upload_image,
        name='dju_image_upload'
    ),
]
