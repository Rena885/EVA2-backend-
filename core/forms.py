
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'tu@email.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
        error_messages = {
            'username': {
                'unique': "este nombre de usuario ya esta en uso",
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de usuario"
        self.fields['username'].help_text = "Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("este correo ya esta en uso")
        return email
