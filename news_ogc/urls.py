from django.urls import path, re_path
from news_ogc import views


urlpatterns = [
    # re_path(r'', views.wms),
    # re_path(r'^$', views.wms),
    path('wms/<slug:model>/<int:year>/', views.wms, name='news_wms'),
    path('wcs/', views.wcs, name="news_wcs"),
]
