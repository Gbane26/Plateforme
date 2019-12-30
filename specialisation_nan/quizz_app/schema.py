from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Connection
import graphene
from graphql_relay import from_global_id


from . import models
from specialisation import models as specialisation
from django.contrib.auth.models import User


class ExtendConnection(Connection):
    class Meta:
        abstract = True
    total_count = graphene.Int()
    edge_count = graphene.Int()
    def resolve_total_count(root,info,**kwargs):
        return root.length
    def resolve_edge_count(root,info,**kwargs):
        return len(root.edges)

class QuizzNode(DjangoObjectType):
    class Meta:
        model = models.Quizz
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'titre': ['exact', 'icontains', 'istartswith'],
            'specialite__nom': ['exact', 'icontains', 'istartswith'],
            'niveau': ['exact'],
            'pourcentage': ['exact'],
            'nbq': ['exact'],
            'duree': ['exact'],
            'statut': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class RelayCreateQuizz(graphene.relay.ClientIDMutation):
    quizz = graphene.Field(QuizzNode)
    class Input:
        specialite = graphene.ID()
        titre = graphene.String()
        niveau = graphene.Int()
        pourcentage = graphene.Int()
        nbq = graphene.Int()
        date_debut = graphene.types.datetime.DateTime()
        date_fin = graphene.types.datetime.DateTime()
        date_fin = graphene.types.datetime.Time()
    def mutate_and_get_payload(root,info,**kwargs):
        titre = kwargs.get('titre') or None
        specialite = kwargs.get('titre') or None
        niveau = kwargs.get('titre') or None
        pourcentage = kwargs.get('titre') or None
        nbq = kwargs.get('titre') or None
        date_debut = kwargs.get('titre') or None
        date_fin = kwargs.get('description') or None
        duree = kwargs.get('description') or None

        quizz = None
        if specialite:
            specialite = from_global_id(specialite)
            specialite=specialite[1]
            specialite = specialisation.Specialite.objects.get(id=specialite)
        data = {
            'titre':titre,
            'niveau':niveau,
            'pourcentage':pourcentage,
            'nbq':nbq,
            'date_debut':date_debut,
            'date_fin':date_fin,
            'duree':duree,
            'specialite':specialite,
        }
        if titre is not None and niveau is not None and pourcentage is not None and nbq is not None and date_debut is not None and date_fin is not None  and duree is not None  and specialite is not None :
            quizz = models.Quizz(titre=titre,niveau=niveau,pourcentage=pourcentage,nbq=nbq,date_debut=date_debut,date_fin=date_fin,duree=duree,specialite=specialite)
            quizz.save()
        else:
            raise Exception('les paramettre sont requis')
        return RelayCreateQuizz(quizz=quizz)

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'username': ['exact', 'icontains', 'istartswith'],
            'statut': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class QuestionNode(DjangoObjectType):
    class Meta:
        model = models.Question
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'niveau': ['exact'],
            'contenu': ['exact', 'icontains', 'istartswith'],
            'statut': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class ReponseNode(DjangoObjectType):
    class Meta:
        model = models.Reponse
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'isrtue': ['exact', 'icontains'],
            'contenu': ['exact', 'icontains', 'istartswith'],
            'statut': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection
        
class QuizzUserNode(DjangoObjectType):
    class Meta:
        model = models.QuizzUser
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'note': ['exact'],
            'issubmit': ['exact', 'icontains'],
            'date_valide': ['exact', 'icontains'],
            'statut': ['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class RelayCreateQuizzUser(graphene.relay.ClientIDMutation):
    quizzUser = graphene.Field(QuizzUserNode)
    class Input:
        quizz = graphene.ID()
        note = graphene.Int()
        date_valide = graphene.types.datetime.DateTime()
        
    def mutate_and_get_payload(root,info,**kwargs):
        quizz = kwargs.get('quizz') or None
        user = info.context.user or None
        note = kwargs.get('titre') or None
        date_valide = kwargs.get('description') or None
        
        quizzUser = None
        if quizz:
            quizz = from_global_id(quizz)
            quizz=quizz[1]
            quizz = models.Quizz.objects.get(id=quizz)
        data = {
            'quizz':quizz,
            'user':user,
            'note':note,
            'date_valide':date_valide,
        }
        if quizz and user and note and date_valide :
            quizzUser = models.QuizzUser(**data)
            quizzUser.save()
            return RelayCreateQuizzUser(quizzUser=quizzUser)
        else:
            raise Exception('must be have all data to create article')

        
        
class ReponseUserNode(DjangoObjectType):
    class Meta:
        model = models.ReponseUser
        # Allow for some more advanced filtering here
        fields = "__all__"
        filter_fields = {
            'istrue': ['exact', 'icontains'],
            'statut': ['exact'],
            'quizzuser__date_add':['exact'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendConnection

class RelayCreateReponseUser(graphene.relay.ClientIDMutation):
    reponseUser = graphene.Field(ReponseUserNode)
    class Input:
        quizzuser = graphene.ID()
        question = graphene.ID()
        reponses = graphene.ID()
        istrue = graphene.Boolean()
        
    def mutate_and_get_payload(root,info,**kwargs):
        quizzuser = kwargs.get('quizzuser') or None
        question = kwargs.get('question') or None
        reponses = kwargs.get('reponses') or None
        istrue = kwargs.get('istrue') or None
        
        reponseUser = None
        if quizzuser:
            quizzuser = from_global_id(quizzuser)
            quizzuser=quizzuser[1]
            quizzuser = models.QuizzUser.objects.get(id=quizzuser)
        if question:
            question = from_global_id(question)
            question=question[1]
            question = models.Question.objects.get(id=question)
        if reponses :
            userReponse = reponses.split(',')
            tableau = []
            for item in userReponse:
                item = from_global_id(userReponse)
                item=item[1]
                userR = models.Reponse.objects.get(pk=item)
                tableau.append(userR)
        data = {
            'quizzuser':quizzuser,
            'question':question,
            'istrue':istrue,
        }
        if quizzuser and question and istrue and reponses :
            quizzUser = models.QuizzUser(**data)
            quizzUser.save()
            for rep in tableau :
                quizzuser.response.add(rep)
                reponseUser.save()
            return RelayCreateQuizzUser(quizzUser=quizzUser)
        else:
            raise Exception('must be have all data to create article')

        
        
    
class Query(graphene.ObjectType):
    Quizz = relay.Node.Field(QuizzNode)
    all_Quizzs = DjangoFilterConnectionField(QuizzNode)

    Question = relay.Node.Field(QuestionNode)
    all_Questions = DjangoFilterConnectionField(QuestionNode)
        
    Reponse = relay.Node.Field(ReponseNode)
    all_Reponses = DjangoFilterConnectionField(ReponseNode)
    
    QuizzUser = relay.Node.Field(QuizzUserNode)
    all_QuizzUsers = DjangoFilterConnectionField(QuizzUserNode)
    
    ReponseUser = relay.Node.Field(ReponseUserNode)
    all_ReponseUsers = DjangoFilterConnectionField(ReponseUserNode)

class RelayMutation(graphene.AbstractType):
    relay_create_quizz = RelayCreateQuizz.Field()
    relay_create_quizzUser = RelayCreateQuizzUser.Field()
    relay_create_reponseUser = RelayCreateReponseUser.Field()