# Register your models here.
# vim: set fileencoding=utf-8 :
from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe



class TestValidationInline(admin.TabularInline):
    model =  models.TestValidation
    #-------------le nombre d element a ajouter----------------#
    extra = 0
    
class ResultatExerciceInline(admin.TabularInline):
    model =  models.ResultatExercice
    #-------------le nombre d element a ajouter----------------#
    extra = 0
    
class ResultatCompoInline(admin.TabularInline):
    model =  models.ResultatCompo
    #-------------le nombre d element a ajouter----------------#
    extra = 0


class ExerciceAdmin(admin.ModelAdmin):

    inlines = [TestValidationInline]
    
    list_display = (
        'titre',
        'titre_slug',
        'code_depart',
        'code',
        'status',
        'date_add',
        'date_upd',
    )
    list_filter = (
        'code',
        'status',
        'date_add',
        'date_upd',
        'titre',
        'code_depart',

    )
    search_fields = ('titre',)
    date_hierarchy = 'date_add'
    actions = (
        'active',
        'desactive',
    )
    list_display_links = ['titre',]
    list_per_page = 100
    ordering = ['titre',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les exercices selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les exercices selectionner"


class TestValidationAdmin(admin.ModelAdmin):

    list_display = (
        'code_test',
        'exercice',
        'resultat',
        'status',
        'date_add',
        'date_upd',
    )
    list_filter = (
        
        'exercice',
        'status',
        'date_add',
        'date_upd',
    )
    search_fields = ('exercice',)
    date_hierarchy = 'date_add'
    list_display_links = ['exercice',]
    list_per_page = 100
    ordering = ['exercice',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les tests de validation selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les tests de validation selectionner"

class CodeAdmin(admin.ModelAdmin):

    list_display = (
        'specialite',
        'titre',
        'consige',
        'status',
        'date_add',
        'date_upd',
        
    )
    list_filter = (

        'titre',
        'specialite',
        'status',
        'date_add',
        'date_upd',
    )
    search_fields = ('titre',)
    # date_hierarchy = 'date_add'
    list_display_links = ['titre', 'specialite']
    list_per_page = 100
    ordering = ['specialite',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les Codes selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les Codes selectionner"




class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'lang_id',

        'status',
        'date_add',
        'date_upd',
        
    )
    list_filter = (
        'status',
    )
    search_fields = ('nom',)
    # date_hierarchy = 'date_add'
    list_display_links = ['nom']
    list_per_page = 100
    ordering = ['nom',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les Codes selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les languages selectionner"




class ResultatExerciceAdmin(admin.ModelAdmin):


    list_display = (
        'exercice',
        'user',
        'code',
        'valider',
        'nb_tentative',
        'status',
        'date_add',
        'date_upd',
    )
    list_filter = (
        'exercice',
        'user',
        'code',
        'status',
        'date_add',
        'date_upd',
        'nb_tentative',
    )
    search_fields = ('exercice',)
    date_hierarchy = 'date_add'
    list_display_links = ['exercice',]
    list_per_page = 100
    ordering = ['exercice',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les resultats des exercices selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les resultats des exercices selectionner"


class ResultatCompoAdmin(admin.ModelAdmin):

    list_display = (
        'resultat_exercice',
        'epreuve',
        'user',
        'note',
        'nbr_exo_valider',
        'status',
        'date_add',
        'date_upd',
    )
    list_filter = (
        'resultat_exercice',
        'epreuve',
        'user',
        'status',
        'date_add',
        'date_upd',
        'resultat_exercice',


    )
    search_fields = ('user','resultat_exercice',)
    date_hierarchy = 'date_add'
    list_display_links = ['resultat_exercice',]
    list_per_page = 100
    ordering = ['resultat_exercice',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les resultats des compo selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les resultats des compo selectionner"
    
    
class Langage_idAdmin(admin.ModelAdmin):
    
    list_display = (
        'lang_id',
           'nom',
        'status',
        'date_add',
        'date_upd',
    )
    list_filter = (
           'nom',
        'status',
        'date_add',
        'date_upd',
        'lang_id',


    )
    search_fields = ('lang_id',)
    date_hierarchy = 'date_add'
    list_display_links = ['lang_id',]
    list_per_page = 100
    ordering = ['lang_id',]
    def active(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,"la selection a ete activer avec succes")
    active.short_description = "Activer les resultats des compo selectionner"

    def desactive(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,"la selection a ete desactiver avec succes")
    desactive.short_description = "desactiver les resultats des compo selectionner"


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Exercice, ExerciceAdmin)
_register(models.TestValidation, TestValidationAdmin)
_register(models.ResultatExercice, ResultatExerciceAdmin)
_register(models.ResultatCompo, ResultatCompoAdmin)
_register(models.Code, CodeAdmin)
_register(models.LangageId, Langage_idAdmin)
