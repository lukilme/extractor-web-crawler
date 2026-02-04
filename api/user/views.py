from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Conta criada com sucesso! Faça login para continuar.'
        )
        return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect('news:feed')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.username}!')
            
            if user.is_admin_user():
                return redirect('scraper:dashboard')
            return redirect('news:feed')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('/')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {
        'form': form
    })