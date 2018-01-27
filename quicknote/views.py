from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from accounts.models import webUser
from chat.models import Room

# Create your views here.
class IndexView(generic.TemplateView):

    rooms = Room.objects.order_by("display_name")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['rooms'] = self.rooms
        return context

    template_name = 'quicknote/index.html'





class SearchView(generic.ListView):

    model = webUser()
