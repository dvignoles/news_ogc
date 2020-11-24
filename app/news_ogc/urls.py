from django.urls import path, re_path
from news_ogc import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('wms/<slug:model>/<int:year>/', views.wms, name='news_wms'),
    path('wcs/', views.wcs, name="news_wcs"),
]
