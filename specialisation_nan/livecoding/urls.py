from django.urls import path

from . import views

urlpatterns = [
    path('<str:nom_epreuve>/livecoding', views.coding, name="coding"),
    path('code', views.postCode, name='code'),
    path('tester', views.postCodeTest, name='tester'),
]
