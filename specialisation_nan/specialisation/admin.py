from django.contrib import admin

#importation des models
from . import models
from .models import Epreuve
from quizz_app.models import Quizz
from django.utils.safestring import mark_safe

class PdfInline(admin.TabularInline):
    model =  models.RessourcePdf
    extra = 0

class VideoInline(admin.TabularInline):
    model =  models.RessourceVideo
    extra = 0

@admin.register(models.Specialite)
class SpecialiteAdmin(admin.ModelAdmin):

    #les champs à afficher dans la table
    list_display = (
        'LogoSpecialite',
        'nom',
        'code',
        'quizz',
        'status',
        'date_add',
        'date_update',
        )
    list_filter = (
        'status',
        'date_add',
        'date_update',
    )

    search_fields = (
        'nom',
    )


    date_hierarchy = 'date_add'

    actions = ('active', 'desactive',)

    list_display_links = ['nom',]
    
    list_per_page = 10

    ordering = ['nom']


    fieldsets = [
        ('Information', {'fields' : ['nom', 'description', 'logo', 'code', 'quizz']}),
        ('Visibilité', {'fields' : ['status']}),
    ]

    def LogoSpecialite(self, obj):
        return mark_safe('<img src = " {url} " width = " 100px " heigth = " 50px " />'.format(url=obj.logo.url))

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Specialisations sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les Specialisations sélectionnées'

    # def view_image(self, obj):
    #     return mark_safe('<img src="{img_url}" width="100px" height="50" />'.format(img_url=obj.image.url))

    # def detail_image(self, obj):
    #     return mark_safe('<img src="{img_url}" width="300px" height="150" />'.format(img_url=obj.image.url))

@admin.register(models.UserSpecialite)
class UserSpecialiteAdmin(admin.ModelAdmin):

    #les champs à afficher dans la table
    list_display = (
        'user',
        'specialite',
        'status_demande',
        'nanplus',
        'status',
        'date_add',
        'date_update',
        )
    list_filter = (
        'status',
        'date_add',
        'date_update',
        'user',
        'specialite',
        'status_demande',
        'nanplus',
        
    )

    # search_fields = (
    #     'nom',
    # )

    date_hierarchy = 'date_add'

    actions = ('active', 'desactive')

    # list_display_links = ['nom',]
    
    list_per_page = 10

    # ordering = ['nom',]

    # readonly_fields = ['detail_image']
    fieldsets = [
        ('Information', {'fields' : ['user', 'specialite', 'status_demande', 'nanplus' ]}),
        ('Visibilité', {'fields' : ['status']}),
    ]

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Specialit"s sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les Specialités sélectionnées'

    # def viw_image(self, obj):
    #     return mark_safe('<img src="{img_url}" width="100px" height="50" />'.format(img_url=obj.image.url))

    # def detail_image(self, obj):
    #     return mark_safe('<img src="{img_url}" width="300px" height="150" />'.format(img_url=obj.image.url))
@admin.register(models.Profile)
class MyUserAdmin(admin.ModelAdmin):

    list_display = (
        'afficheImage',
        'user',
        'contacts',
        'genre',
        'location',
        'pays',
        'ville',
        'birth_date',
        'status',
        'date_add',
    )
    list_filter = (

        'status',
        'date_add',
        'date_update',
        'location',
        'ville',
    )
    search_fields = ('ville',)
    date_hierarchy = 'date_add'
    actions = ('active','desactive')
    list_display_links = ['user','contacts']
    list_per_page = 5
    ordering = ['birth_date']
    readonly_fields = ['afficheImage']
    fieldsets = [
        ('Identification utilisateur',{
            'fields':['user','contacts','genre','location','pays','ville','birth_date','images']
        }),
        ('Visibilité',{
            'fields':['status']
        }),
    ]
    
    def afficheImage(self, obj):
        return mark_safe('<img src = " {url} " width = " 100px " heigth = " 50px " />'.format(url=obj.images.url))

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request,"La selection a été activé avec succés")
    
    active.short_description = "activer Les profiles selectionnés"
    
    
    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request,"La selection a été desactivé avec succés")
        
    desactive.short_description = "desactivés Les sousCategorie selectionnés"


@admin.register(models.Epreuve)
class EpreuveAdmin(admin.ModelAdmin):

    #les champs à afficher dans la table
    list_display = (
        'specialite',
        'nom',
        'cours',
        'quizz',
        'code',
        'date_add',
        'status',
        'date_update',
        )
    list_filter = (
        'status',
        'date_add',
        'date_update',
    )

    search_fields = (
        'nom',
    )

    date_hierarchy = 'date_add'

    actions = ('active', 'desactive')

    list_display_links = ['nom']
    
    list_per_page = 10

    ordering = ['nom',]

    fieldsets = [
        ('Information', {'fields' : ['specialite','nom', 'cours','quizz', 'code' ]}),

        ('Standard', {'fields' : ['status']}),
    ]
    
    # change_list_template = 'pages/admin/change_list_epreuve.html'

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
    #     chart_data =  Epreuve.objects.all()

    #     data = {
    #         'chart_data': chart_data,
    #         'nom': 'Gbane'
    #     }

    #     extra_context = extra_context or data

    #     return super().changelist_view(request, extra_context=data)
    

    def render_change_form(self, request, context, *args, **kwargs):
        spe = request.user.user_specialite.specialite
        context['adminform'].form.fields['quizz'].queryset = spe.quizzs.filter(statut=True)
        context['adminform'].form.fields['code'].queryset = spe.specialitecode.filter(status=True)
        return super(EpreuveAdmin, self).render_change_form(request, context, *args, **kwargs)

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Epreuves sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les epreuves sélectionnées'


@admin.register(models.Cours)
class CoursAdmin(admin.ModelAdmin):

    #les champs à afficher dans la table
    list_display = (
        'titre',
        'date_add',
        'date_update',
        'status',
        )
    list_filter = (
        'status',
        'date_add',
        'date_update',
        'description',

    )

    search_fields = (
        'titre',
    )

    inlines = [PdfInline, VideoInline]

    date_hierarchy = 'date_add'

    actions = ('active', 'desactive')

    list_display_links = ['titre']
    
    list_per_page = 10

    ordering = ['titre',]
    fieldsets = [
        ('Information', {'fields' : ['titre', 'description' ]}),
        ('Visibilité', {'fields' : ['status']}),
    ]

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Cours sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les cours sélectionnées'


@admin.register(models.RessourcePdf)
class RessourcePdfAdmin(admin.ModelAdmin):
    
    #les champs à afficher dans la table
    list_display = (
        'titre',
        'cours',
        'pdf',
        'status',
        'date_add',
        'date_update',
        )
    list_filter = (
        'titre',
        'status',
        'date_add',
        'date_update',
        'cours',
        'pdf',
    )

    search_fields = (
        'pdf',
    )

    list_display_links = ['cours']

    list_per_page = 10

    ordering = ['cours']


    fieldsets = [
        ('Information', {'fields' : ['cours', 'titre']}),
        ('Ressources', {'fields' : ['pdf']}),
        ('Visibilité', {'fields' : ['status']}),
    ]
    

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Ressources sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les Ressources sélectionnées'


@admin.register(models.RessourceVideo)
class RessourceVideoAdmin(admin.ModelAdmin):
    
    #les champs à afficher dans la table
    list_display = (
        'titre',
        'cours',
        'video',
        'status',
        'date_add',
        'date_update',
        )
    list_filter = (
        'titre',
        'status',
        'date_add',
        'date_update',
        'cours',
        'video',


    )


    date_hierarchy = 'date_add'

    actions = ('active', 'desactive')

    list_display_links = ['cours']
    
    list_per_page = 10

    ordering = ['cours']


    fieldsets = [
        ('Information', {'fields' : ['cours','titre']}),
        ('Ressources', {'fields' : ['video']}),
        ('Visibilité', {'fields' : ['status']}),
    ]

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Compositions sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les Compositions sélectionnées'

    # def view_video(self, obj):
    #     return mark_safe('<video controls width="250"><source src="{video_url}" type="video/webm"><source src="{video_url}" type="video/mp4"></video>'.format(video_url=obj.video.url))

@admin.register(models.ResultatEpreuve)
class ResultatEpreuveAdmin(admin.ModelAdmin):

    #les champs à afficher dans la table
    list_display = (
        'epreuve',
        'user',
        'quizz',
        'code',
        'note',
        'status',
        'date_add',
        'date_update',
        'moyenne',
        'duree_total',
        )
    list_filter = (
        'status',
        'date_add',
        'date_update',
        'epreuve',
        'user',
        'quizz',
        'note',
    )



    actions = ('active', 'desactive')

    list_display_links = ['user']
    
    list_per_page = 10

    ordering = ['epreuve']


    fieldsets = [
        ('Information', {'fields' : ['user', 'epreuve', 'quizz', 'code', 'note']}),
        ('Visibilité', {'fields' : ['status']}),
    ]

    def active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "La sélection a été activée avec succès")
    active.short_description = 'Activez les Resultats Compos sélectionnées'

    def desactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "La sélection a été désactivée avec succès")
    desactive.short_description = 'Désactivez les Resultats Compos sélectionnées'
