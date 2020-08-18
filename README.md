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















  
