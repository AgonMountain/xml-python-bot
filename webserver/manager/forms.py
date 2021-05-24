from django.forms import ModelForm, TextInput, CheckboxInput
from django import forms
from django.contrib.auth.models import User
from .models import User as MyUser
from .models import Config, Scheme, Element, ElementAddition, ElementTransition


class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Неверный пароль.')

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class FindUserForm(ModelForm):
    user_id = forms.CharField(max_length=100, required=False, label='ID пользователя',
                    widget=forms.TextInput(attrs={'placeholder': 'все пользователи'}))

    class Meta:
        model = MyUser
        fields = ['user_id']


class ConfigForm(ModelForm):
    class Meta:
        model = Config
        fields = ['token', 'is_on']

        widgets = {
            'token': TextInput(attrs={'placeholder': 'токен'}),
            'is_on': CheckboxInput(),
        }


class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'placeholder': 'имя ветки'})
        }


class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = ['scheme', 'name', 'text']

        widgets = {
            'text': TextInput(attrs={'placeholder': 'текст элемента'}),
        }


class AdditionForm(ModelForm):
    class Meta:
        model = ElementAddition
        fields = ['text', 'addition']

        widgets = {
            'text': TextInput(attrs={'placeholder': 'текст / условие дополнения'}),
        }


class TransitionForm(ModelForm):
    class Meta:
        model = ElementTransition
        fields = ['text', 'transition']

        widgets = {
            'text': TextInput(attrs={'placeholder': 'текст / условие перехода'}),
        }
