from django.shortcuts import render , redirect
from .models import *
from specialisation.models import * 
from django.contrib.auth.decorators import login_required
from datetime import datetime
import requests
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Sum
from .managers import ApiPost , Note ,DartAPI

apicodepost = ApiPost()
note = Note()
dart = DartAPI()


# Create your views here.
@login_required(login_url='connexion')
def coding(request, nom_epreuve):
    
    data = {}
    try:
        if request.user_agent.is_pc :
            templates_name = 'pages/livecoding/coding.html'
            try:

                code = Epreuve.objects.filter(status=True,nom=nom_epreuve)[:1].get()
                if not code.code.is_valid:
                    return redirect('home')
                code_id= code.code.pk
                code_id_lang = code.code.coding_in.lang_id
                code_nom_lang = code.code.coding_in.nom
                code_consigne = code.code.consige
                code_start = code.code.debut
                code_end = code.code.fin
                user = request.user
                user_resultat =  user.userresultat.filter(status=True,exercice__code__titre=code.code.titre,valider=True)
                print(user)
                print(code)
                print(code_id_lang)
                print(code_nom_lang)
                print(code.code.titre)
             
                deja_fait = []
                exo =  Exercice.objects.filter(status=True,code__pk=code_id)
                for t in user_resultat :
                    deja_fait.extend([ex.id for ex in exo if t.exercice == ex ])
                exo = exo.exclude(id__in=deja_fait)
                print(exo)
                if exo :
                    code_end = datetime.strftime(code_end,'%B %d, %Y %H:%M:%S')
                    code_start = datetime.strftime(code_start,'%B %d, %Y %H:%M:%S')
                    data = {
                            'exo':exo,
                            'code':code_nom_lang,
                            'id_lang':code_id_lang,
                            'code_start':code_start,
                            'code_end':code_end,
                            'user':user,
                            'consigne':code_consigne,
                            'code_id':code_id,
                            'nom_epreuve':nom_epreuve, 
                    }
                else :
                    return redirect('home')
            except:
                return redirect('profil')
   
        else:
            templates_name = 'pages/livecoding/connexion.html'
            

    except :        
    
        pass
    
    return render(request, templates_name,data)


def postCode(request):
    
    # url pour avoir le token
    base_url_post = 'https://api.judge0.com//submissions?base64_encoded=false&wait=false'
    
    cod = request.POST.get('contentA')
    lang_id = request.POST.get('id_lang')
    slug = request.POST.get('exo_slug')
    user = request.POST.get('user')
    code_id = request.POST.get('code_id')
    epreuve = request.POST.get('epreuve')
    print(user)
    print(epreuve)
    print('slug------',slug)
    get_exo = Exercice.objects.filter(status=True,titre_slug=slug)[:1].get()
    get_test = TestValidation.objects.filter(status=True,exercice=get_exo)
    compter = len(get_test)
    print('code----------' ,cod)
    
    tester  = ''
    output = ''
    resultat =''
    compt = 0
    ################ TEST CODE ###################
    for test in get_test:
        tester = test.code_test
        output = test.resultat
        codepost = cod + "\n" + tester
        ######## POST CODE ###################
        if lang_id == '100':
            ######## POST CODE DART ###################
            datas = dart.postCodeDart(codepost,output)
            print (datas)
            if datas['valide']== False:
                break
            compt+=1      
        else:
            ######## POST CODE AUTRE ###################
            staus, datas = apicodepost.postCode(codepost, lang_id, output)
            datapi = datas
            print("status:", datapi['status']['id'])
            if datapi['status']['id'] > 3:  
                break
            compt+=1     
        
    print(compter, compt)
    valider = False
    if compt == compter:
        resultat = "Valider"
        valider = True
        succes = True

    else:
        valider = False
        nan = user+'-$'
        compt += 1
        resultat = "{user} Vous avez echouer au test numero {compt} :{tester} ; resultat attendu : {output}".format(user=nan,compt=compt,tester=tester,output=output)
        succes = False
    
    try:
        get_exercice_user = Exercice.objects.filter(status=True,titre_slug=slug)[:1].get()
        user = User.objects.filter(username=user,)[:1].get()
        save_exo = ResultatExercice.objects.filter(user=user, exercice=get_exercice_user)[:1].get()
        if save_exo.valider == False : 
            save_exo.nb_tentative += 1
            save_exo.code = cod
            save_exo.valider = valider
            
        else:
            resultat = "Vous avez deja valider Ce quest "
  
        save_exo.save()
        print(save_exo.nb_tentative)
    except :
        tantative = 1
        save_exo = ResultatExercice(user = user, nb_tentative = tantative , code = cod, valider = valider, exercice=get_exercice_user)
        save_exo.save()
        ###### CALCUL NOTE USER : LIVECODING ######
    try:
        get_user_valider = ResultatExercice.objects.filter(user = user , valider = True ,exercice__code__pk=code_id).count()
    except :
        get_user_valider = 0
    
    print(get_user_valider)
    sum_tentative = ResultatExercice.objects.filter(user=user,exercice__code__pk=code_id).aggregate(Sum('nb_tentative'))
    sum_user_tentative = sum_tentative['nb_tentative__sum']
    print(sum_user_tentative)
    exo =  Exercice.objects.filter(status=True,code__pk=code_id).count()
    print(exo)
    
    note_user = note.CalCpourcentage(get_user_valider,sum_user_tentative,exo)
    if note_user <= 0:
        note_user = 0 
    print(note_user)
    get_livecoding = Code.objects.filter(status = True , pk=code_id)[:1].get()
    epreuve_save = Epreuve.objects.filter(status=True,nom=epreuve)[:1].get()
    try:
        get_user_resultat_note = ResultatEpreuve.objects.filter(user=user , epreuve = epreuve_save , code = get_livecoding)[:1].get()
        get_user_resultat_note.note = note_user
        get_user_resultat_note.save()
        print('update ok')

    except :
 
        save_resultat = ResultatEpreuve(user = user, epreuve = epreuve_save , code = get_livecoding , note = note_user )
        save_resultat.save()
        print('save ok')
    datas = {
        'succes':succes,
        'resultat': resultat
    }
    return JsonResponse(datas, safe=False)

def postCodeTest(request):

    # url pour avoir le token
    base_url_post = 'https://api.judge0.com//submissions?base64_encoded=false&wait=false'
        

    cod = request.POST.get('contentA')
    lang_id = request.POST.get('id_lang')

    print('code----------' ,cod)
    if lang_id == '100' :
        
    ######## POST CODE TEST DART ###################
        datas = dart.postCodeTestDart(cod)
        if datas['error']== True:
            resultat = datas['message']
            print("ici")
        else : 
            resultat = datas['resultat']
            print("else")
            print(datas)

        print (datas)
        
    else:
        data = {
            'source_code': cod ,
            'language_id': lang_id,

        }
        req = requests.post(base_url_post, data = data)
        token = req.text
        data = json.loads(token)
        token= data['token']
        print(token)
        base_url_get = 'https://api.judge0.com/submissions/{}?base64_encoded=false'.format(token)
        reqapi=requests.get(base_url_get)
        reponse = reqapi.text

        datapi = json.loads(reponse)

        while datapi['status']['id'] == 1 or datapi['status']['id'] == 2 :
        
            reqapi=requests.get(base_url_get)
            reponse = reqapi.text
            datapi = json.loads(reponse)

        if datapi['status']['id'] == 3:
            
            resultat = datapi['stdout']
            
        elif  datapi['status']['id'] ==7:
            
            resultat=datapi['status']['description']
            
        elif  datapi['status']['id'] ==11:
            
            resultat = datapi['stderr']
            
        else:
            resultat=datapi['status']['description']
            
    print(resultat)
    # print(reqapi.status_code)
    # print(reponse)
    datas = {
        'succes':True,
        'resultat': resultat
    }
    return JsonResponse(datas, safe=False)





