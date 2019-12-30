from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models
from django.db.models import Count
from django.db.models.functions import TruncDay
from .models import Quizz, Question, Reponse, QuizzUser, ReponseUser



""" Les Inlines ------------------ """
class QuestionInline(admin.TabularInline):
    model =  models.Question
    extra = 0

class ReponseInline(admin.TabularInline):
    model =  models.Reponse
    extra = 0

""" Les Differentes Partie Admin  ------------------ """

class QuizzAdmin(admin.ModelAdmin):

    list_display = (
        'specialite',
        'statut',
        'is_available',
        'date_add',
        'date_update',
        'titre',
        'niveau',
        'pourcentage',
        'nbq',
        'date_debut',
        'date_fin',
        'duree',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_update',
        'date_debut',
        'date_fin',
    )
    date_hierarchy = ('date_add')


    inlines = [QuestionInline]

    readonly_fields = ['specialite']

    def save_model(self, request, obj, form, change):
        obj.specialite = request.user.user_specialite.specialite
        super(QuizzAdmin, self).save_model(request, obj, form, change)

    # change_list_template = 'pages/admin/change_list_quizapp.html'

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
    #     chart_data =  Quizz.objects.all()

    #     data = {
    #         'chart_data': chart_data,
    #         'nom': 'Gbane'
    #     }

    #     extra_context = extra_context or data

    #     return super().changelist_view(request, extra_context=data)



class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        'statut',
        'date_add',
        'date_update',
        'quizz',
        'niveau',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_update',
        'quizz',
    )
    date_hierarchy = ('date_add')

    inlines = [ReponseInline]

    # change_list_template = 'pages/admin/change_list_question.html'

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
    #     chart_data =  Question.objects.all()

    #     data = {
    #         'chart_data': chart_data,
    #         'nom': 'Gbane'
    #     }

    #     extra_context = extra_context or data

    #     return super().changelist_view(request, extra_context=data)


class ReponseAdmin(admin.ModelAdmin):

    list_display = (
        'statut',
        'date_add',
        'date_update',
        'isrtue',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_update',
        'isrtue',
    )
    date_hierarchy = ('date_add')

    # change_list_template = 'pages/admin/change_list_reponse.html'

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
    #     chart_data =  Reponse.objects.all()

    #     data = {
    #         'chart_data': chart_data,
    #         'nom': 'Gbane'
    #     }

    #     extra_context = extra_context or data

    #     return super().changelist_view(request, extra_context=data)



class QuizzUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_update',
        'date_valide',
        'quizz',
        'user',
        'note',
        'duree',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_update',
        'note',
    )
    date_hierarchy = ('date_add')

    # change_list_template = 'pages/admin/change_list_quizzuser.html'

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
       
    #     chart_data = QuizzUser.objects.all()

    #     data = {
            
    #         'chart_data': chart_data,
    #     }

    #     extra_context = extra_context or data

    #     return super().changelist_view(request, extra_context=data)



class ReponseUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_update',
        'quizzuser',
        'istrue',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_update',
        'istrue',
    )
    date_hierarchy = ('date_add')

    raw_id_fields = ('reponses',)
    def save_related(self, request, form, formsets, change):
        super(ReponseUserAdmin, self).save_related(request, form, formsets, change)
        form.instance.save()
    
    # change_list_template = 'pages/admin/change_list_reponseuser.html'

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
    #     chart_data = ReponseUser.objects.all()

    #     data = {
    #         'chart_data': chart_data,
    #         'nom': 'Gbane'
    #     }

    #     extra_context = extra_context or data

    #     return super().changelist_view(request, extra_context=data)
    


def _register(model, admin_class):
    admin.site.register(model, admin_class)


# _register(models.Specialisation, SpecialisationAdmin)
# _register(models.Profile, ProfileAdmin)
_register(models.Quizz, QuizzAdmin)
_register(models.Question, QuestionAdmin)
_register(models.Reponse, ReponseAdmin)
_register(models.QuizzUser, QuizzUserAdmin)
_register(models.ReponseUser, ReponseUserAdmin)