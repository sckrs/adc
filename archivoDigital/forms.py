from django import forms
from django.contrib.auth import forms as auth_forms
from archivoDigital.models import User,AreaRestringida,Area,Documento,retornaBreadCumbAreas,DocumentoRestringido
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from archivoDigital.send_email import sender,senderMany

class AreaRestringidaCreationForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirmación del Password', widget=forms.PasswordInput)

    class Meta:
        model = AreaRestringida
        fields = ['area','password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)
            return password1
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Los passwords no coinciden")
        else:
            area = self.cleaned_data.get("area")
            self.cambiaStatus(area)
        return password1

    def cambiaStatus(instancia,area):
        instancia_area = Area.objects.get(pk=area.pk)
        instancia_area.area_restringida=True
        instancia_area.save()

class AreaRestringidaChangeForm(forms.ModelForm):
    area=''
    count=0
    password_2 = forms.CharField(label='Confirmación del nuevo password', widget=forms.PasswordInput,required=False)
    password_admin = forms.CharField(label='Password de administrador', widget=forms.PasswordInput,required=False)
    changer = forms.BooleanField(label='Cambiar contraseña',help_text="Para cambiar la contraseña de esta área, usted debe comprobar que es el administrador.",required=False)

    class Meta:
        model = AreaRestringida
        fields = ['area','password','password_2','password_admin','changer']

        widgets = {
            'password': forms.TextInput(attrs={'readonly':'readonly',})
        }

    def clean_changer(self):
        changer = self.cleaned_data.get("changer")
        if changer:
            passwordadmin = self.cleaned_data.get("password_admin")
            newpassword = self.cleaned_data.get("password")
            confirmnewpassword = self.cleaned_data.get("password_2")
            if passwordadmin == None or passwordadmin == '' or confirmnewpassword == None or confirmnewpassword == '':
                raise forms.ValidationError("Ningun password puede estar vacio, favor de reinsertar los datos")
            else:
                if not check_password(passwordadmin,self.request.user.password):
                    raise forms.ValidationError("El password de administrador incorrecto, intentelo nuevamente")
                    self.count=1
                    return passwordadmin
                try:
                    password_validation.validate_password(confirmnewpassword, self.instance)
                except forms.ValidationError as error:
                    self.add_error('password_2', error)
                    self.count=2
                    return confirmnewpassword
                if newpassword and confirmnewpassword and newpassword != confirmnewpassword:
                    raise forms.ValidationError("Los passwords no coinciden")
                    self.count=3
                    return password_2
        else:
            password = self.cleaned_data.get("password")
            area = self.cleaned_data.get("area")
            try:
                areac=AreaRestringida.objects.get(area=area)
            except:
                raise forms.ValidationError("No puedes cambiar el area")
                return area
            if areac.pk != self.areaCambia.pk:
                raise forms.ValidationError("No puedes cambiar el area")
                return area
            else:
                if not check_password(password,areac.password):
                    raise forms.ValidationError("Para cambiar el password debes activar el checkbox")
                    return password
        return changer

    def save(self, commit=True):
        changer = self.cleaned_data.get('changer')
        psw=self.cleaned_data['password']
        areaModificada=self.cleaned_data.get('area')
        arearestringida = super(AreaRestringidaChangeForm, self).save(commit=False)
        if self.count == 0 and changer:
            areaS=retornaBreadCumbAreas(areaModificada,[])
            listaContactos=[]
            for area in areaS:
                usuarioEmail=User.objects.filter(area=area)
                if usuarioEmail.exists():
                    for usr in usuarioEmail:
                        listaContactos.append(usr.email)
            senderMany(listaContactos,'Actualización de claves de acceso',psw,areaModificada.nombre)
            return arearestringida
        else:
            self.count=0

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        form = self.cleaned_data
        passW=User.objects.make_random_password()
        user.set_password(passW)
        sender(1,form['email'],'Bienvenido(a)',passW,'')
        user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = auth_forms.ReadOnlyPasswordHashField(label="Contraseña",#)
        help_text="Puede cambiar la contraseña activando este checkbox"
                  "&nbsp;&nbsp;&nbsp;<input id=\"one\" type=\"checkbox\" value=\"Cambiar Contraseña\" name=\"changePass\">")

    password_admin = forms.CharField(label='Password de administrador', widget=forms.PasswordInput,required=False)

    class Meta:
        model = User
        fields = '__all__'

        widgets = {
            'phone': forms.NumberInput(attrs={'minlength': 10, 'maxlength': 15,  'type': 'number',}),
            'extension': forms.NumberInput(attrs={'minlength': 3, 'maxlength': 15,  'type': 'number',}),
        }

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_changePass(self):
        change = self.cleaned_data.get('changePass')
        pswdadmin = self.cleaned_data.get("password_admin")
        if change == 'change':
            if not check_password(pswdadmin,self.request.user.password):
                raise forms.ValidationError("El password de administrador incorrecto, intentelo nuevamente")
                return pswdadmin
        return change

    def clean_password(self):
        return self.initial["password"]

    def save(self,commit=True):
        data=self.cleaned_data
        user = super(UserChangeForm, self).save(commit=False)
        if data['changePass']=='change':
            passW=User.objects.make_random_password()
            sender(4,data['email'],'Restablecimiento de contraseña del Archivo Digital',passW,'su usuario')
            user.set_password(passW)
        if commit:
            user.save()
        return user

class DocumentForm(forms.ModelForm):
    class Meta:
        model=Documento
        fields=['periodo','area','documento','asunto','documento_restringido']
        widgets = {
            'documento':forms.ClearableFileInput(attrs={'multiple': True})
        }

class DocumentoRestringidoForm(forms.ModelForm):
    passwordCC = forms.CharField(label='Confirmación del Password', widget=forms.PasswordInput,required=True)

    class Meta:
        model=DocumentoRestringido
        fields='__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'required':True})
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)
        if  password=='':
            raise forms.ValidationError("El campo de password no pueden estar vacio.")
        return password

    def clean_area(self):
        periodo = self.cleaned_data.get("periodo")
        area = self.cleaned_data.get("area")
        verificaExistencia = DocumentoRestringido.objects.filter(periodo=periodo,area=area)

        if len(verificaExistencia) != 0 :
            raise forms.ValidationError("Los documentos del area {} del año {} ya se encuentran restringidos.".format(area,periodo))

        return area

    def clean_passwordC(self):
        data= self.cleaned_data
        passwordC = self.cleaned_data.get("passwordCC")
        if  data['password'] != data['passwordCC']:
            raise forms.ValidationError("Las contraseñas no coinciden")
        if  passwordC=='':
            raise forms.ValidationError("El campos de Confirmación de password no pueden estar vacio.")
        return passwordC

    def __init__(self, *args, **kwargs):
        super(DocumentoRestringidoForm, self).__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(area_restringida=True)

class DocumentoRestringidoChangeForm(forms.ModelForm):
    area=''
    count=0
    passwordC = forms.CharField(label='Confirmación del Password', widget=forms.PasswordInput,required=False)
    passwordAdmn = forms.CharField(label='Password administrador', widget=forms.PasswordInput,required=False)
    changerPs = forms.BooleanField(label='Cambiar contraseña',help_text="Para cambiar la contraseña usted debe comprobar que es el administrador.",required=False)

    class Meta:
        model=DocumentoRestringido
        fields='__all__'
        widgets = {
            'password': forms.TextInput(attrs={'readonly':'readonly'})
        }

    def clean_changerPs(self):
        changer = self.cleaned_data.get("changerPs")
        if changer:
            passwordadmin = self.cleaned_data.get("passwordAdmn")
            newpassword = self.cleaned_data.get("password")
            confirmnewpassword = self.cleaned_data.get("passwordC")
            if passwordadmin == None or passwordadmin == '' or confirmnewpassword == None or confirmnewpassword == '':
                raise forms.ValidationError("Ningun password puede estar vacio, favor de reinsertar los datos")
            else:
                if not check_password(passwordadmin,self.request.user.password):
                    raise forms.ValidationError("El password de administrador incorrecto, intentelo nuevamente")
                    self.count=1
                    return passwordadmin
                try:
                    password_validation.validate_password(confirmnewpassword, self.instance)
                except forms.ValidationError as error:
                    self.add_error('password_2', error)
                    self.count=2
                    return confirmnewpassword
                if newpassword and confirmnewpassword and newpassword != confirmnewpassword:
                    raise forms.ValidationError("Los passwords no coinciden")
                    self.count=3
                    return password_2
        else:
            password = self.cleaned_data.get("password")
            area = self.cleaned_data.get("area")
            try:
                areac=AreaRestringida.objects.get(area=area)
            except:
                raise forms.ValidationError("No puedes cambiar el area")
                return area
            if areac.pk != self.areaCambia.pk:
                raise forms.ValidationError("No puedes cambiar el area")
                return area
            else:
                if not check_password(password,areac.password):
                    raise forms.ValidationError("Para cambiar el password debes activar el checkbox")
                    return password
        return changer

    def save(self, commit=True):
        changer = self.cleaned_data.get('changerPs')
        psw=self.cleaned_data['password']
        areaModificada=self.cleaned_data.get('area')
        periodo=self.cleaned_data.get('periodo')
        docrestringido = super(DocumentoRestringidoChangeForm, self).save(commit=False)
        if self.count == 0 and changer:
            areaS=retornaBreadCumbAreas(areaModificada,[])
            listaContactos=[]
            for area in areaS:
                usuarioEmail=User.objects.filter(area=area)
                if usuarioEmail.exists():
                    for usr in usuarioEmail:
                        listaContactos.append(usr.email)
            senderMany(listaContactos,'Actualización de claves de acceso para los documentos de',psw,'{}/{}'.format(periodo.periodo,areaModificada.nombre))
            return docrestringido
        else:
            self.count=0

    def __init__(self, *args, **kwargs):
        super(DocumentoRestringidoChangeForm, self).__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(area_restringida=True)
