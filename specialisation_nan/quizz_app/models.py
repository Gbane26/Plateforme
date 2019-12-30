from django.db import models

# Create your models here.

# Projet_quizz
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from tinymce import HTMLField
from django.core.validators import MaxValueValidator, MinValueValidator
import pytz
from specialisation import models as specialisation


class Timemodels(models.Model):
    statut = models.BooleanField(default=True)
    date_add =  models.DateTimeField(auto_now_add=True)
    date_update =  models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
# class Specialisation(Timemodels):
#     """Model definition for Specialisation."""

#     # TODO: Define fields here
#     nom = models.CharField(max_length=50)
#     langage = models.CharField(max_length=50)
    
#     # @property
#     # def classement(self):
#     #     """Fonction pour faire le classement par spécialisation"""
#     #     return self.users.all().order_by('-moyenne_generale')

#     class Meta:
#         """Meta definition for Specialisation."""

#         verbose_name = 'Specialisation'
#         verbose_name_plural = 'Specialisations'

#     def __str__(self):
#         """Unicode representation of Specialisation."""
#         return self.nom


# class Profile(Timemodels):
#     """Model definition for UserProfile."""
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     image = models.ImageField(upload_to="profile", default="omar-sy-by-rachel.jpg")
#     specialisation = models.ForeignKey('Specialisation', related_name='users', on_delete=models.CASCADE, blank=True, null=True)
#     moyenne_generale = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
#     def save(self, *args, **kwargs):
#         self.moyenne_generale = self.get_moyenne_general()
#         super(Profile, self).save(*args, **kwargs)

    # def get_moyenne_general(self):
    #     """ Fonction qui recupère la moyenne de l'utilisateur """
    #     if self.specialisation:
    #         notes = sum([i.note for i in self.user.quizzs.all()])
    #         nb = self.specialisation.quizzs.filter(statut = True).count()
    #         return notes/nb
    #     else:
    #         return 0
    # @property
    # def get_specialisation_rang(self):
    #     """Fonction pour récupérer le classement de l'utilisateur par spécialisation"""
    #     return self.specialisation.all().order_by('-moyenne_generale')

    # @property
    # def get_general_rang(self):
    #     """Fonction pour récupérer le classement général de l'utilisateur"""
    #     pass
    
    # @property
    # def get_specialisation_sexe_rang(self):
    #     """Fonction pour récupérer le classement de l'utilisateur par spécialisation par sexe"""
    #     pass
    
    # @property
    # def get_general_sexe_rang(self):
    #     """Fonction pour récupérer le classement de l'utilisateur par spécialisation"""
    #     pass


    # class Meta:
    #     """Meta definition for UserProfile."""

    #     verbose_name = 'UserProfile'
    #     verbose_name_plural = 'UserProfiles'

    # def __str__(self):
    #     """Unicode representation of UserProfile."""
    #     return self.user.username
    
    # @classmethod
    # def classement_general(cls):
    #     return cls.objet.all().order_by('-moyenne_generale')
          
    # @property
    # def get_general_rang(self):
    #     """Fonction pour récupérer le classement général de l'utilisateur"""
    #     pass
    
    # @property
    # def get_specialisation_sexe_rang(self):
    #     """Fonction pour récupérer le classement de l'utilisateur par spécialisation par sexe"""
    #     pass
    
    # @property
    # def get_general_sexe_rang(self):
    #     """Fonction pour récupérer le classement de l'utilisateur par spécialisation"""
    #     pass
    
    # @classmethod
    # def classement_general(cls):
    #     return cls.objet.all().order_by('-moyenne_generale')


    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, created, **kwargs):
    #     instance.profile.save()

class Quizz(Timemodels):
    """Model definition for Quizz."""

    # TODO: Define fields here
    specialite = models.ForeignKey('specialisation.Specialite', related_name='quizzs', on_delete=models.CASCADE)
    titre = models.CharField(max_length=50)
    niveau = models.PositiveIntegerField()
    pourcentage = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="pourcentage pour valider")
    nbq = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], verbose_name="Nombre de questions par quizz", null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    duree = models.TimeField()
    
    def save(self, *args, **kwargs):
        if self.questions.filter(statut=True).count() < self.nbq:
            self.statut = False 
        super(Quizz, self).save(*args, **kwargs) # Call the real save() method

    @property
    def is_available(self):
        now = datetime.now()
        now = pytz.utc.localize(now)
        return self.date_debut < now <self.date_fin

    @property
    def time_available(self):
        return self.convert_timedelta(self.date_fin - pytz.utc.localize(datetime.now()))

    @property
    def is_comming(self):
        now = datetime.now()
        now = pytz.utc.localize(now)
        return  now < self.date_debut

    @property
    def time_comming(self):
        return self.convert_timedelta(self.date_debut - pytz.utc.localize(datetime.now()))
    
    @property
    def datetime_valide(self):
        return pytz.utc.localize(datetime.now()) + timedelta(hours=self.duree.hour, minutes=self.duree.minute, seconds=self.duree.second)


    def convert_timedelta(self, t):
        aux = str(t)
        li = aux.split()
        try:
            j = int(li[0])
        except:
            j=0
            li.insert(0, 0)
            li.insert(0, 0)
        re = li[2]
        tim = re.split(":")
        h = int(tim[0])
        m = int(tim[1])
        s = tim[2].split(".")
        s = int(s[0])
        return "{}j {}h {}min {}s".format(j, h, m, s)

    class Meta:
        """Meta definition for Quizz."""

        verbose_name = 'Quizz'
        verbose_name_plural = 'Quizzs'

    def __str__(self):
        """Unicode representation of Quizz."""
        return "{}: {}".format(self.specialite, self.titre)

class Question(Timemodels):
    """Model definition for Question."""

    # TODO: Define fields here
    quizz = models.ForeignKey('Quizz', related_name='questions', on_delete=models.CASCADE)
    niveau = models.PositiveIntegerField()
    contenu =  HTMLField('question_contenu')

    @property
    def ischeckbox(self):
        if len(self.liste_true)>1:
            return True
        else:
            return False

    @property
    def liste_true(self):
        aux = [i.id for i in self.reponses.filter(isrtue=True)]
        aux.sort()
        return aux

    def save(self, *args, **kwargs):
        if len(self.liste_true) ==0:
            self.statut = False 
        super(Question, self).save(*args, **kwargs)

    class Meta:
        """Meta definition for Question."""

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        """Unicode representation of Question."""
        return self.contenu

class Reponse(Timemodels):
    """Model definition for Reponse."""

    # TODO: Define fields here
    question = models.ForeignKey('Question', related_name='reponses', on_delete=models.CASCADE)
    contenu =  HTMLField('reponse_contenu')
    isrtue = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Reponse, self).save(*args, **kwargs)
        self.question.save()

    class Meta:
        """Meta definition for Reponse."""

        verbose_name = 'Reponse'
        verbose_name_plural = 'Reponses'

    def __str__(self):
        """Unicode representation of Reponse."""
        return self.contenu

class QuizzUser(Timemodels):
    """Model definition for QuizzUser."""

    # TODO: Define fields here
    quizz = models.ForeignKey('Quizz', related_name='quizzuser', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzs")
    note = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    issubmit = models.BooleanField(default=False)
    date_valide = models.DateField(blank=True, null=True)

    class Meta:
        """Meta definition for QuizzUser."""

        verbose_name = 'QuizzUser'
        verbose_name_plural = 'QuizzUsers'
        
    def createquizz(self):
        """Fonction pour générer les questions d'un quizz"""
        list_q= self.quizz.questions.filter(statut=True).order_by('?')
        # print(list_q)
        nb = list_q.count()
        nq = self.quizz.nbq
        # print(nb, nq)
        if nb==nq:
            liste_questions=list_q
        else:
            li =[]
            aux = []
            for i in range(nb - nq):
                li.append(list_q[i:nq+i])
                a = [self.quizz.niveau-a.niveau  for a in list_q[i:nq+i]]
                res = abs(sum(a)/len(a))
                aux.append(res)
            # print(aux)
            # print(aux.index(min(aux)))
            liste_questions = li[aux.index(min(aux))]
        for i in liste_questions:
            # print(i.contenu)
            # print(type(i))
            r = ReponseUser(
                question = i,
                quizzuser = self
            )
            # print('debut save')
            r.save()
            # print('fin')


    def getnote(self):
        """Fonction pour calculer la note"""
        nb = self.questions.all()
        n = nb.filter(istrue=True).count()
        nb = nb.count()
        # print(n, nb)
        return round(n/nb, 4)*100
    
    @property
    def isvalide(self):
        return self.note >= self.quizz.pourcentage
    
    @property
    def duree(self):
        debut = self.date_add
        fin = self.date_update
        fin = (fin.day*86400) +(fin.hour*3600) + (fin.minute*60)+ fin.second
        debut = (debut.day * 86400) + (debut.hour * 3600) + (debut.minute * 60) + debut.second
        secs = fin - debut
        d =""
        if secs >= 86400: # 60sec * 60min * 24hrs
            days = secs // 86400
            d += "{} days".format(int(days))
            secs = secs - days*86400

        if secs >= 3600:
            hrs = secs // 3600
            d += " {} hours".format(int(hrs))
            secs = secs - hrs*3600

        if secs >= 60:
            mins = secs // 60
            d += " {} minutes".format(int(mins))
            secs = secs - mins*60

        if secs > 0:
            d += " {} seconds".format(int(secs))
        return d

    @property
    def duree_for_classement(self):
        user_result = QuizzUser.objects.filter(user=self.user).all()
        user_total_time = 0
        for n in user_result:
            fin = (n.date_update.day*86400) +(n.date_update.hour*3600) + (n.date_update.minute*60)+ n.date_update.second
            debut = (n.date_add.day * 86400) + (n.date_add.hour * 3600) + (n.date_add.minute * 60) + n.date_add.second
            user_total_time += fin - debut
        return (1000 - user_total_time)

    def submit_quizz(self):
        self.issubmit =True
        self.save()


    def save(self, *args, **kwargs):
        nb = self.questions.all().count()
        if not self.pk:
            self.note = 0
            super(QuizzUser, self).save(*args, **kwargs)
            self.createquizz()
            result_epreuve = self.resultat_quizz.create(
                user= self.user,
                epreuve = self.quizz.epreuve_quizz.all()[:1].get(),
                note = self.note
            )
        else:
            # print("debut")
            if self.issubmit and not self.date_valide:
                self.date_valide = datetime.now()
            # print("debut note")
            self.note = self.getnote()
            # print(self.note)
            super(QuizzUser, self).save(*args, **kwargs)
            result_epreuve =self.resultat_quizz.all()[:1].get()
            result_epreuve.note = self.note
            result_epreuve.save()
            # print('fin save')
        self.user.save()

    def __str__(self):
        """Unicode representation of QuizzUser."""
        return self.user.username




class ReponseUser(Timemodels):
    """Model definition for ReponseUser."""

    # TODO: Define fields here
    question = models.ForeignKey(Question, related_name='reponseuser', on_delete=models.CASCADE)
    quizzuser = models.ForeignKey(QuizzUser, related_name='questions', on_delete=models.CASCADE)
    reponses = models.ManyToManyField('Reponse')
    istrue = models.BooleanField(default=False)

    @property
    def liste_true(self):
        aux = [i.id for i in self.reponses.all()]
        aux.sort()
        return aux

    class Meta:
        """Meta definition for ReponseUser."""

        verbose_name = 'ReponseUser'
        verbose_name_plural = 'ReponseUsers'
    
    def save(self, *args, **kwargs):
        # print("debut reponse")
        if not self.pk:
            super(ReponseUser, self).save(*args, **kwargs)
        else:
            super(ReponseUser, self).save(*args, **kwargs)
            self.istrue = self.liste_true == self.question.liste_true
            # print("continue")
            super(ReponseUser, self).save(*args, **kwargs)
            self.quizzuser.save()
        # print("fin reponse")

    def __str__(self):
        """Unicode representation of ReponseUser."""
        return str(self.istrue)