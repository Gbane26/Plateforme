import graphene
from .models import *
from graphene import relay, ObjectType, Connection, Node, Int
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter
from django.contrib.auth.models import User

class ExtendedConnection(Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length
    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)

# class UserNode(DjangoObjectType):
#     class Meta:
#         model = User
         
#         filter_fields = ['first_name','last_name','email']
          
        
      
#         interfaces = (relay.Node, )
#         connection_class = ExtendedConnection
class ExerciceNode(DjangoObjectType):
    class Meta:
        fields = "__all__"
        model = Exercice

        filter_fields = ['titre_slug']
        
        order_by = OrderingFilter(
            fields=(
                ('date_add','date_add'),
          
            )
        )
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection



class Query(ObjectType):
    Exercice = relay.Node.Field(ExerciceNode)
    all_Exercice = DjangoFilterConnectionField(ExerciceNode)

    