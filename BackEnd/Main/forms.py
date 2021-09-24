from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسمك ثلاثي'}),

                                 )

    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الكود',
                                                              'data-validation': "number",
                                                              'data-validation-error-msg': "الكود لازم يكون 5 ارقام وتكون ارقام انجليزي",
                                                              'data-validation-allowing': "range[00000;99999]"

                                                              }),
                                )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'الرقم السري'}),
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'اعد ادخال الرقم السري'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'Phone_No', 'password1', 'password2',)