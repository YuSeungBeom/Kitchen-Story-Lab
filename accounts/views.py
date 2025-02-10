from django.views.generic import CreateView, FormView, UpdateView, TemplateView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        self.request.user = user
        messages.success(self.request, '회원가입이 완료되었습니다.')
        return response

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        messages.success(self.request, '로그인되었습니다.')
        return reverse_lazy('blog:post_list')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, '로그아웃되었습니다.')
        return redirect('blog:post_list')

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '프로필이 업데이트되었습니다.')
        return response

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '비밀번호가 변경되었습니다.')
        return response