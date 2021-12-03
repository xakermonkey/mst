from .views import *
from django.urls import path


urlpatterns = [
    path("", map, name='map'),
    path("statistics", statistics, name='statistics'),
    path("predict", predict, name='predict'),
    path("create_model", create_model, name='create_model'),
    path("docs", docs, name='docs'),
    path("location", location, name='location'),

]
