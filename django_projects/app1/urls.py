from django.urls import path

from app1 import views


urlpatterns = [
    path('', views.sign_in, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('user_list/', views.user_list, name='user_list'),
    path('logout/', views.sign_out, name='signout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]
