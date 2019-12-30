from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Connection
import graphene

from . import models
from django.contrib.auth.models import User
from quizz_app.models import QuizzUser



class ExtendConnection(Connection):
    class Meta:
        abstract = True
    total_count = graphene.Int()
    edge_count = graphene.Int()
    def resolve_total_count(root,info,**kwargs):
        return root.length
    def resolve_edge_count(root,info,**kwargs):
        return len(root.edges)

class SpecialiteNode(DjangoObjectType):
    class Meta:
        model = models.Specialite
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'nom': ['exact', 'icontains', 'istartswith'],
            'code': ['exact', 'icontains', ],
            'quizz': ['exact', 'icontains', ],
            'status': ['exact', 'icontains',],
            # permet de rechercher la spécialité d'un utilisateur par son firstname
            'userspecialite_specialite__user__first_name': ['exact', 'icontains', 'istartswith'],
            # permet de faire un filtrer les spécialité par nom des épreuves
            'epreuve_specialite__nom': ['exact', 'icontains', 'istartswith' ],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'username': ['exact', 'icontains', 'istartswith'],
            # permet de filter les utilisateur par spécialité
            'user_specialite__nom': ['exact', 'icontains', 'istartswith'],
            'statut': ['exact'],
            'resultat_user__note': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class UserSpecialiteNode(DjangoObjectType):
    class Meta:
        model = models.UserSpecialite
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'status_demande': ['exact'],
            'nanplus': ['exact', 'icontains', 'istartswith'],
            # permet de filtrer les utilisateurs par spécialité
            'specialite__nom': ['exact', 'icontains', 'istartswith'],
            'specialite__id': ['exact'],
            'status': ['exact'],

        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class EpreuveNode(DjangoObjectType):
    class Meta:
        model = models.Epreuve
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'nom': ['exact', 'icontains', 'istartswith'],
            'cours__titre': ['exact', 'icontains', 'istartswith'],
            'specialite__nom': ['exact', 'icontains', 'istartswith'],
            'status': ['exact'],
            'specialite__id': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection
        
class CoursNode(DjangoObjectType):
    class Meta:
        model = models.Cours
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'titre': ['exact', 'icontains', 'istartswith'],
            'status': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection
        
class RessourcePdfNode(DjangoObjectType):
    class Meta:
        model = models.RessourcePdf
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'status': ['exact'],
            'cours__titre': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection
        
class RessourceVideoNode(DjangoObjectType):
    class Meta:
        model = models.RessourceVideo
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'status': ['exact'],
            'cours__titre': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection
        
class ResultatEpreuveNode(DjangoObjectType):
    class Meta:
        model = models.ResultatEpreuve
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'note': ['exact'],
            'epreuve__nom': ['exact', 'icontains', 'istartswith'],
            'quizz__quizz__titre': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection
    
class Query(graphene.ObjectType):
    Specialite = relay.Node.Field(SpecialiteNode)
    all_Specialites = DjangoFilterConnectionField(SpecialiteNode)

    UserSpecialite= relay.Node.Field(UserSpecialiteNode)
    all_UserSpecialites = DjangoFilterConnectionField(UserSpecialiteNode)
        
    Epreuve = relay.Node.Field(EpreuveNode)
    all_Epreuves = DjangoFilterConnectionField(EpreuveNode)
    
    Cours = relay.Node.Field(CoursNode)
    all_Courss = DjangoFilterConnectionField(CoursNode)
    
    RessourcePdf = relay.Node.Field(RessourcePdfNode)
    all_RessourcePdfs = DjangoFilterConnectionField(RessourcePdfNode)
    
    RessourceVideo = relay.Node.Field(RessourceVideoNode)
    all_RessourceVideos = DjangoFilterConnectionField(RessourceVideoNode)

    ResultatEpreuve = relay.Node.Field(ResultatEpreuveNode)
    all_ResultatEpreuves = DjangoFilterConnectionField(ResultatEpreuveNode)