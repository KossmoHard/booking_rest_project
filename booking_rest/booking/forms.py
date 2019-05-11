from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget

from .models import Restaurant, Tables, ReservedTables

TABLES_STATUS_FREE = 1
TABLES_STATUS_BOOKED = 2


class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['title', 'slug', 'image', 'description', 'city', 'start_working_time', 'end_working_time']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'start_working_time': forms.TimeInput(attrs={'class': 'form-control'}, format='%H:%M'),
            'end_working_time': forms.TimeInput(attrs={'class': 'form-control'}, format='%H:%M'),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Restaurant.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
        return new_slug


class TableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TableForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].queryset = Restaurant.objects.filter(user=self.user)

    class Meta:
        model = Tables
        fields = ['title', 'number_seats', 'status', 'restaurant']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'number_seats': forms.Select(
                attrs={'class': 'form-control'},
                choices=[(o, str(o)) for o in range(1, 16)]
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'restaurant': forms.Select(attrs={'class': 'form-control'})

        }

    def clean_title(self):
        new_title = self.cleaned_data['title'].lower()
        if new_title == 'create':
            raise ValidationError('Slug may not be "Create"')
        else:
            return new_title


class ReservedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.restaurant = kwargs.pop('restaurant', None)
        super(ReservedForm, self).__init__(*args, **kwargs)
        self.fields['tables'].queryset = Tables.objects.filter(restaurant=self.restaurant, status=TABLES_STATUS_FREE)

    class Meta:
        model = ReservedTables
        fields = ['name', 'phone', 'date', 'time', 'tables']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'tables': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if ReservedTables.objects.filter(
            restaurant=self.restaurant,
            date=cleaned_data['date'],
            time=cleaned_data['time'],
        ):
            self.add_error('tables', 'Place already booked. Please choose another table!')
