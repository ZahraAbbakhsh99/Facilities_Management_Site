from django.contrib import admin
from .models import *

@admin.register(FacilitiesManager)
class FacilitiesManagerAdmin(admin.ModelAdmin):
    list_display = ('organization', 'branch', 'identifier')
    list_filter = ('organization', 'branch')
    search_fields = ('organization', 'branch', 'identifier')


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('personnel_number', 'firstname', 'lastname', 'phone_number', 'expertise', 'current_tasks', 'satisfaction')
    list_filter = ('expertise', 'satisfaction')
    search_fields = ('personnel_number', 'firstname', 'lastname', 'phone_number')
    ordering = ('personnel_number',)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('department', 'organization', 'firstname', 'lastname', 'phone_number')
    list_filter = ('organization', 'department')
    search_fields = ('department', 'organization', 'firstname', 'lastname', 'phone_number')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'category__name', 'applicant__department', 'facility', 'registration_time', 'status')
    list_filter = ('category', 'status', 'facility')
    search_fields = ('task_id', 'applicant__department', 'facility__organization', 'category__name')
    ordering = ('registration_time',)

@admin.register(TaskCategory)
class TaskCategory(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
