from django.http import HttpResponseRedirect
from django.urls import reverse
from allauth.account.auth_backends import AuthenticationBackend
from carts.models import Cart


# class MyAuthenticationBackend(AuthenticationBackend):
#     def authenticate(self, request, **credentials):
#         user = super().authenticate(request, **credentials)
#         if user.custom_field == True:
#             return user
#         else:
#             return None


class SessionAuthenticationBackend(AuthenticationBackend):
    def authenticate(self, request, **credentials):
        print(f"sc -> {request.session.session_key}")
        a = super().authenticate(request, **credentials)
        print(f"sc <- {request.session.session_key}")
        
        # session_key = request.session.session_key

        # if request.user:
        #     if session_key:
        #         Cart.objects.filter(session_key=session_key).update(user=user)

        return a
