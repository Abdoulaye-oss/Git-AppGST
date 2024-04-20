from django.contrib import admin
from django.urls import path
from . import views
from .views import HistogrammeAbsencesView, HistogrammeAbsencesViews



app_name='interfaces'
urlpatterns = [
    path('',views.accueil, name='accueil'),
    path('rechercher/', views.rechercher, name='rechercher'),
    path('rechercher_absence/', views.rechercher_absence, name='rechercher_absence'),

    
    path('ajouter_personnel/', views.ajouter_personnel, name='ajouter_personnel'),
    path('list_personnel/', views.list_personnel, name='list_personnel'),
    path('info_personnel/<int:matricule>/', views.info_personnel, name='info_personnel'),
    path('delete_personnel/<int:matricule>/', views.delete_personnel, name='delete_personnel'),
    path('edit_personnel/<int:matricule>/', views.edit_personnel, name='edit_personnel'),


    path('ajouter_absence/', views.ajouter_absence, name='ajouter_absence'),
    path('une_absence/<int:matricule>/', views.une_absence, name='une_absence'),
    path('historiques/', views.historiques, name='historiques'),
    path('absence/', views.absence, name='absence'),
    path('absences_personnel/<int:matricule>/', views.absences_personnel, name='absences_personnel'),
    path('edit_absence/<int:id>/', views.edit_absence, name='edit_absence'),
    path('delete_absence/<int:id>/', views.delete_absence, name='delete_absence'),
    path('disponibilite/', views.disponibilite, name='disponibilite'),


    path('histogramme-absences/', HistogrammeAbsencesView.as_view(), name='histogramme-absences'),
    path('histogramme-absences_anote/', HistogrammeAbsencesViews.as_view(), name='histogramme-absences_anote'),


]