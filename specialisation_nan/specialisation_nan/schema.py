import graphene

import quizz_app.schema
import specialisation.schema
import livecoding.schema


class Query(quizz_app.schema.Query, specialisation.schema.Query,livecoding.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass
class Mutation(quizz_app.schema.RelayMutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)

