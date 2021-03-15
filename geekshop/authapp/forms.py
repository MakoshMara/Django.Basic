from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        data = self.cleaned_data['username']
        dict_wrong = ['мудак', 'хрен', 'сексмашина']
        if dict_wrong.count(data) != 0:
            raise forms.ValidationError('Вы плохой мальчик!')
        return data

class ShopUserEditForm(UserChangeForm):
    class Meta:
        model =ShopUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_username(self):
        data = self.cleaned_data['username']
        dict_wrong = ['мудак', 'хрен', 'сексмашина']
        if dict_wrong.count(data) != 0:
            raise forms.ValidationError('Вы плохой мальчик!')
        return data
