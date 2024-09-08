from django.urls import path,include
from app import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

#Маршруты для барберов
barber_patterns = [
    path("", views.barbers,name='barbers'),
    path('create', views.barber_create, name='barber_create'),
    path('<int:pk>/update', views.barber_update, name='barber_update'),
    path('<int:pk>/delete', views.barber_delete, name='barber_delete'),
    path('<int:pk>/shifts', views.barber_shifts, name='barber_shifts'),
]

#Маршруты для смен
shifts_patterns = [
    path("", views.shifts,name='shifts'),
    path('create', views.shift_create, name='shift_create'),
    path('<int:pk>/update', views.shift_update, name='shift_update'),
    path('<int:pk>/delete', views.shift_delete, name='shift_delete'),
]

#Маршруты для клиентов
client_patterns = [
    path("", views.clients,name='clients'),
    path('create', views.client_create, name='client_create'),
    path('<int:pk>/update', views.client_update, name='client_update'),
    path('<int:pk>/delete', views.client_delete, name='client_delete'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('', views.index, name='index'),
    path("barbers/", include(barber_patterns)),
    path("shifts/", include(shifts_patterns)),
    path("clients/", include(client_patterns)),
]
