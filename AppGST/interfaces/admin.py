from django.contrib import admin
from .models import Absence
from .autre_models import MembrePersonnel


admin.site.site_header='Administration de GST-FRA'
admin.site.site_title='GST-FRA'


class AdminMembrePersonnel(admin.ModelAdmin):
    search_fields= ['nom', 'prenom', 'naissance', 'sexe', 'matricule', 'grade', 'service', 'numero', 'email', 'photo','statut']
    list_display = ['nom', 'prenom', 'naissance', 'sexe', 'matricule', 'grade', 'service', 'numero', 'email', 'photo','statut']
    #readonly_fields=['nom', 'prenom', 'naissance', 'sexe', 'matricule', 'grade', 'service', 'numero', 'email', 'photo','statut']
    ordering=('prenom',)
admin.site.register(MembrePersonnel, AdminMembrePersonnel)


class AdminAbsence(admin.ModelAdmin):
    # Configuration de l'interface d'administration
    ordering = ['date_depart', 'heure_depart', 'date_arrivee', 'heure_arrivee']
    
    list_display = [
        'personnel',
        'type_absence',
        'date_depart',
        'heure_depart',
        'date_arrivee',
        'heure_arrivee',
        'duree_absence',
        'get_motif_specific',
    ]
    
    def duree_absence(self, obj):
        # Affiche la durée d'absence en heures avec arrondi à 2 décimales
        return round(obj.duree_absence, 2)
    duree_absence.short_description = "Durée d'absence (en heures)"
    
    def get_motif_specific(self, obj):
        # Affiche les motifs spécifiques en fonction du type d'absence
        if obj.type_absence == 'PCD':
            return obj.motif_pcd
        elif obj.type_absence == 'PLD':
            return obj.motif_pld
        elif obj.type_absence == 'ASM':
            return obj.motif_asm
        elif obj.type_absence == 'Repos_medical':
            return obj.motif_repos_medical
        elif obj.type_absence == 'Service_interieur':
            return obj.motif_service_interieur
        return None
    
    get_motif_specific.short_description = "Motif spécifique"

admin.site.register(Absence, AdminAbsence)
