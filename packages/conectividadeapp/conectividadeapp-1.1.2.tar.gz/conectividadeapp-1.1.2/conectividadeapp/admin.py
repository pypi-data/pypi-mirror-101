from django.contrib import admin

from .models import Actor, ActorCategory
from .models import OldDevice
from .models import ActivityReason, Activity

@admin.register(ActorCategory)
class ActorCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id','name')


@admin.register(OldDevice)
class OldDevice(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'when', 'description','reason' , 'type']

# @admin.register(ActivityInstall)
# class ActivityInstallAdmin(admin.ModelAdmin):
#     list_display = ['id', 'when', 'description', 'reason', 'type']
#
# @admin.register(ActivityRemove)
# class ActivityRemoveAdmin(admin.ModelAdmin):
#     list_display = ['id', 'when', 'description', 'reason', 'type']

@admin.register(ActivityReason)
class ActivityReason(admin.ModelAdmin):
    list_display = ['name', 'type']


#admin.site.register(Categoria)
#admin.site.register(Registroo)

#admin.site.register()

# Register your models here.
