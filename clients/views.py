from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from clients.forms import ClientForm
from clients.models import Client
from newsletter.models import Mailing


class ClientListView(ListView):
    model = Client
    template_name = "client/client_list.html"
    context_object_name = "clients"

class ClientDetailView(DetailView):
    model = Client
    template_name = "client/client_detail.html"
    context_object_name = "client"

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_form.html"
    success_url = reverse_lazy("clients:client_list")

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_form.html"
    success_url = reverse_lazy("clients:client_list")

class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client/client_delete.html"
    success_url = reverse_lazy("clients:client_list")


class HomeView(TemplateView):
    template_name = "client/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for mailing in Mailing.objects.all():
            mailing.update_status()

        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="started").count()
        context["unique_clients"] = Client.objects.count()

        context["clients"] = Client.objects.all()

        return context
