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
python manage.py startapp tracks

```
<h3>Go to settings.py and add this</h3>

```

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'tracks'
]

```

<h3>Go to models.py and add this</h3>

```

from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth import get_user_model
# Create your models here.


class Track(models.Model):
    # id will be created automatically
    title = models.CharField(max_length=50)
    # we make it optional by using blank=True
    description = models.TextField(blank=True)
    url = models.URLField()
    # It is automatically populated
    created_at = models.DateTimeField(auto_now_add=True)
   
    
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
    'tracks'
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

<h1>Schema.py in tracks folder</h1>

```
import graphene
from .models import Track
from graphene_django import DjangoObjectType

class TrackType(DjangoObjectType):
    class Meta:
        model = Track

class Query(graphene.ObjectType):
    tracks = graphene.List(CassandraType)

    def resolve_tracks(self,info):
      return Track.object.all()

```

<h1>Schema.py in app folder</h1>

```

import graphene 
import tracks.schema

class Query(tracks.schema.Query,graphene.ObjectType):
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
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

```


<h1>Adding Mutations In schema.py in app folder and in tracks folder</h1>

```

cd tracks/

import graphene
from .models import Track
from graphene_django import DjangoObjectType

class CassandraType(DjangoObjectType):
    class Meta:
        model = Track

class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    def resolve_tracks(self,info):
      return Track.object.all()

# adding mutation
cd tracks/schema.py

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        track = Track(title=title, description=description,
                      url=url)
         track.save()
         return CreateTrack(track=track)

class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    
    
```

```

cd app/
import graphene
import tracks.schema

class Query(tracks.schema.Query,graphene.ObjectType):
  pass

class Mutation(tracks.schema.Mutation,graphene.ObjectType):
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
import tracks.schema
import users.schema

class Query(tracks.schema.Query,graphene.ObjectType):
  pass

class Mutation(users.schema.Mutation,tracks.schema.Mutation,graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query ,mutation=Mutation)

```

<h1>Quering User By ID </h1>

```

cd users/schema.py

import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql import GraphQLError


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # to return only the fields included
        # only_fields = ('id', 'email', 'password', 'username')


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Not logged in!')

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
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
import tracks.schema
import users.schema



class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query ,mutation=Mutation)

```

<h1>User Authentication with Django-GraphQL-JWT</h1>

```
cd app/settings.py

"""

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
SECRET_KEY = 's+rl)1ly1xw$i3*mlbq)r9tr10-!aowyokaoehis8j-@a58#4e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'tracks'
]


GRAPHENE = {
    'SCHEMA': 'app.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',    
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
import tracks.schema
import users.schema
import graphql_jwt


class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

```



















  
