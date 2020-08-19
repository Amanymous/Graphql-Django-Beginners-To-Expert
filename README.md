# Graphql-Django-Beginners-To-Expert
https://dev.to/pydorax/an-intro-to-graphql-with-django-16e1
https://dev.to/pydorax
follow these links also for more information

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

<h1>User Authentication with Django-GraphQL-JWT</h1>

```
cd app/settings.py

"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cge*=d(da8^5#bax0(tt=2wsrpsc$isaz)pjq^8m!mqjf6z+!@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

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
GRAPHENE = {
    'SCHEMA':'app.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ]
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

   
]

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

```

```
cd users/schema.py

def resolve_me(self,info):
        user = info.context.user 
        if user.is_anonymous:
            raise Exception('Not loggged in!')
        return user
        
````

```

cd app/schema.py

import graphene 
import cassandra.schema
import users.schema
import graphql_jwt

class Query(users.schema.Query,cassandra.schema.Query,graphene.ObjectType):
  pass

class Mutation(users.schema.Mutation,cassandra.schema.Mutation,graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query ,mutation=Mutation)


```



















  
