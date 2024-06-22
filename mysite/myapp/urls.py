from django.urls import path
from . import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path('myapp/', views.index, name='index'),
    path('myapp/log_in/', views.check_password, name='check_password'),
    path('myapp/logged_in/', views.display_main_menu, name='display_main_menu'),
    path('myapp/log_out/', views.logout, name='logout'),

    path('myapp/logged_in/users/', views.display_users, name='display_users'),
    path('myapp/logged_in/users/me/', views.display_my_profile, name='display_my_profile'),
    path('myapp/logged_in/users/new/', views.create_user, name='create_user'),
    path('myapp/logged_in/users/<int:user_id>/', views.display_user_detail, name='display_user_detail'),

    path('myapp/logged_in/tickets/', views.display_tickets, name='display_tickets'),
    path('myapp/logged_in/tickets/new/', views.create_ticket, name='create_ticket'),

    path('myapp/logged_in/tickets/<int:ticket_id>/', views.display_ticket_detail, name='display_ticket_detail'),
    path('myapp/logged_in/tickets/<int:ticket_id>/open/', views.open_ticket, name='open_ticket'),
    path('myapp/logged_in/tickets/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),
    path('myapp/logged_in/tickets/<int:ticket_id>/<int:admin_id>/', views.asign_ticket, name='asign_ticket'),
]
