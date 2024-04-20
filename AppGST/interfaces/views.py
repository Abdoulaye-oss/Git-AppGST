from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FichePersonnelForm, AbsenceForm
from .autre_models import MembrePersonnel
from django.db.models import Q, Sum
from datetime import datetime
from .models import Absence
from django.utils import timezone



@login_required
def accueil(request):
    # Récupérer tous les membres du personnel
    personnels = MembrePersonnel.objects.all()
    # Calculer le nombre total de personnels
    nombre_personnel = personnels.count()
    # Calculer le nombre de personnels absents et présents
    nombre_absent = personnels.filter(statut='Absent').count()
    nombre_present = personnels.filter(statut='Présent').count()
    # Obtenir la date actuelle et l'heure actuelle
    date_actuelle = datetime.now().date()
    heure_actuelle = datetime.now().time()
    date_actuelles = datetime.combine(date_actuelle, heure_actuelle)

    context = {
        'nombre_personnel': nombre_personnel,
        'nombre_absent': nombre_absent,
        'nombre_present': nombre_present,
        'date_actuelles': date_actuelles,
    }
    return render(request, 'pages/home.html', context)


# Gestion de personnel
@login_required
def list_personnel(request):
    personnels = MembrePersonnel.objects.all().order_by('prenom')
    context = {'personnels': personnels}
    return render(request, 'pages/list_personnel.html', context)

@login_required
def ajouter_personnel(request):
    if request.method == 'POST':
        form = FichePersonnelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('interfaces:list_personnel')  # Rediriger vers une page de succès
    else:
        form = FichePersonnelForm()
    return render(request, 'pages/ajouter_personnel.html', {'form': form})

@login_required
def info_personnel(request, matricule):
    personnel = MembrePersonnel.objects.get(matricule=matricule)
    context = {'personnel': personnel}
    return render(request, 'pages/info_personnel.html', context)

@login_required
def edit_personnel(request, matricule):
    personnel=MembrePersonnel.objects.get(matricule=matricule) 
    if request.method=='POST':
        form=FichePersonnelForm(request.POST, instance=personnel)
        if  form.is_valid:
            form.save()
            return redirect('interfaces:list_personnel')
    else:
        form=FichePersonnelForm(instance=personnel)
    context={
        'form':form,
    }
    return render(request, 'pages/edit_personnel.html',context)


@login_required
def delete_personnel(request, matricule):
    personnel=MembrePersonnel.objects.get(matricule=matricule)    
    if request.method == 'POST':
        # Si la requête est de type POST, cela signifie que l'utilisateur a confirmé la suppression
        personnel.delete()
        # Rediriger vers une page appropriée après la suppression, par exemple la liste des absences
        return redirect('interfaces:list_personnel')
    return render(request, 'pages/delete_personnel.html', {'personnel':personnel} )



#==========Gestion d'absence=========#

@login_required
def absence(request):
    personnels = MembrePersonnel.objects.all().order_by('prenom')
    absences = []

    for personnel in personnels:
        absences_personnel = Absence.objects.filter(personnel=personnel)
        statut_personnel = 'Présent'  # Par défaut, on suppose que le personnel est présent
        statut_absence= 'Passée'

        for absence in absences_personnel:
            depart = datetime.combine(absence.date_depart, absence.heure_depart)
            if absence.date_arrivee and absence.heure_arrivee:
                arrivee = datetime.combine(absence.date_arrivee, absence.heure_arrivee)
                # Vérifier si la date et l'heure actuelles sont entre le départ et l'arrivée
                if depart <= datetime.now() <= arrivee:
                    statut_personnel = 'Absent'
                    statut_absence='Actuelle'
                    break  # On peut arrêter de vérifier car on a trouvé un cas d'absence
            else:
                # Si absence n'a pas de date et heure d'arrivée, le personnel est considéré comme absent
                statut_personnel = 'Absent'
                statut_absence='Actuelle'
                break
        
        # Mettre à jour le statut du personnel si nécessaire
        personnel.statut = statut_personnel
        absence.statut=statut_absence
        personnel.save()
        absence.save()
        
        # Ajouter le personnel et sa dernière absence dans la liste des absences
        absences.append((personnel, absences_personnel.latest('id') if absences_personnel.exists() else None))

    context = {
        'absences': absences,
        'personnels': personnels,
    }
    return render(request, 'pages/absence.html', context)

@login_required
def historiques(request):
    absences=Absence.objects.order_by('-id')
    context={
        'absences':absences
    }
    return render(request, 'pages/historiques.html', context)

@login_required
def absences_personnel(request, matricule):
    # Récupérer le membre du personnel en fonction de son matricule
    personnel = get_object_or_404(MembrePersonnel, matricule=matricule)
    # Récupérer toutes les absences associées à ce membre
    absences = Absence.objects.filter(personnel=personnel).order_by('-id')
    nombre_heure = sum(absence.duree_absence for absence in absences if isinstance(absence.duree_absence, (int, float)))
    
    if absences.exists():
        message = ""
    else:
        message = "Aucune absence enregistrée pour ce membre du personnel."
    
    context = {
        'personnel': personnel,
        'absences': absences,
        'nombre_heure': nombre_heure,
        'message': message
    }
    
    return render(request, 'pages/absences_personnel.html', context)


@login_required
def ajouter_absence(request):
    personnels = MembrePersonnel.objects.all().order_by('prenom')
    context = {'personnels': personnels}
    return render(request, 'pages/ajouter_absence.html', context)

@login_required
def edit_absence(request, id):
    # Récupérer l'absence à éditer
    absence = get_object_or_404(Absence, id=id)
    message = ''  # Initialiser la variable message à une chaîne vide
    form = AbsenceForm(instance=absence)  # Initialiser le formulaire avec l'instance de l'absence à éditer
    message1 = ''  # Initialiser la variable message1 à une chaîne vide

    if absence.date_arrivee and absence.heure_arrivee:
        message = 'Désolé, vous ne pouvez pas modifier cette absence.'
    else:
        if request.method == 'POST':
            # Si le formulaire est soumis, créer une instance du formulaire avec les données soumises et l'instance de l'absence à éditer
            form = AbsenceForm(request.POST, instance=absence)
            if form.is_valid():
                absence = form.save(commit=False)
                absence_depart = datetime.combine(absence.date_depart, absence.heure_depart)
                if absence.date_arrivee and absence.heure_arrivee:
                    absence_arrivee = datetime.combine(absence.date_arrivee, absence.heure_arrivee)
                else:
                    absence_arrivee = None

                if absence_arrivee is None or absence_arrivee >= absence_depart:
                    # Si le formulaire est valide, sauvegarder les modifications
                    form.save()
                    return redirect('interfaces:absence')  # Rediriger vers une page appropriée après l'édition
                else:
                    message1 = "La date de départ doit être antérieure à la date d'arrivée."
            else:
                form = AbsenceForm(instance=absence)

    # Retourner la page avec les formulaires et les messages
    return render(request, 'pages/edit_absence.html', {'form': form, 'message': message, 'message1': message1})


@login_required
def delete_absence(request,id):
    # Récupérer l'absence à supprimer
    absence = get_object_or_404(Absence, id=id)
    
    if request.method == 'POST':
        # Si la requête est de type POST, cela signifie que l'utilisateur a confirmé la suppression
        absence.delete()
        # Rediriger vers une page appropriée après la suppression, par exemple la liste des absences
        return redirect('interfaces:historiques')
    
    # Si la requête est de type GET, afficher une page de confirmation de suppression
    return render(request, 'pages/delete_absence.html', {'absence': absence})


@login_required
def une_absence(request, matricule):
    personnel = MembrePersonnel.objects.get(matricule=matricule)
    
    # Vérifie s'il y a des absences pour ce personnel
    absences_exist = Absence.objects.filter(personnel=personnel).exists()
    
    if absences_exist:
        derniere_absence = Absence.objects.filter(personnel=personnel).latest('id')  # Récupère la dernière absence enregistrée
    else:
        derniere_absence = None
    
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            nouvelle_absence = form.save(commit=False)
            nouvelle_depart = datetime.combine(nouvelle_absence.date_depart, nouvelle_absence.heure_depart)
            if absences_exist:
                # Ne sauvegarde pas encore dans la base de données
                if derniere_absence.date_arrivee and derniere_absence.heure_arrivee:
                    derniere_arrivee = datetime.combine(derniere_absence.date_arrivee, derniere_absence.heure_arrivee)

                    if nouvelle_depart >= derniere_arrivee:
                    # Si la date de départ de la nouvelle absence est postérieure à la date d'arrivée de la dernière absence
                        form.save()
                        return redirect('interfaces:ajouter_absence')
                    else:
                    # Gérer l'erreur ici si la date de départ est antérieure à la date d'arrivée
                        print("La date de départ doit être postérieure à la date d'arrivée de la dernière absence.")
            else:
                form.save()
                return redirect('interfaces:absence')
        else:
            print(form.errors)
    else:
        form = AbsenceForm(initial={'personnel': personnel})  # Pré-remplir le champ personnel avec le membre du personnel concerné
    return render(request, 'pages/une_absence.html', {'form': form, 'derniere_absence': derniere_absence})



@login_required
def disponibilite(request):
    # Récupérer tous les membres du personnel
    personnels = MembrePersonnel.objects.all()

    # Calculer la durée totale d'absence pour chaque membre du personnel
    # Utiliser une sous-requête pour calculer la somme des heures d'absence pour chaque membre du personnel
    personnels = personnels.annotate(
        total_absence=Sum('absence__duree_absence')
    ).order_by('-total_absence')

    context = {
        'personnels': personnels
    }
    return render(request, 'pages/disponibilite.html', context)


@login_required
def rechercher(request):
    search = request.GET.get('search')
    # Recherche des membres du personnel
    personnels = MembrePersonnel.objects.filter(Q(nom__icontains=search)|
                                                Q(prenom__icontains=search)|
                                                Q(matricule__icontains=search)|
                                                Q(grade__icontains=search)|
                                                Q(service__icontains=search))
    if not personnels.exists():
        message = "Aucun résultat trouvé pour cette recherche."
    else:
        message = ""
    
    context = {
        'personnels': personnels,
        'message': message
    }
    return render(request, 'pages/rechercher.html', context)


@login_required
def rechercher_absence(request):
    # Récupérer le terme de recherche dans les requêtes GET
    search = request.GET.get('search', '').strip()
    
    # Filtrer les absences actuelles
    absences_actuelles = Absence.objects.filter(statut='Actuelle')
    
    # Filtrer par terme de recherche, en vérifiant si le terme de recherche n'est pas vide
    if search:
        les_absences = absences_actuelles.filter(
            Q(personnel__nom__icontains=search) |
            Q(personnel__prenom__icontains=search) |
            Q(personnel__grade__icontains=search) |
            Q(personnel__matricule__icontains=search) |
            Q(personnel__service__icontains=search) |
            Q(type_absence__icontains=search) |
            Q(motif_pcd__icontains=search) |
            Q(motif_pld__icontains=search) |
            Q(motif_asm__icontains=search) |
            Q(motif_service_interieur__icontains=search) |
            Q(motif_repos_medical__icontains=search)
        )
    else:
        les_absences = absences_actuelles
    
    # Créer le contexte pour le template
    context = {
        'les_absences': les_absences,
    }
    
    # Rendre le template avec le contexte
    return render(request, 'pages/rechercher_absence.html', context)


from django.views import View
from django.shortcuts import render
from .models import Absence
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

class HistogrammeAbsencesView(View):
    def get(self, request):
        # Récupérer les données des absences
        absences = Absence.objects.all()
        
        # Créer un dictionnaire pour stocker les durées d'absence par membre du personnel
        durees_absences = {}
        for absence in absences:
            # Récupérer le membre du personnel et la durée d'absence
            personnel = absence.personnel
            duree_absence = absence.duree_absence
            
            # Accumuler les durées d'absence pour chaque membre du personnel
            if personnel in durees_absences:
                durees_absences[personnel] += duree_absence
            else:
                durees_absences[personnel] = duree_absence
        
        # Trier les données par ordre décroissant de durée d'absence
        sorted_durees = sorted(durees_absences.items(), key=lambda x: x[1], reverse=True)  # Tri par durée d'absence
        
        # Extraire les noms et les durées d'absence pour les utiliser dans le graphique
        noms_personnel = [str(personnel) for personnel, duree in sorted_durees]
        durees = [duree for personnel, duree in sorted_durees]
        
        # Créer l'histogramme
        plt.figure(figsize=(10, 4))

        # Configurer le format du graphique
        plt.bar(noms_personnel, durees, color='blue', width=0.04)
        plt.xlabel('Membre du personnel')
        plt.ylabel('Somme des durées d\'absence (heures)')
        plt.title('Somme des durées d\'absence par membre du personnel')

        # Enregistrer le graphique en tant qu'image dans un objet BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        
        # Encoder l'image en base64
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Passer l'image en base64 au template
        img_src = f'data:image/png;base64,{img_base64}'

        # Rendre le template avec l'image du graphique
        return render(request, 'pages/absences_histogram_view.html', {'img_src': img_src})

       
from django.views import View
from django.shortcuts import render
from .models import Absence
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

class HistogrammeAbsencesViews(View):
    def get(self, request):
        # Récupérer les données des absences
        absences = Absence.objects.all()
        
        # Créer des listes pour stocker les noms de personnel et les durées d'absence pour chaque catégorie
        noms_personnel_asm = []
        durees_asm = []
        noms_personnel_repos_medical = []
        durees_repos_medical = []
        noms_personnel_pcd_problemes_sociaux = []
        durees_pcd_problemes_sociaux = []
        
        # Parcourir toutes les absences
        for absence in absences:
            personnel = absence.personnel
            duree_absence = absence.duree_absence
            
            # Vérifier le type d'absence et les motifs spécifiques
            if absence.type_absence == 'ASM':
                noms_personnel_asm.append(str(personnel))
                durees_asm.append(duree_absence)
            elif absence.type_absence == 'Repos_médical':
                noms_personnel_repos_medical.append(str(personnel))
                durees_repos_medical.append(duree_absence)
            elif absence.type_absence == 'PCD' and absence.motif_pcd == 'Problemes_sociaux':
                noms_personnel_pcd_problemes_sociaux.append(str(personnel))
                durees_pcd_problemes_sociaux.append(duree_absence)
        
        # Créer l'histogramme
        plt.figure(figsize=(10, 6))

        # Tracer les durées d'absence pour chaque catégorie
        plt.bar(noms_personnel_asm, durees_asm, color='red', width=0.4, label='ASM')
        plt.bar(noms_personnel_repos_medical, durees_repos_medical, color='green', width=0.4, label='Repos médical')
        plt.bar(noms_personnel_pcd_problemes_sociaux, durees_pcd_problemes_sociaux, color='blue', width=0.4, label='PCD - Problèmes sociaux')
        
        # Configurer les étiquettes et le titre du graphique
        plt.xlabel('Membre du personnel')
        plt.ylabel('Somme des durées d\'absence (heures)')
        plt.title('Somme des durées d\'absence par membre du personnel et par type')
        
        # Ajouter une légende pour les différentes catégories
        plt.legend()
        
        # Enregistrer le graphique en tant qu'image dans un objet BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        
        # Encoder l'image en base64
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Passer l'image en base64 au template
        img_src = f'data:image/png;base64,{img_base64}'

        # Rendre le template avec l'image du graphique
        return render(request, 'pages/absences_histogram_view.html', {'img_src': img_src})
