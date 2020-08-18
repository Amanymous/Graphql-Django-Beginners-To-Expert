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