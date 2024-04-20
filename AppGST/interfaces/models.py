from django.db import models
from datetime import datetime, timedelta

class Absence(models.Model):
    # Choix de type d'absence
    TYPE_ABSENCE_CHOICES = (
        ('ASM', 'ASM'),
        ('PLD', 'PLD'),
        ('PCD', 'PCD'),
        ('Repos_médical', 'Repos médical'),
        ('Service_intérieur', 'Service intérieur'),
    )

    # Choix de motifs pour chaque type d'absence
    MOTIF_PCD_CHOICES = (
        ('Recuperation_de_travail', 'Récupération de travail'),
        ('Recuperation_de_garde', 'Récupération de garde'),
        ('Affaires_administratives', 'Affaires administratives'),
        ('Recuperation_apres_mission', 'Récupération après retour de mission'),
        ('Problemes_sociaux', 'Problèmes sociaux'),
        ('Recuperation_de_permanence', 'Récupération de permanence'),
        ('Preparation_a_la_garde', 'Préparation à la garde'),
    )

    MOTIF_PLD_CHOICES = (
        ('Droit_annuel', 'Droit annuel'),
    )

    MOTIF_SERVICE_INTERIEUR_CHOICES = (
        ('Garde', 'Garde'),
        ('Mission', 'Mission'),
        ('Detache', 'Détaché'),
        ('Cours', 'Cours')
    )

    MOTIF_REPOS_MEDICAL_CHOICES = (
        ('Repos_médical', 'Repos médical'),
        ('PTC','PTC'),
        ('Consultation_médicale', 'Consultation médicale'),
    )

    MOTIF_ASM_CHOICES = (
        ('ASM', 'ASM'),
        ('Retard','Retard')
    )
    STATUT_CHOICES=(
        ('Actuelle','Actuelle'),
        ('Passée','Passée')
    )

    # Champs du modèle
    personnel = models.ForeignKey('MembrePersonnel', on_delete=models.CASCADE)
    type_absence = models.CharField(max_length=250, choices=TYPE_ABSENCE_CHOICES, default='ASM')

    date_depart = models.DateField(null=True)
    heure_depart = models.TimeField(null=True)
    date_arrivee = models.DateField(blank=True, null=True)
    heure_arrivee = models.TimeField(blank=True, null=True)

    # Champ pour stocker la durée d'absence en heures
    duree_absence = models.FloatField(default=0.0)

    # Champs de motifs spécifiques pour chaque type d'absence
    motif_pcd = models.CharField(max_length=50, choices=MOTIF_PCD_CHOICES, null=True, blank=True)
    motif_pld = models.CharField(max_length=50, choices=MOTIF_PLD_CHOICES, null=True, blank=True)
    motif_asm = models.CharField(max_length=50, choices=MOTIF_ASM_CHOICES, null=True, blank=True)
    motif_repos_medical = models.CharField(max_length=50, choices=MOTIF_REPOS_MEDICAL_CHOICES, null=True, blank=True, default='Repos_médical')
    motif_service_interieur = models.CharField(max_length=50, choices=MOTIF_SERVICE_INTERIEUR_CHOICES, null=True, blank=True)
    statut=models.CharField(max_length=30, default='Passée', choices=STATUT_CHOICES, verbose_name="Statut")



    def get_motif_specific(self):
        # Renvoie le motif spécifique en fonction du type d'absence
        if self.type_absence == 'PCD':
            return self.motif_pcd
        elif self.type_absence == 'PLD':
            return self.motif_pld
        elif self.type_absence == 'ASM':
            return self.motif_asm
        elif self.type_absence == 'Repos_médical':
            return self.motif_repos_medical
        elif self.type_absence == 'Service_intérieur':
            return self.motif_service_interieur
        return None  # Retourne None si aucun type d'absence ne correspond

    @property
    def motif_specific(self):
        return self.get_motif_specific()
    
    def save(self, *args, **kwargs):
        # Calcul de la durée d'absence si toutes les données sont présentes
        if self.date_depart and self.heure_depart and self.date_arrivee and self.heure_arrivee:
            depart = datetime.combine(self.date_depart, self.heure_depart)
            arrivee = datetime.combine(self.date_arrivee, self.heure_arrivee)
            if arrivee > depart:
                duree = (arrivee - depart).total_seconds() / 3600  # Convertir en heures
                self.duree_absence = round(duree, 2)
        super().save(*args, **kwargs)
