from django.db import models

# Create your models here.
from django.db import models
from tinymce import HTMLField
from django.utils.text import slugify
from specialisation.models import * 
from django.utils.timezone import now


# Create your models here.

class LangageId(models.Model):
    """Model definition for LangageId."""

    lang_id = models.PositiveIntegerField()
    nom = models.CharField(max_length=250)

    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    class Meta:
        """Meta definition for LangageId."""

        verbose_name = 'LangageId'
        verbose_name_plural = 'LangageId'
        ordering = ('date_add',)

    def __str__(self):
        """Unicode representation of ResultatCompo."""
        return '{}:{}'.format(self.lang_id , self.nom ) # TODO

class Code(models.Model):
    """Model definition for Code."""
    # TODO: Define fields here
    titre = models.CharField(max_length=50)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE,related_name='specialitecode')   
    coding_in = models.ForeignKey(LangageId, on_delete=models.CASCADE,related_name='codingin',null=True) 
    consige = models.TextField(null=True, verbose_name="consigne a respecter")
    debut = models.DateTimeField(auto_now=False, null=True)
    fin = models.DateTimeField(auto_now=False, null=True)  
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    

    @property
    def is_valid(self):
        if self.debut < now() and self.fin > now():
            return True
        else :
            return False


    class Meta:
        
        """Meta definition for Code."""

        verbose_name = 'Code'
        verbose_name_plural = 'Codes'
    def __str__(self):
        """Unicode representation of Exercice."""
        return '{} : {}'.format(self.titre,self.specialite.nom ) # TODO
        
class Exercice(models.Model):
    """Model definition for Exercice."""  
    code = models.ForeignKey(Code, on_delete=models.CASCADE,related_name='livecoding')   
    titre = models.CharField(max_length=255)
    titre_slug = models.SlugField(max_length=255,editable=False,null=True)
    description = HTMLField('description')
    code_depart = models.TextField()
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        
        super(Exercice, self).save(*args, **kwargs)
        self.titre_slug = slugify(self.titre +' '+ str(self.id))
        super(Exercice, self).save(*args, **kwargs)

    class Meta:
        """Meta definition for Exercice."""

        verbose_name = 'Exercice'
        verbose_name_plural = 'Exercices'
        ordering = ('date_add',)

    def __str__(self):
        """Unicode representation of Exercice."""
        return '{}'.format(self.titre ) # TODO

class TestValidation(models.Model):
    """Model definition for TestValidation."""

    code_test = models.TextField()
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE,related_name='exercicetest')
    resultat = models.TextField()

    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for TestValidation."""

        verbose_name = 'TestValidation'
        verbose_name_plural = 'TestValidations'
        ordering = ('date_add',)

    def __str__(self):
        """Unicode representation of TestValidation."""
        return '{}'.format(self.resultat ) # TODO

class ResultatExercice(models.Model):
    """Model definition for ResultatExercice."""

    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE,related_name='exerciceresultat')
    nb_tentative = models.PositiveIntegerField()
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userresultat')
    valider = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for ResultatExercice."""

        verbose_name = 'ResultatExercice'
        verbose_name_plural = 'ResultatExercices'
        ordering = ('date_add',)
    def __str__(self):
        """Unicode representation of ResultatExercice."""
        return '{}'.format(self.user.username ) # TODO
   

 

class ResultatCompo(models.Model):
    """Model definition for ResultatCompo."""

    resultat_exercice = models.ForeignKey(Code, on_delete=models.CASCADE,related_name='resultexoresultcompo', verbose_name="livecoding")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='resultatcompouser')
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE,related_name='epreuve',null=True)
    note = models.IntegerField(default=0)
    nbr_exo_valider = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    class Meta:
        """Meta definition for ResultatCompo."""

        verbose_name = 'ResultatCompo'
        verbose_name_plural = 'ResultatCompos'
        ordering = ('date_add',)

    def __str__(self):
        """Unicode representation of ResultatCompo."""
        return '{}'.format(self.user.username ) # TODO
    
  
    

    
    

    
