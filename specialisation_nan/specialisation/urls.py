from django.urls import path

from . import views

urlpatterns = [
    path('connexion', views.connexion, name="connexion"),
    path('post', views.islogin, name='login_request'),
    path('', views.home, name="home"),
    path('epreuve/<str:nom_epreuve>/', views.epreuve, name="epreuve"),
    path('epreuve/<str:nom_epreuve>/quizz', views.quizz, name="quizz"),
    path('epreuve/<str:nom_epreuve>/quizz/valide', views.quizz_valider, name="quizz_valider"),
    path('profil', views.profil, name="profil"),
    path('resultat', views.result, name="resultat"),
    path('pdf/<int:id>', views.pdf, name="pdf"),
    path('specialisation', views.specialisation, name="specialisation"),
    path('special', views.special, name="special"),
    path('deconnexion', views.deconnexion, name='deconnexion'),
]