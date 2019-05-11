from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.
TABLES_STATUS_FREE = 1
TABLES_STATUS_BOOKED = 2
# PROCESSED = 1
# NOT_PROCESSED = 2

STATUS = (
    (TABLES_STATUS_BOOKED, 'Booked'),
    (TABLES_STATUS_FREE, 'Free')
)

# STATUS_RESERVED = (
#     (PROCESSED, 'Processed'),
#     (NOT_PROCESSED, 'not processed')
# )


class Restaurant(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    image = models.ImageField(upload_to='media/', default='media/photo_2019-05-04 17.39.22.jpeg', blank=True)
    description = models.TextField(blank=True, db_index=True)
    data_pub = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=150, db_index=True, blank=False)
    start_working_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    end_working_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restaurant', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('reserve_create_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('restaurant_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('restaurant_delete_url', kwargs={'slug': self.slug})

    # def get_reserved_url(self):
    #     if self.slug:
    #         return reverse('reserved_list_url', kwargs={'slug': self.slug})
    #     else:
    #         return reverse('reserved_list_url', kwargs={'pk': self.pk})
    def get_reserved_url(self):
        return reverse('reserved_list_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ReservedTables(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    phone = models.IntegerField(blank=False)
    date = models.DateField(auto_now=False, auto_now_add=False, db_index=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, db_index=True)
    #status = models.PositiveSmallIntegerField(choices=STATUS_RESERVED, default=NOT_PROCESSED)
    tables = models.ForeignKey('Tables', related_name='reserved_tables', on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, related_name='reserved_tables', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('reserve_create_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Tables(models.Model):
    title = models.CharField(max_length=150, db_index=True, unique=True)
    number_seats = models.IntegerField(blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=TABLES_STATUS_FREE)
    restaurant = models.ForeignKey(Restaurant, related_name='tables', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tables', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('table_create_url')

    def get_delete_url(self):
        return reverse('table_delete_url', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('table_update_url', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Table "{}" - number seats - {}'.format(self.title, self.number_seats)












