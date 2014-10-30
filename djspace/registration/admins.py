from django.contrib import admin

from djspace.registration.models import *

class UndergraduateAdmin(admin.ModelAdmin):

    model = Undergraduate
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(UndergraduateAdmin, self).save(request, obj, form, change)

class GraduateAdmin(admin.ModelAdmin):

    model = Graduate
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(GraduateAdmin, self).save(request, obj, form, change)

class FacultyAdmin(admin.ModelAdmin):

    model = Faculty
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(FacultyAdmin, self).save(request, obj, form, change)

class ProfessionalAdmin(admin.ModelAdmin):

    model = Professional
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        super(ProfessionalAdmin, self).save(request, obj, form, change)


admin.site.register(Undergraduate, UndergraduateAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Professional, ProfessionalAdmin)

