from django.db import models
from tinymce import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from quizz_app.models import QuizzUser, Quizz
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Specialite(models.Model):
    """Model definition for Specialite."""
    nom = models.CharField(max_length=250)
    description = HTMLField('description')
    logo = models.ImageField(upload_to='Specialite')
    code = models.BooleanField(default=False)
    quizz = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Specialite."""

        verbose_name = 'Specialite'
        verbose_name_plural = 'Specialites'

    def __str__(self):
        """Unicode representation of Specialite."""
        return self.nom


class UserSpecialite(models.Model):
    """Model definition for UserSpeciallite."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_specialite')
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='userspecialite_specialite')
    status_demande = models.BooleanField(default=False)
    nanplus = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # moyenne_generale = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    
    # def save(self, *args, **kwargs):
    #     self.moyenne_generale = self.get_moyenne_general()
    #     super(UserSpecialite, self).save(*args, **kwargs)

    # def get_moyenne_general(self):
    #     """ Fonction qui recupère la moyenne de l'utilisateur """
    #     if self.specialisation:
    #         notes = sum([i.note for i in self.user.quizzs.all()])
    #         nb = self.specialite.quizzs.filter(statut = True).count()
    #         return notes/nb
    #     else:
    #         return 0

    # @property
    # def get_specialisation_rang(self):
    #     """Fonction pour récupérer le classement de l'utilisateur par spécialisation"""
    #     return self.specialite.all().order_by('-moyenne_generale')

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

    class Meta:
        """Meta definition for UserSpecialite."""

        verbose_name = 'UserSpeciallite'
        verbose_name_plural = 'UserSpecialites'

    def __str__(self):
        """Unicode representation of UserSpecialite."""
        return self.user.username

class Profile(models.Model):
    """Model definition for Profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    contacts = models.CharField(max_length=30, null=True)
    genre = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=30, null=True)
    pays = models.CharField(max_length=255, null=True)
    ville = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    images = models.ImageField(upload_to='images/avatar/', default="specialisation_nan\static\ressources\images\logo-nan.png")
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    # TODO: Define fields here
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.user_profile.save()
    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.username

class Cours(models.Model):
    """Model definition for Cours."""
    titre = models.CharField(max_length=200)
    description = HTMLField('description')
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Cours."""
        
        verbose_name = 'Cours'
        verbose_name_plural = 'Courss'

    def __str__(self):
        """Unicode representation of Cours."""
        return self.titre

class Epreuve(models.Model):
    """Model definition for Epreuve."""
    nom = models.CharField(max_length=150)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='epreuve_specialite')
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='epreuve_quizz', blank=True, null=True)
    code = models.ForeignKey('livecoding.Code', on_delete=models.CASCADE, related_name='resultat_code', blank=True, null=True)
    cours = models.OneToOneField(Cours, on_delete=models.CASCADE, related_name='epreuve_cours')
    status = models.BooleanField(default=True)
    
    date_add = models.DateTimeField(auto_now_add=True)
    
    date_update = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Epreuve."""

        verbose_name = 'Epreuve'
        verbose_name_plural = 'Epreuves'
        ordering = ('date_add',)

    def __str__(self):
        """Unicode representation of Epreuve."""
        return self.nom




class RessourcePdf(models.Model):
    """Model definition for RessourcePdf."""
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='pdf_cours')
    titre = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='pdf')
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for RessourcePdf."""

        verbose_name = 'RessourcePdf'
        verbose_name_plural = 'RessourcePdfs'

class RessourceVideo(models.Model):
    """Model definition for RessourceVideo."""
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='video_cours')
    titre = models.CharField(max_length=200)
    video = models.FileField(upload_to='video')
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for RessourceVideo."""

        verbose_name = 'RessourceVideo'
        verbose_name_plural = 'RessourceVideos'

class ResultatEpreuve(models.Model):
    """Model definition for ResultatEpreuve."""
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE, related_name='resultat_epreuve')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultat_user')
    quizz = models.ForeignKey(QuizzUser, on_delete=models.CASCADE, related_name='resultat_quizz', blank=True, null=True)
    code = models.ForeignKey('livecoding.Code', on_delete=models.CASCADE, related_name='resultat_livecoding', blank=True, null=True)
    note = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True, blank='True', null='True')
    date_update = models.DateTimeField(auto_now=True, blank='True', null='True')
    # user_moyenne = models.FloatField()


    # TODO: Define fields here

    class Meta:
        """Meta definition for ResultatEpreuve."""

        verbose_name = 'ResultatEpreuve'
        verbose_name_plural = 'ResultatEpreuves'

    def __str__(self):
        """Unicode representation of ResultatEpreuve."""
        return self.user.username
    
    @property
    def moyenne(self):
        user_note = ResultatEpreuve.objects.filter(user=self.user, quizz__issubmit="True" ).all()
        user_qt = ResultatEpreuve.objects.filter(user=self.user, quizz__issubmit="True").all().count()
        user_total = 0
        if user_qt > 0:
            for n in user_note:
                user_total += n.note
            return round((user_total / user_qt), 2)
        else:
            return 0
            
    
    @property
    def duree_total(self):
        user_result = ResultatEpreuve.objects.filter(user=self.user).all()
        user_total_time = 0
        for n in user_result:
            fin = (n.date_update.day*86400) +(n.date_update.hour*3600) + (n.date_update.minute*60)+ n.date_update.second
            debut = (n.date_add.day * 86400) + (n.date_add.hour * 3600) + (n.date_add.minute * 60) + n.date_add.second
            user_total_time += fin - debut
        return (1000 - user_total_time)

    # def save(self, *args, **kwargs):
    #     user_note = ResultatEpreuve.objects.filter(user=self.user).all()
    #     user_qt = ResultatEpreuve.objects.filter(user=self.user).all().count()
    #     user_total = 0
    #     for n in user_note:
    #         user_total += n.note
    #     self.user_moyenne = (user_total / user_qt)
            
    #     super(ResultatEpreuve, self).save(*args, **kwargs)


