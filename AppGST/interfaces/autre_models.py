from django.db import models
class MembrePersonnel(models.Model):
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    GRADE_CHOICES = (
        ('Soldat deuxieme classe','Soldat deuxième classe'),
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

    )

    SERVICE_CHOICES = (
        ('SGMA1','SGMA1'),
        ('SGMA2','SGMA2'),
        ('SGMA3','SGMA3'),
        ('SGAS','SGAS'),
        ('SGMMR','SGMMR'),
        ('SGRT','SGRT'),
        ('BCT','BCT'),
        ('BST','BST'),
        ('BPI','BPI'),
        ('BTD','BTD'),
        ('Secretariat','Secretariat'),
        ('Comptabilité','Comptabilité'),
        ('Fourier','Fourier'),
       
    )
    STATUT_CHOICES=(
        ('Présent','Présent'),
        ('Absent','Absent')
    )
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    naissance = models.DateField(verbose_name="Date de naissance")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    matricule = models.CharField(primary_key=True, max_length=50, verbose_name="Matricule")
    grade = models.CharField(max_length=30, choices=GRADE_CHOICES, verbose_name="Grade")
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, verbose_name="Service")
    numero = models.IntegerField(verbose_name="Numéro de téléphone")
    email = models.EmailField(verbose_name="Email")
    photo = models.ImageField(upload_to='photos/', verbose_name="Photo")
    statut=models.CharField(max_length=30, default='Présent', choices=STATUT_CHOICES, verbose_name="Statut")



    def __str__(self):
        return f"{self.nom} {self.prenom}"
