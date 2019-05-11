from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import RestaurantForm, TableForm, ReservedForm

TABLES_STATUS_FREE = 1
TABLES_STATUS_BOOKED = 2


class MenuMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_reserved'] = Restaurant.objects.filter(user=self.request.user)
        return context


class RestaurantsListView(ListView):
    model = Restaurant
    template_name = 'booking/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class RestaurantCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = RestaurantForm
    template_name = 'booking/control-panel/restaurant_create.html'
    success_url = reverse_lazy('control_panel_restaurants_url')

    def form_valid(self, form):
        restaurant = form.instance
        restaurant.user = self.request.user

        return super().form_valid(form)


class TableCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = TableForm
    template_name = 'booking/control-panel/table_create.html'

    def get_form_kwargs(self):
        kwargs = super(TableCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        table = form.instance
        table.user = self.request.user

        return super().form_valid(form)


class ReserveCreateView(CreateView):
    form_class = ReservedForm
    template_name = 'booking/restaurant_detail.html'

    def get_form_kwargs(self):
        form_kw = super(ReserveCreateView, self).get_form_kwargs()
        form_kw['restaurant'] = Restaurant.objects.get(slug__iexact=self.kwargs['slug'])
        return form_kw

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Restaurant.objects.get(slug__iexact=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(slug__iexact=self.kwargs['slug'])
        form.instance.restaurant = restaurant
        #form.instance.tables.status = TABLES_STATUS_BOOKED
        #form.instance.tables.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('success_url', kwargs={'slug': self.kwargs['slug']})


class SuccessDetailView(DetailView):
    model = Restaurant
    template_name = 'booking/success.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['reserved_object'] = ReservedTables.objects.filter(restaurant=self.object)


class ControlPanelListView(LoginRequiredMixin, MenuMixin, ListView):
    model = Restaurant
    template_name = 'booking/control-panel/index.html'

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        context['object_tables_list'] = Tables.objects.filter(user=self.request.user)
        return context


class ControlPanelRestaurants(LoginRequiredMixin, MenuMixin, ListView):
    model = Restaurant
    template_name = 'booking/control-panel/restaurants_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class RestaurantDeleteView(LoginRequiredMixin, MenuMixin, DeleteView):
    model = Restaurant
    template_name = 'booking/control-panel/restaurant_delete.html'
    success_url = reverse_lazy('control_panel_restaurants_url')


class RestaurantUpdateView(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'booking/control-panel/restaurant_update.html'
    success_url = ''


class ControlPanelTables(LoginRequiredMixin, MenuMixin, ListView):
    model = Tables
    template_name = 'booking/control-panel/tables_list.html'
    context_object_name = 'object_tables_list'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TableUpdateView(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Tables
    form_class = TableForm
    template_name = 'booking/control-panel/table_update.html'
    success_url = reverse_lazy('control_panel_tables_url')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class TableDeleteView(LoginRequiredMixin, MenuMixin, DeleteView):
    model = Tables
    template_name = 'booking/control-panel/table_delete.html'
    success_url = reverse_lazy('control_panel_tables_url')


class ControlPanelReserved(LoginRequiredMixin, MenuMixin, ListView):
    model = ReservedTables
    template_name = 'booking/control-panel/reserved_tables_list.html'

    def get_queryset(self):
        restaurant = Restaurant.objects.get(slug__iexact=self.kwargs['slug'], user=self.request.user)
        return self.model.objects.filter(restaurant=restaurant)