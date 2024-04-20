from django import forms
from .models import Absence
from .autre_models import MembrePersonnel
from django.core.exceptions import ValidationError
from datetime import datetime


class FichePersonnelForm(forms.ModelForm):
    nom = forms.CharField(label="Nom :", widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(label="Prénom :", widget=forms.TextInput(attrs={'class': 'form-control'}))
    matricule = forms.IntegerField(label="Matricule :", widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.ChoiceField(label="Grade :", choices=(('Soldat deuxieme classe','Soldat deuxième classe'),
        ('Soldat première classe','Soldat prémière classe'),
        ('Caporal','Caporal'),
        ('Caporal chef','Caporal chef'),
        ('Sergent', 'Sergent'),
        ('Sergent chef','Sergent Chef'),
        ('Adjudant','Adjudant'),
        ('Adjudant chef','Adjudant chef'),
        ('Aspirant','Aspirant'),
        ('Sous lieutenant','Sous lieutenant'),
        ('Lieutenant','Lieutenant'),
        ('Capitaine','Capitaine'),
        ('Commandant','Commandant'),
        ('Lieutenant colonel','Lieutenant colonel'),
        ('Colonel','Colonel'),
        ('Colonel major','Colonel major'),
        ('Géneral de brigade aerienne','Géneral de brigade aerienne'),
        ('Géneral de division','Géneral de division'),
        ("Géneral de corps d'armée", "Géneral de corps d'armée"),
        ("Géneral d'armée","Géneral d'armée")

    ), widget=forms.Select(attrs={'class': 'form-control',}))
    naissance = forms.DateField(label="Date de naissance :", widget=forms.DateInput(attrs={'class': 'form-control',}))
    sexe = forms.ChoiceField(label="Sexe :", choices=(('M', 'Masculin'), ('F', 'Féminin')), widget=forms.Select(attrs={'class': 'form-control'}))
    service = forms.ChoiceField(label="Service :",choices=(('SGMA1','SGMA1'),('SGMA2','SGMA2'),('SGMA3','SGMA3'),('SGAS','SGAS'),('SGMMR','SGMMR'),('SGRT','SGRT'),('BCT','BCT'),('BST','BST'),('BPI','BPI'),('BTD','BTD'),('Secretariat','Secretariat'),('Comptabilité','Comptabilité'),('Fourier','Fourier')), widget=forms.Select(attrs={'class': 'form-control',}))
    numero = forms.IntegerField(label="Numéro de téléphone :", widget=forms.NumberInput(attrs={'class': 'form-control',}))
    email = forms.EmailField(label="Email :", widget=forms.EmailInput(attrs={'class': 'form-control',}))
    photo = forms.ImageField(label="Image", required=False)

    class Meta:
        model = MembrePersonnel
        fields = ['nom', 'prenom', 'naissance', 'sexe', 'matricule', 'grade', 'service', 'numero', 'email', 'photo']


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = [
            'personnel',
            'type_absence',
            'date_depart',
            'heure_depart',
            'date_arrivee',
            'heure_arrivee',
            'motif_pcd',
            'motif_pld',
            'motif_asm',
            'motif_repos_medical',
            'motif_service_interieur',
        ]
        labels = {
            'personnel': 'Membre du personnel',
            'type_absence': 'Type d\'absence',
            'date_depart': 'Date de départ',
            'heure_depart': 'Heure de départ',
            'date_arrivee': 'Date d\'arrivée',
            'heure_arrivee': 'Heure d\'arrivée',
            'motif_pcd': 'Motif PCD',
            'motif_pld': 'Motif PLD',
            'motif_asm': 'Motif ASM',
            'motif_repos_medical': 'Motif repos médical',
            'motif_service_interieur': 'Motif service intérieur',
        }
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-control'}),
            'type_absence': forms.Select(attrs={'class': 'form-control'}),
            'date_depart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_depart': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'date_arrivee': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_arrivee': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motif_pcd': forms.Select(attrs={'class': 'form-control'}),
            'motif_pld': forms.Select(attrs={'class': 'form-control'}),
            'motif_asm': forms.Select(attrs={'class': 'form-control'}),
            'motif_repos_medical': forms.Select(attrs={'class': 'form-control'}),
            'motif_service_interieur': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Masquer les champs de motifs spécifiques par défaut
        self.fields['motif_pcd'].widget.attrs.update({'hidden': True})
        self.fields['motif_pld'].widget.attrs.update({'hidden': True})
        self.fields['motif_asm'].widget.attrs.update({'hidden': True})
        self.fields['motif_repos_medical'].widget.attrs.update({'hidden': True})
        self.fields['motif_service_interieur'].widget.attrs.update({'hidden': True})
    
        # Afficher les champs appropriés en fonction du type d'absence sélectionné
        type_absence = self.data.get('type_absence', self.initial.get('type_absence'))
        if type_absence:
            if type_absence == 'PCD':
                self.fields['motif_pcd'].widget.attrs.pop('hidden')
            elif type_absence == 'PLD':
                self.fields['motif_pld'].widget.attrs.pop('hidden')
            elif type_absence == 'ASM':
                self.fields['motif_asm'].widget.attrs.pop('hidden')
            elif type_absence == 'Repos_médical':
                self.fields['motif_repos_medical'].widget.attrs.pop('hidden')
            elif type_absence == 'Service_intérieur':
                self.fields['motif_service_interieur'].widget.attrs.pop('hidden')

"""class AbsenceForm(forms.ModelForm):
    # Ajout d'un champ pour le type d'absence
    type_absence = forms.ChoiceField(
        label='Type d\'absence',
        choices=Absence.TYPE_ABSENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    # Ajout de champs pour la nature et le lieu (si besoin)
    nature = forms.CharField(label='Nature', max_length=250, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lieu = forms.CharField(label='Lieu', max_length=250, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Absence
        fields = [
            'personnel',
            'type_absence',
            'motif',
            'date_depart',
            'heure_depart',
            'date_arrivee',
            'heure_arrivee',
            'duree_absence',
            'nature',
            'lieu'
        ]
        labels = {
            'personnel': 'Membre du personnel',
            'type_absence': 'Type d\'absence',
            'motif': 'Motif',
            'date_depart': 'Date de départ',
            'heure_depart': 'Heure de départ',
            'date_arrivee': 'Date d\'arrivée',
            'heure_arrivee': 'Heure d\'arrivée',
            'duree_absence': 'Durée d\'absence',
            'nature': 'Nature',
            'lieu': 'Lieu',
        }
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-control'}),
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'date_depart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_depart': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'date_arrivee': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': False}),
            'heure_arrivee': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': False}),
            'duree_absence': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),  # Lecture seule
            'nature': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Ajouter ici des validations personnalisées si nécessaire
        date_depart = cleaned_data.get('date_depart')
        heure_depart = cleaned_data.get('heure_depart')
        date_arrivee = cleaned_data.get('date_arrivee')
        heure_arrivee = cleaned_data.get('heure_arrivee')
        
        # Vous pouvez ajouter des validations spécifiques selon vos besoins
        if date_depart and date_arrivee and date_arrivee < date_depart:
            raise forms.ValidationError("La date d'arrivée doit être postérieure à la date de départ.")
        
        if date_depart and date_arrivee and date_arrivee == date_depart and heure_arrivee and heure_depart and heure_arrivee <= heure_depart:
            raise forms.ValidationError("L'heure d'arrivée doit être postérieure à l'heure de départ.")

        # Vous pouvez ajouter d'autres validations ici, selon vos besoins
        
        return cleaned_data
"""