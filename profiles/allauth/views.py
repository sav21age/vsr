from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from allauth.account.views import LogoutView
from allauth.account.views import PasswordChangeView
from common.mixins import LoginRequiredMixin
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
