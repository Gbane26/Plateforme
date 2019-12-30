from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
from quizz_app import models as models_quizzapp
from django.contrib.auth.models import User
from .models import *
from django.db.models import Avg
from livecoding import models as livecoding_models
import traceback
from apscheduler.schedulers.background  import BackgroundScheduler
# Create your views here.

def connexion(request):
    # ramener sur la page de home une foi connecter
    try:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'pages/login.html')
    except:
        return redirect('home')

def islogin(request):
    try:
        postdata = json.loads(request.body.decode('utf-8'))
        UserModel = get_user_model()
        # name = postdata['name']

        email = postdata['email']
        password = postdata['password']
        
        isSuccess=False
        try:
            u = UserModel.objects.get(email=email)
            username = u.username

            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_active:
                # print("user is login")
                isSuccess = True
                login(request, user)

                datas = {
                    'success':True,
                    'email':email,
                    'message':'Votre connection a reussi avec succes',
                }
                return JsonResponse(datas,safe=False) # page si connect
                    
            else:
                data = {
                'success':False,
                'message':'Vos identifiants ne sont pas correcte',
                }
                return JsonResponse(data,safe=False)
            return JsonResponse(datas, safe=False)
        except:
            data = {
            'success':False,
            'message':'Vos identifiants ne sont pas correcte',
            }
            return JsonResponse(data,safe=False)
    except:
        return redirect('home')


@login_required(login_url='connexion')
def home(request):
    try:
        try:
            data = {
                'specialite': request.user.user_specialite.specialite,
                'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
            }
            return render(request, 'pages/epreuve.html', data)
        except:
            return redirect('specialisation')
    except:
        return redirect('home')

@login_required(login_url='connexion')
def epreuve(request, nom_epreuve):
    try:
        spe = request.user.user_specialite.specialite
        #cour = Cours.objects.filter(status=True)
        epreuve = spe.epreuve_specialite.filter(nom=nom_epreuve)[:1].get()
        try:
            # print('debut search quizz')
            quizz = models_quizzapp.QuizzUser.objects.filter(user=request.user.id).filter(quizz=epreuve.quizz.id).get()
            # print('fin search quizz')
            hasquizz = True
        except:
            hasquizz = False
            # print('except has quizz')
        # video = RessourceVideo.objects.all()
        data = {
            'hasquizz': hasquizz,
            'specialite': spe,
            'epreuve': epreuve,
            'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
            # 'video': video,
        }
        # print('debut render')
        return render(request, 'pages/lesson.html', data)
    except:
        return redirect('home')

@login_required(login_url='connexion')
def profil(request):
    try:
        spe = request.user.user_specialite.specialite
        user_info = UserSpecialite.objects.filter(user_id=request.user.id)
        classement = sorted(ResultatEpreuve.objects.filter(epreuve__specialite__nom=spe.nom).distinct('user'), key=lambda t: (t.moyenne, t.duree_total) , reverse=True)
        # print(classement)

        # classement = ResultatEpreuve.objects.filter(epreuve__specialite__nom = spe.nom).order_by('moyenne').distinct('user')
        # user_resultat = ResultatEpreuve.objects.filter(user_id=request.user.id).order_by('date_add')
        # user_resultat = ResultatEpreuve.objects.select_related().get()
        # user_quizz = QuizzUser.objects.filter(user_id=request.user.id)
        # all_user = []
        # for user in classement:
        #     userss = User.objects.filter(username=user.user)
        #     all_user.append(userss)
        user_resultat_count = ResultatEpreuve.objects.filter(user_id=request.user.id).count()
        user_classement_by_quizz = []
        user_classement_by_coding = []
        if user_resultat_count <= 0:
            # print("je suis la")
            data= {
                'specialite': request.user.user_specialite.specialite,
                'user_info': user_info,
                'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
                'classement': classement,
                # 'userss': userss,
            }
        else:
            user_resultat = ResultatEpreuve.objects.filter(user_id=request.user.id).order_by('-date_add')
            specialite_quizz = models_quizzapp.Quizz.objects.filter(specialite=spe).count()
            specialite_coding = livecoding_models.Code.objects.filter(specialite=spe).count()
            print(specialite_coding)
            # specialite_livecoding = livecoding_models.Exercice.objects.filter(specialite=spe).count()
            specialite_all_user = UserSpecialite.objects.filter(specialite=spe).count()
            if specialite_quizz == 0 and specialite_coding == 0:
                data= {
                'user_info': user_info,
                'user_resultat': user_resultat,
                'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
                'classement': classement,
                # 'userss': userss,
                }
            elif  specialite_quizz > 0 :
                specialite_quizz = models_quizzapp.Quizz.objects.filter(specialite=spe).all()
                for item in specialite_quizz:
                    query = sorted(models_quizzapp.QuizzUser.objects.filter(quizz=item, issubmit="True"), key=lambda t: (t.note, t.duree_for_classement) , reverse=True)
                    print(query)
                    user_classement_by_quizz.append(query)
                
                # print(specialite_quizz, specialite_all_user)
                data= {
                    'user_info': user_info,
                    'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
                    'classement': classement,
                    'specialite_all_user': specialite_all_user,
                    'user_classement_by_quizz': user_classement_by_quizz,
                    }
            elif specialite_coding > 0:
                specialite_coding = livecoding_models.Code.objects.filter(specialite=spe).all()
                for item in specialite_coding:
                    query = sorted(ResultatEpreuve.objects.filter(code=item), key=lambda t: (t.note), reverse=True)
                    print(query)
                    user_classement_by_coding.append(query)
                
                # print(specialite_quizz, specialite_all_user)
                data= {
                    'user_info': user_info,
                    'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
                    'classement': classement,
                    'specialite_all_user': specialite_all_user,
                    'user_classement_by_coding': user_classement_by_coding,
                    }
            else:
                specialite_quizz = models_quizzapp.Quizz.objects.filter(specialite=spe).all()
                specialite_coding = livecoding_models.Code.objects.filter(specialite=spe).all()
                for item in specialite_quizz:
                    query = sorted(models_quizzapp.QuizzUser.objects.filter(quizz=item), key=lambda t: (t.note, t.duree_for_classement) , reverse=True)
                    print(query)
                    user_classement_by_quizz.append(query)
                for items in specialite_coding:
                    query = sorted(ResultatEpreuve.objects.filter(code=items), key=lambda t: (t.note), reverse=True)
                    print(query)
                    user_classement_by_coding.append(query)
                
                # print(specialite_quizz, specialite_all_user)
                data= {
                    'user_info': user_info,
                    'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
                    'classement': classement,
                    'specialite_all_user': specialite_all_user,
                    'user_classement_by_quizz': user_classement_by_quizz,
                    'user_classement_by_coding': user_classement_by_coding,

                }    
        return render(request, 'pages/profil.html', data)
    except Exception:
        traceback.print_exc()
        return redirect('home')

@login_required(login_url='connexion')
def pdf(request, id):
    try:
        fichier = RessourcePdf.objects.get(pk=id)
        data = {
            'fichier': fichier
        }
        # print (fichier)
        return render(request, 'pages/pdf.html', data)
    except:
        return redirect('home')


@login_required(login_url='connexion')
def quizz(request, nom_epreuve):
    spe = request.user.user_specialite.specialite
    epreuve = spe.epreuve_specialite.filter(nom=nom_epreuve)[:1].get()
    try:
        quizz = models_quizzapp.QuizzUser.objects.filter(user=request.user.id).filter(quizz=epreuve.quizz.id)[:1].get()
        return redirect('profil')
    except:
        quizz = models_quizzapp.QuizzUser(
            quizz = epreuve.quizz,
            user = request.user,
        )
        quizz.save()
        data= {
            'quizz': quizz,
            'specialite': spe,
            'epreuve': epreuve,
            'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
        }
        scheduler = BackgroundScheduler()
        scheduler.add_job(quizz.submit_quizz, 'date', run_date=quizz.quizz.datetime_valide)
        scheduler.start()
        return render(request, 'pages/quizz.html', data)


@login_required(login_url='connexion')
def quizz_valider(request, nom_epreuve):
    try:
        if request.method == 'POST':
            postdata = json.loads(request.body.decode('utf-8'))
            pk = postdata['reponse_user']
            value = postdata['value']
            reponse_user = models_quizzapp.ReponseUser.objects.get(pk=int(pk))
            reponse_user.reponses.clear()
            if type(value) == list:
                for v in value:
                    reponse_user.reponses.add(models_quizzapp.Reponse.objects.get(pk=int(v)))
                reponse_user.save()
            else:
                reponse_user.reponses.add(models_quizzapp.Reponse.objects.get(pk=int(value)))
                reponse_user.save()
            data = {
                    'success':True,
                    'pk':pk,
                    'value':value
                }
            return JsonResponse(data,safe=False)
        else:
            spe = request.user.user_specialite.specialite
            epreuve = spe.epreuve_specialite.filter(nom=nom_epreuve)[:1].get()
            quizz = models_quizzapp.QuizzUser.objects.filter(user=request.user.id).filter(quizz=epreuve.quizz.id)[:1].get()
            quizz.issubmit=True
            quizz.save()
            data = {
                    'success':True,
                    'pk':quizz.id,
                }
            return JsonResponse(data,safe=False)
    except:
        return redirect('home')

@login_required(login_url='connexion')
def specialisation(request):
    try:
        special = Specialite.objects.filter(status=True)
        data = {
            'user_profile': Profile.objects.filter(user_id=request.user.id).get(),
            'special': special,
        }
        return render(request, 'pages/specialisation.html', data)
    except:
        return redirect('home')

@login_required(login_url='connexion')
def special(request):
    try:
        postdata = json.loads(request.body.decode('utf-8'))
        demande = postdata['demande']
        isSuccess=False
        try:
            spe = request.user.user_specialite.specialite
            datas = {
                'success':False,
                'specialite':demande,
                'message':'Vous avez déja une spécialité',
            }
            return JsonResponse(datas,safe=False) 
        except:
            specialite = Specialite.objects.get(pk=int(demande))
            user = request.user
            UserSpecialite.objects.create(
                user = user,
                specialite = specialite
            )
            datas = {
                'success':True,
                'specialite':demande,
                'message':'Votre spécialité a été enregistrée avec succès',
            }
            return JsonResponse(datas,safe=False) # page si connect
    except:
        return redirect('home')

def result(request):
    return render(request, 'pages/resultat.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')
