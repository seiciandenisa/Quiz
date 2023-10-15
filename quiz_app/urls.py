from django.urls import path

from quiz_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start_game', views.start_game, name='start-game'),
    path('on_game', views.on_game, name='on-game'),
    path('finish', views.finish, name='finish'),
    path('ranking_view/', views.ranking_view, name='ranking-view'),
]
