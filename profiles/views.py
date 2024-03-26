from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from common.mixins import LoginRequiredMixin
from favorites.models import Favorites
from orders.models import Order, OrderItem
from profiles.forms import ProfileUpdateForm
from profiles.models import Profile
from pure_pagination.mixins import PaginationMixin


class ProfileIndex(LoginRequiredMixin, View):
    template_name = 'profiles/index.html'

    def get(self, request, *args, **kwargs):
        context = {}

        try:
            context['object'] = User.objects.get(id=self.request.user.pk)
        except User.DoesNotExist:
            raise Http404

        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )


@login_required
def profile_update(request):
    context = {}
    obj = Profile.objects.get(user_id=request.user.pk)

    if not obj:
        raise Http404

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            obj.phone_number = clean['phone_number']
            obj.save()
            user = User.objects.get(id=request.user.pk)
            user.first_name = clean['first_name']
            user.last_name = clean['last_name']
            user.save()
            return redirect(reverse('profiles:index'))

        context['form'] = ProfileUpdateForm(request.POST)

    else:
        context['form'] = ProfileUpdateForm(initial={
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'phone_number': obj.phone_number,
        })

    return render(
        request,
        'profiles/update_form.html',
        context,
    )


class ProfileFavorites(LoginRequiredMixin, PaginationMixin, ListView):
    model = Favorites
    template_name = 'profiles/favorites.html'
    paginate_by = 8

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) \
            .prefetch_related('content_object') \
            .prefetch_related('content_object__images')

        return qs


# class ProfileCart(PaginationMixin, LoginRequiredMixin, ListView):
#     model = Favorites
#     template_name = 'profiles/cart.html'
#     paginate_by = 8

#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.filter(user=self.request.user) \
#             .prefetch_related('content_object')

#         return qs


class ProfileOrderList(LoginRequiredMixin, PaginationMixin, ListView):
    model = Order
    template_name = 'profiles/order_list.html'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) \
            .select_related('status') \
            .prefetch_related('order_items') \
            .prefetch_related('order_items__content_object')

        return qs


class ProfileOrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'profiles/order_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) \
            .select_related('status') \
            .prefetch_related('order_items') \
            .prefetch_related('order_items__content_object')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get(self.pk_url_kwarg)
        context['object_list'] = OrderItem.objects.filter(order_id=pk)

        return context
