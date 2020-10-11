"""ncbaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from controlapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custermer pages management
    path('', views.homepage),
    path('index/', views.index),
    path('newslist/', views.newslist),
    path('newslist/<str:pageindex>/', views.newslist),
    path('news/<int:newsid>/', views.news),
    path('schedule/', views.schedule),
    path('schedule/<int:year>/', views.schedule),
    path('box/<int:year>/<str:datestr>/<int:number>/', views.box),
    path('standing/', views.standing),
    path('standing/<int:year>/', views.standing),
    path('teams/', views.teams),
    path('teams/<int:year>/', views.teams),
    path('teams/<int:year>/<int:teamid>/<str:itemtype>/', views.teams),
    path('player/<int:personid>/', views.player),
    path('rank/', views.rank),
    path('rank/<int:year>/', views.rank),
    path('activity/', views.activity),
    path('activity/<int:eventid>/', views.activity),
    path('repeatvote/', views.repeatvote),
    path('umpire/', views.umpire),
    path('umpire/<int:year>/', views.umpire),

    # Email verification
    path('mail/vote/<int:eventid>/<str:randomkey>/', views.mailvote),

    # Member management
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    
    # Member options
    path('option/', views.option),

    # Teams management
    path('teamadd/<int:year>/', views.teamadd),
    path('teamedit/<int:teamid>/', views.teamedit),
    path('teamdelete/<int:teamid>/', views.teamdelete),
    
    # Players management
    path('playeradd/<int:year>/', views.playeradd),
    path('playeradd/<int:year>/<str:teamid>/', views.playeradd),
    path('playeredit/<str:edittype>/<int:playerid>/', views.playeredit),
    
    # Games management
    path('gameadd/<int:year>/', views.gameadd),
    path('gameedit/<int:gameid>/<str:edittype>/', views.gameedit),
    path('gamenotplay/<int:year>/<int:gameid>/', views.gamenotplay),

    # Lineup list
    path('lineuplist/<int:year>/', views.lineuplist),
    path('lineup/<int:gameid>/', views.lineup),

    # Album url management
    path('album/<int:year>/', views.album),
    path('album/<int:year>/<int:gameid>/', views.album),
    
    # Game boxes management
    path('boxadd/<int:year>/', views.boxadd),
    path('boxadd/<int:year>/<int:gameid>/<str:itemtype>/', views.boxadd),
    path('boxedit/<int:gameid>/<str:itemtype>/<int:boxid>/<str:edittype>/', views.boxedit),
    
    # News management
    path('allnews/', views.allnews),
    path('newsadd/', views.newsadd),
    path('newsedit/<int:newsid>/<str:edittype>/', views.newsedit),

    # Team order management
    path('orderlist/<int:teamid>/', views.orderlist),
    path('order/<int:gameid>/<str:team>/', views.order),

    # Events management
    path('allevents/', views.allevents),
    path('eventadd/', views.eventadd),
    path('eventedit/<int:eventid>/<str:edittype>/', views.eventedit),

    # Vote options management
    path('itemadd/<int:eventid>/', views.itemadd),
    path('itemedit/<int:eventid>/<int:itemid>/', views.itemedit),
    path('itemdelete/<int:eventid>/<int:itemid>/', views.itemdelete),

]
