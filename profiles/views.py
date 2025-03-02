from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from common.mixins import LoginRequiredMixin
from favorites.models import Favorites
from orders.models import Order, OrderItem
from profiles.forms import ProfileUpdateForm
from pure_pagination.mixins import PaginationMixin


class ProfileIndex(LoginRequiredMixin, View):
    template_name = 'profiles/index.html'

    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name
        )


@login_required
def profile_update(request):
    context = {}
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            user = User.objects.get(id=request.user.pk)
            user.profile.phone_number = clean['phone_number']
            user.profile.save()
            user.first_name = clean['first_name']
            user.last_name = clean['last_name']
            user.save()
            return redirect(reverse('profiles:index'))

        context['form'] = ProfileUpdateForm(request.POST)

    else:
        context['form'] = ProfileUpdateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone_number': request.user.profile.phone_number,
        })

    return render(
        request,
        'profiles/update_form.html',
        context,
    )


class ProfileFavorites(LoginRequiredMixin, PaginationMixin, ListView):
    model = Favorites
    template_name = 'profiles/favorites_list.html'
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
            .prefetch_related('order_items')
            # .prefetch_related('order_items__content_object')

        return qs


class ProfileOrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'profiles/order_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) \
            .select_related('status') \
            .prefetch_related('order_items')
            # .prefetch_related('order_items__content_object')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get(self.pk_url_kwarg)
        context['order_items'] = OrderItem.objects.filter(order_id=pk)

        return context
