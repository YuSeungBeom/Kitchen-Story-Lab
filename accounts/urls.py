from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
   path('signup/', views.SignUpView.as_view(), name='signup'),  
   path('login/', views.UserLoginView.as_view(), name='login'),
   path('logout/', views.UserLogoutView.as_view(), name='logout'),
   path('profile/', views.ProfileView.as_view(), name='profile'),
   path('change_password/', views.PasswordChangeView.as_view(), name='change_password'),
]