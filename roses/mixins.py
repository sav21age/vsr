from django.http import Http404
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from common.views import UrlQuerystring


class RoseSpeciesFilterMixinTemplate(TemplateView):
    parent_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = self.request.get_full_path()
        url = UrlQuerystring.delete_param(url, 'page')

        cur = self.parent_context['species_current']

        context['links'] = [{
            'url': UrlQuerystring.delete_param(url, 'species'),
            'name': 'все',
            'active': True if cur is None else False,
        }]

        for value in self.parent_context['species_allowed']:
            context['links'].append({
                'url': UrlQuerystring.get_url(url, 'species', value.id),
                'name': value.name.replace(self.parent_context['genus_name'], '').strip(),
                'active': True if str(value.id) == cur else False,
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
        qs = self.species_model.objects.all()
        if qs:
            context['genus_name'] = 'Роза'
            context['species_allowed'] = qs
            context['species_current'] = self.request.GET.get('species', None)

            context['species_filter'] = RoseSpeciesFilterMixinTemplate.as_view(
                template_name='common/listview/species_filter.html',
                parent_context=context)(self.request)

        return context
