from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.edit import CreateView, FormView
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 

class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm                                                                                                

    def form_valid(self, form):
        usuario = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, "Inicio de sesión exitoso.")
            return HttpResponseRedirect(
                reverse("home")
            )
        
        else: 
            messages.add_message(
                self.request, messages.ERROR, ("Usuario no válido o contraseña no válida."))
            return super(LoginView, self).form_invalid(form)
    
class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy("login")
    form_class = RegistrationForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView, self).form_valid(form)
    
@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "se ha cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse("home"))

