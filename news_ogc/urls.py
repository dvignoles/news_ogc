from django.urls import path, re_path
from news_ogc import views


urlpatterns = [
    path('wms/<slug:model>/<int:year>/', views.wms_test, name='news_ogc'),
    path('wcs/', views.wcs, name="news_wcs"),
]


