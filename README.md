# Graphql-Django-Beginners-To-Expert
<h1>GraphQl Beginners To Advanced In Python</h1>

```
pipenv install django graphene-django django-graphql-jwt django-cors-headers
pipenv install --dev autopep8
pipenv shell
django-admin startproject app
cd app
python manage.py migrate
python manage.py runserver
python manage.py startapp cassandra

```
<h3>Go to settings.py and add this</h3>

```

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'cassandra'
]

```

<h3>Go to models.py and add this</h3>

```

from django.db import models

# Create your models here.
class Cassandra(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Age = models.PositiveIntegerField(null=True, blank=True)    
    Description = models.TextField(blank=True)
    url = models.URLField()
    createdAt = models.DateTimeField(auto_now_add=True)
    
```

```

cd app/
python manage.py makemigrations
python manage.py migrate

```


<h1>Creating Schema with Graphene-Django</h1>

```

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'cassandra'
]
GRAPHENE={
    'SCHEMA':'app.schema.schema'
}

```

```
cd app/

python manage.py shell
from cassandra.models import Cassandra
Cassandra.objects.create(FirstName="Aman",LastName="Mirza",Age=21,Description="complete info",url="https://track1.com")

```

<h1>Schema.py in cassandra folder</h1>

```
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

```

<h1>Schema.py in app folder</h1>

```

import graphene 
import cassandra.schema

class Query(cassandra.schema.Query,graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query)

```

<h1>urls.py in app folder</h1>

```

from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/',csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

```


<h1>Adding Mutations In schema.py in app folder and in cassanda folder</h1>

```

cd cassandra/

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
    
    
```

```

cd app/
import graphene 
import cassandra.schema

class Query(cassandra.schema.Query,graphene.ObjectType):
  pass

class Mutation(cassandra.schema.Mutation,graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query ,mutation=Mutation)


```


<h1>Adding user folder</h1>

```

from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # only_fields = ('id','email','password','username')


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self,info,username,password,email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    
```

```

cd app/schema.py

import graphene 
import cassandra.schema
import users.schema
class Query(cassandra.schema.Query,graphene.ObjectType):
  pass

class Mutation(users.schema.Mutation,cassandra.schema.Mutation,graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query ,mutation=Mutation)

```

<h1>Quering User By ID </h1>

```

cd users/schema.py

from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # only_fields = ('id','email','password','username')

class Query(graphene.ObjectType):
    user = graphene.Field(UserType,id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self,info,id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self,info):
        user = info.context.user 
        if user.is_anonymous:
            raise Exception('Not loggged in!')
        return user
        
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self,info,username,password,email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    
    
````

```

cd app/schema.py

import graphene 
import cassandra.schema
import users.schema
class Query(users.schema.Query,cassandra.schema.Query,graphene.ObjectType):
  pass

class Mutation(users.schema.Mutation,cassandra.schema.Mutation,graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query ,mutation=Mutation)

```





  
