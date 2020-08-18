import graphene 
import cassandra.schema

class Query(cassandra.schema.Query,graphene.ObjectType):
  pass

class Mutation(cassandra.schema.Mutation,graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query ,mutation=Mutation)

