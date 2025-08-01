from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import re
from orders.models import Recipient

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль',
        })
    )
    password2 = forms.CharField(
        label='Підтвердіть пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть пароль',
        })
    )

    class Meta:
        model = CustomUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Email'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Користувач з таким email вже існує.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise ValidationError("Пароль має містити щонайменше 8 символів.")

        if not re.search(r"\d", password1):
            raise ValidationError("Пароль має містити хоча б одну цифру.")

        if not re.search(r"[a-zA-Zа-яА-Я]", password1):
            raise ValidationError("Пароль має містити хоча б одну літеру.")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не співпадають.")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))   
        if commit:
            user.save()
        return user
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ChangeUserDataForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        if not first_name:
            return None
        first_name = first_name.strip()

        if not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-]+$', first_name):
            raise forms.ValidationError("Ім’я може містити тільки літери, пробіли або дефіс")

        if len(first_name) < 2:
            raise forms.ValidationError("Ім’я повинно містити щонайменше 2 символи")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        if not last_name:
            return None
        last_name = last_name.strip()
        
        if not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-]+$', last_name):
            raise forms.ValidationError("Прізвище може містити тільки літери, пробіли або дефіс")

        if len(last_name) < 2:
            raise forms.ValidationError("Прізвище повинно містити щонайменше 2 символи")

        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return None
        phone = phone.strip()

        if not phone.startswith('+380'):
            raise forms.ValidationError("Номер телефону повинен починатися з +380")

        if not re.match(r'^\+?\d{9,15}$', phone):
            raise forms.ValidationError("Невірний формат номера телефону. Повинен містити від 9 до 15 цифр, може починатися з '+'")

        return phone
    
    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name', '')
        if not middle_name:
            return None
        middle_name = middle_name.strip()

        if not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-]+$', middle_name):
            raise forms.ValidationError("По батькові може містити тільки літери, пробіли або дефіс")

        if len(middle_name) < 2:
            raise forms.ValidationError("По батькові повинно містити щонайменше 2 символи")

        return middle_name

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть вашу електронну адресу'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть новий пароль'
        })
    )

    new_password2 = forms.CharField(
        label="Підтвердіть пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Підтвердіть новий пароль'
        })
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")

        if len(password1) < 8:
            raise ValidationError("Пароль має містити щонайменше 8 символів.")

        if not re.search(r"\d", password1):
            raise ValidationError("Пароль має містити хоча б одну цифру.")

        if not re.search(r"[a-zA-Zа-яА-Я]", password1):
            raise ValidationError("Пароль має містити хоча б одну літеру.")

        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не співпадають.")

        return cleaned_data

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['first_name', 'last_name', 'middle_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-custom'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError("Ім’я є обов’язковим.")
        if not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-]+$', first_name):
            raise forms.ValidationError("Ім’я може містити тільки літери, пробіли або дефіс.")
        if len(first_name) < 2:
            raise forms.ValidationError("Ім’я повинно містити щонайменше 2 символи.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError("Прізвище є обов’язковим.")
        if not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-]+$', last_name):
            raise forms.ValidationError("Прізвище може містити тільки літери, пробіли або дефіс.")
        if len(last_name) < 2:
            raise forms.ValidationError("Прізвище повинно містити щонайменше 2 символи.")
        return last_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name', '').strip()
        if middle_name and (len(middle_name) < 2 or not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-]+$', middle_name)):
            raise forms.ValidationError("По батькові повинно містити щонайменше 2 літери і тільки допустимі символи.")
        return middle_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError("Телефон є обов’язковим.")
        if not phone.startswith('+380'):
            raise forms.ValidationError("Номер телефону повинен починатися з +380.")
        if not re.match(r'^\+?\d{9,15}$', phone):
            raise forms.ValidationError("Невірний формат номера телефону. Повинен містити від 9 до 15 цифр.")
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone', '').strip()
        middle_name = cleaned_data.get('middle_name', '').strip()
        last_name = cleaned_data.get('last_name', '').strip()
        first_name = cleaned_data.get('first_name', '').strip()

        if not (phone and middle_name and last_name and first_name):
            return cleaned_data

        existing = Recipient.objects.filter( phone=phone, middle_name=middle_name, last_name=last_name, first_name=first_name)

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError("Отримувач з такими даними вже існує.")

        return cleaned_data
