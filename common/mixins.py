from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator

from common.views import PerPageMixinTemplate, PlantDivisionFilterMixinTemplate
from plants.models import PlantDivision

# from django.db.models import QuerySet 


class LoginRequiredMixin():
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PerPageMixin():
    per_page_allowed = (12, 24, 36, 48, 60)
    per_page_default = 12

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page', None)

        if per_page:
            try:
                per_page = int(per_page)
            except ValueError:
                pass

            if per_page in self.per_page_allowed:
                self.per_page_default = per_page

        return self.per_page_default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page_allowed'] = self.per_page_allowed
        context['per_page_current'] = self.per_page_default

        context['per_page'] = PerPageMixinTemplate.as_view(
            template_name='common/listview/per_page.html',
            parent_context=context)(self.request)
        return context


class RecommendedDetailMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context['object']
        context['recommended'] = self.model.is_visible_objects \
            .filter(species=obj.species) \
            .prefetch_related('images') \
            .prefetch_related('prices') \
            .exclude(id=obj.id)\
            .distinct()[:4]

        return context


class PlantDivisionFilterMixin():
    division_id = None

    def get_queryset(self):
        qs = super().get_queryset()

        self.division_id = self.request.GET.get('division', None)
        if self.division_id and self.division_id.isnumeric() and self.division_id.isdigit():
            qs = qs.filter(division__id=self.division_id)
            if not qs:
                raise Http404
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        qs = self.model.is_visible_objects \
            .values_list('division_id', flat=True).distinct()[:]
        lst = list(qs)

        if len(lst) < 2:
            return context
        
        context['division_allowed'] = PlantDivision.objects.filter(id__in=lst)
        context['division_current'] = self.division_id
        context['division_filter'] = PlantDivisionFilterMixinTemplate.as_view(
            template_name='common/listview/division_filter.html',
            parent_context=context)(self.request)
        
        return context


# class PlantGenusFilterMixin():
#     genus_id = None

#     def get_queryset(self):
#         qs = super().get_queryset()

#         self.genus_id = self.request.GET.get('genus', None)
#         if self.genus_id and self.genus_id.isnumeric():
#             try:
#                 qs = qs.filter(species__genus__id=self.genus_id)
#             except ValueError as e:
#                 raise Http404 from e

#             if not qs:
#                 raise Http404
            
#         return qs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         qs = self.species_model.objects \
#             .values_list('genus_id', flat=True).distinct()[:]
#         lst = list(qs)
#         context['genus_allowed'] = PlantGenus.objects.filter(
#             division__name=self.division_name).filter(id__in=lst)

#         context['genus_current'] = self.genus_id
        
#         context['genus_filter'] = PlantGenusFilterMixinTemplate.as_view(
#             template_name='common/listview/genus_filter.html',
#             parent_context=context)(self.request)
        
#         return context
    

# class PlantSpeciesFilterMixin():
#     species_id = None

#     def get_queryset(self):
#         qs = super().get_queryset()
#         self.species_id = self.request.GET.get('species', None)
        
#         if self.species_id and self.species_id.isnumeric():
#             try:
#                 qs = qs.filter(species__id=self.species_id)
#             except ValueError:
#                 raise Http404

#             if not qs:
#                 raise Http404

#         return qs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         genus_id = self.request.GET.get('genus', None)
#         if genus_id and not genus_id.isnumeric():
#             raise Http404

#         try:
#             qs = self.species_model.objects.filter(genus_id=genus_id)
#         except ValueError:
#             raise Http404

#         if genus_id and qs.count() > 1:
#             context['genus_name'] = PlantGenus.objects.filter(id=genus_id).get().name
#             context['species_allowed'] = qs
#             context['species_current'] = self.species_id

#             context['species_filter'] = PlantSpeciesFilterMixinTemplate.as_view(
#                 template_name='common/listview/species_filter.html',
#                 parent_context=context)(self.request)

#         return context
