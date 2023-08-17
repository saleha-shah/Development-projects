from django.urls import path

from account import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signin/', views.sign_in, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.sign_out, name='signout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
