from django import forms
from django.contrib.auth import authenticate, get_user_model

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(
                email=email,
                password=password
            )

            if not user:
                raise forms.ValidationError("E-mail ou senha inválidos.")

            cleaned_data["user"] = user

        return cleaned_data


User = get_user_model()

class RegisterForm(forms.Form):
    name = forms.CharField(label="Nome completo", max_length=255)
    username = forms.CharField(label="Usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput
    )
    password_repeat = forms.CharField(
        label="Repita a senha",
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nome de usuário já está em uso."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_repeat")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(
                "As senhas não coincidem."
            )

        return cleaned_data

    def save(self):
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            name=self.cleaned_data["name"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
