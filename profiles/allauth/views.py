from allauth.account.signals import user_signed_up, user_logged_in
from allauth.account.views import SignupView, LoginView, LogoutView
from allauth.account.auth_backends import AuthenticationBackend
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from allauth.account.views import PasswordChangeView
from carts.models import Cart
from common.mixins import LoginRequiredMixin
import allauth.account.views as auth_views
from django.utils.decorators import method_decorator
from common.sessions import persist_session_vars


class RedirectedPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('profiles:index')


@method_decorator(persist_session_vars(['cart_id',]), name='dispatch')
class PersistLogoutView(LogoutView):
    pass


# class PersistLogoutView(LogoutView):
    
#     @method_decorator(persist_session_vars(['cart_id',]))
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)


# class AccountLoginView(LoginView):
#     def dispatch(self, request, *args, **kwargs):
#         print(f"dispatch - sc before: {request.session.session_key}")
#         s = super().dispatch(request, *args, **kwargs)
#         print(f"dispatch - sc after: {request.session.session_key}")
#         return s
    
#     def form_valid(self, form):
#         print(f"form valid before - sc before: {self.request.session.session_key}")
#         s = super().form_valid(form)
#         print(f"form valid after - sc before: {self.request.session.session_key}")
#         return s


# account_login_view = AccountLoginView.as_view()

# @receiver(user_logged_in)
# def logged_in(sender, **kwargs):
#     print(f"signal - sc: {kwargs['request'].session.session_key}")


# class SessionAuthenticationBackend(AuthenticationBackend):
#     def authenticate(self, request, **credentials):
#         user = super().authenticate(request, **credentials)
#         session_key = request.session.session_key

#         if user:
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))
                    
#         return HttpResponseRedirect(reverse('main:index'))

# AUTH_USER_MODEL = 'your_app_name.CustomUser'
    
# class AccountSignupView(SignupView):
#     # Signup View extended

#     # change template's name and path
#     template_name = "users/custom_signup.html"

#     # You can also override some other methods of SignupView
#     # Like below:
#     # def form_valid(self, form):
#     #     ...
#     #
#     # def get_context_data(self, **kwargs):
#     #     ...

# account_signup_view = AccountSignupView.as_view()
# Then, update your URL configuration to use this custom view.