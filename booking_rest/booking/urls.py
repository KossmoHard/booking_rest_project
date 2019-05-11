from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', RestaurantsListView.as_view(), name='restaurants_list_url'),
    path('restaurant/<str:slug>/', ReserveCreateView.as_view(), name='reserve_create_url'),
    path('restaurant/<str:slug>/success/', SuccessDetailView.as_view(), name='success_url'),
    path('control-panel/', ControlPanelListView.as_view(), name='control_panel_url'),
    path('control-panel/restaurants/', ControlPanelRestaurants.as_view(), name='control_panel_restaurants_url'),
    path('control-panel/restaurants/create/', RestaurantCreateView.as_view(), name='restaurant_create_url'),
    path('control-panel/restaurants/<str:slug>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete_url'),
    path('control-panel/restaurants/<str:slug>/update/', RestaurantUpdateView.as_view(), name='restaurant_update_url'),
    path('control-panel/tables/', ControlPanelTables.as_view(), name='control_panel_tables_url'),
    path('control-panel/tables/create/', TableCreateView.as_view(), name='table_create_url'),
    path('control-panel/tables/<int:pk>/delete', TableDeleteView.as_view(), name='table_delete_url'),
    path('control-panel/tables/<int:pk>/update', TableUpdateView.as_view(), name='table_update_url'),
    path('control-panel/<str:slug>/reserved', ControlPanelReserved.as_view(), name='reserved_list_url')
]