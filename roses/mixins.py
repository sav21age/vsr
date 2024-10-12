from django.http import Http404
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from common.views import UrlQuerystring
from roses.models import RoseProduct


class RoseSpeciesFilterMixinTemplate(TemplateView):
    parent_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = self.request.get_full_path()
        url = UrlQuerystring.delete_param(url, 'page')

        cur = self.parent_context['species_current']

        context['options'] = [{
            'querystring': UrlQuerystring.delete_param(url, 'species'),
            'name': 'Все',
            'selected': True if cur is None else False,
        }]

        for value in self.parent_context['species_allowed']:
            context['options'].append({
                'querystring': UrlQuerystring.get_url(url, 'species', value.id),
                'name': value.name.replace(self.parent_context['genus_name'], '').strip().capitalize(),
                'selected': True if str(value.id) == cur else False,
            })

        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_string(self.template_name, context, request=self.request)


class RoseSpeciesFilterMixin():
    def get_queryset(self):
        qs = super().get_queryset()
        species = self.request.GET.get('species', None)
        if species:
            qs = qs.filter(species__id=species)
            if not qs:
                raise Http404

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # qs = self.species_model.objects.all()

        qs = RoseProduct.is_visible_objects \
            .values_list('species_id', flat=True).distinct()[:]
        lst = list(qs)

        if qs:
            context['genus_name'] = 'Роза'
            # context['species_allowed'] = qs

            context['species_allowed'] = self.species_model.objects.filter(id__in=lst)

            context['species_current'] = self.request.GET.get('species', None)

            context['species_filter'] = RoseSpeciesFilterMixinTemplate.as_view(
                template_name='roses/species_filter.html',
                parent_context=context)(self.request)

        return context
