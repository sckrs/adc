from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.core.exceptions import PermissionDenied
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.template.response import TemplateResponse
from archivoDigital.forms import UserChangeForm, UserCreationForm, AreaRestringidaCreationForm, AreaRestringidaChangeForm,DocumentForm,DocumentoRestringidoForm,DocumentoRestringidoChangeForm
from archivoDigital.models import User,Documento,DocumentoRestringido,Area,AreaRestringida,PeriodoGestion,AsuntoArea,ReporteInsidencias
# Register your models here.

class AreaRestringidaAdmin(admin.ModelAdmin):
    formix = AreaRestringidaChangeForm
    add_form = AreaRestringidaCreationForm
    change_form_template = "admin/arearestringida_pass_change_form.html"
    actions = ['delete_selected']
    search_fields = ['area']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('area','password', 'password2')}
        ),
    )

    def delete_selected(modeladmin, request, queryset):
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied
        if request.POST.get('post'):
            for obj in queryset:
                areamodificastatus = Area.objects.get(nombre=obj)
                areamodificastatus.area_restringida=False
                areamodificastatus.save()
                obj.delete()
        else:
            return delete_selected_(modeladmin, request, queryset)
    delete_selected.short_description = "Eliminar areas restringidas seleccionadas"

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.formix
            self.form.request=request
            self.form.areaCambia=obj
        return super(AreaRestringidaAdmin, self).get_form(request, obj, **kwargs)

class AreaAdmin(admin.ModelAdmin):
    #list_display = ('nombre', 'clave','tipo','area_superior')
    list_display = ('tipo', 'nombre','clave','area_superior','prioridad','area_restringida')
    search_fields = ['nombre']

    fieldsets = (
        ('Datos del área', {'fields': ('tipo', 'nombre','clave','area_superior','prioridad','area_restringida')}),
    )
    ordering = ('id',)

class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        ('Credenciales_de_acceso', {'fields': ('email', 'password','password_admin')}),
        ('Información del Usuario', {'fields': ('first_name', 'last_name','area','cargo','phone','extension')}),
        ('Rol de usuario, bloqueo de acceso y permisos', {'fields': ('is_active', 'is_staff', 'is_superuser','changePass','user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)}
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_form_template = "admin/pass_change_form.html"
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    ordering = ('first_name',)
    readonly_fields = ('last_login', 'date_joined','is_superuser',)

    def get_form(self, request, *args, **kwargs):
        form=super(UserAdmin, self).get_form(request, *args, **kwargs)
        form.request=request
        return form

class DocumentFormAdmin(admin.ModelAdmin):
    form=DocumentForm

    list_display = ('Nombre',)
    search_fields = ['nombre']

    def save_model(self, request, obj, form, change):
        datos=form.cleaned_data
        for afile in request.FILES.getlist('documento'):
             instance = Documento(documento=afile,periodo=datos['periodo'],area=datos['area'],documento_restringido=datos['documento_restringido'])
             instance.save()

class AsuntoAreaAdmin(admin.ModelAdmin):
    fields = ['nombre', 'area']
    list_display = ('nombre','area_del_asunto')
    search_fields = ['nombre','area_del_asunto']

    ordering = ('id',)

class DocumentoRestringidoAdminForm(admin.ModelAdmin):
    formi = DocumentoRestringidoChangeForm
    add_form = DocumentoRestringidoForm
    change_form_template = "admin/Docrestringido_pass_change_form.html"
    actions = ['delete_selected']
    search_fields = ['area']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('area','password', 'password2')}
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.formi
            self.form.request=request
            self.form.areaCambia=obj
        return super(DocumentoRestringidoAdminForm, self).get_form(request, obj, **kwargs)

    def delete_selected(modeladmin, request, queryset):
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied
        if request.POST.get('post'):
            for obj in queryset:
                Documento.objects.filter(periodo=obj.periodo,area=obj.area).update(documento_restringido=False)
                obj.delete()
        else:
            return delete_selected_(modeladmin, request, queryset)
    delete_selected.short_description = "Eliminar restriccion en documentos"


admin.site.register(User, UserAdmin)
admin.site.register(Documento,DocumentFormAdmin)
admin.site.register(DocumentoRestringido,DocumentoRestringidoAdminForm)
admin.site.register(Area,AreaAdmin)
admin.site.register(AreaRestringida,AreaRestringidaAdmin)
admin.site.register(AsuntoArea,AsuntoAreaAdmin)

admin.site.register(PeriodoGestion)
admin.site.register(ReporteInsidencias)
