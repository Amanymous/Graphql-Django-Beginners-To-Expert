import graphene
from .models import Cassandra
from graphene_django import DjangoObjectType

class CassandraType(DjangoObjectType):
    class Meta:
        model = Cassandra

class Query(graphene.ObjectType):
    cassandras = graphene.List(CassandraType)

    def resolve_cassandras(self,info):
      return Cassandra.object.all()

# adding mutation
class CreateCassandra(graphene.Mutation):
    cassandra = graphene.String()
    

    class Arguments:
        FirstName = graphene.String()
        LastName = graphene.String()
        Age = graphene.Int()
        Description = graphene.String()
        url = graphene.String()

    def mutate(self,info,FirstName,LastName,Age,Description,url):
        cassandra = Cassandra(FirstName=FirstName,LastName=LastName,
        Age=Age,Description=Description,url=url)
        cassandra.save()
        return CreateCassandra(cassandra=cassandra)


class Mutation(graphene.ObjectType):
    create_cassandra = CreateCassandra.Field()