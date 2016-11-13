from django.conf import urls
from django.contrib import admin

urlpatterns = [
    urls.url(r'^admin/', admin.site.urls),
    urls.url(r'^api/', urls.include('image_data.urls'))
]
