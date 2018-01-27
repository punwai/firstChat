from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class RegisterView(generic.View):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, self.template_name, {'form': form, 'invalid': 'account invalid'})
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'invalid': ''})

@login_required
def logout_view(request):
    logout(request)

class ProfileView(generic.TemplateView):
    template_name = 'accounts/profile.html'
