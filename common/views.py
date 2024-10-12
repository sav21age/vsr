from urllib.parse import urlencode, urlparse, urlunparse, parse_qs, urlsplit
from django.urls import resolve, reverse
from django.views.generic import TemplateView
from django.template.loader import render_to_string

from plants.models import PlantDivision


# def cut_page_query(q):
#     p = re.compile(r'(page=)[^&]*')
#     q = p.sub('', q)
#     # q = re.sub(r'(page=)[^&]*', '', q)
#     return q.strip('&')


# def set_querystring(request, param, value):
#     q = urllib.parse.urlsplit(request.get_full_path()).query

#     if request.GET.get('page', None):
#         q = cut_page_query(q)

#     if request.GET.get(param, None):
#         p = re.compile(r'({}=)[^&]*'.format(param))
#         q = p.sub(r'\g<1>' + f"{value}", q)
#     else:
#         if q:
#             q += '&'
#         q += f"{param}={value}"
#     return q


# def cut_param_querystring(request, param):
#     q = urllib.parse.urlsplit(request.get_full_path()).query

#     if request.GET.get('page', None):
#         q = cut_page_query(q)

#     if request.GET.get(param, None):
#         p = re.compile(r'({}=)[^&]*'.format(param))
#         q = p.sub('', q)
#         # q = re.sub(r'({}=)[^&]*'.format(param), '', q)
#         q = q.strip('&')
#     return q


class UrlQuerystring():

    @staticmethod
    def get_url(url, param, value):
        # u = urlparse(request.get_full_path())
        u = urlparse(url)
        query = parse_qs(u.query, keep_blank_values=True)
        
        # query.pop('page', None)
        query[param] = value
        
        u = u._replace(query=urlencode(query, True))
        return(urlunparse(u))

    @staticmethod
    def delete_param(url, param):
        # u = urlparse(request.get_full_path())
        u = urlparse(url)
        query = parse_qs(u.query, keep_blank_values=True)
        
        # query.pop('page', None)
        query.pop(param, None)
        
        u = u._replace(query=urlencode(query, True))
        return(urlunparse(u))


class PerPageMixinTemplate(TemplateView):
    parent_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = self.request.get_full_path()
        url = UrlQuerystring.delete_param(url, 'page')

        context['options'] = []
        for value in self.parent_context['per_page_allowed']:
            context['options'].append({
                'querystring': UrlQuerystring.get_url(url, 'per_page', value),
                'name': value,
                'selected': True if value == self.parent_context['per_page_current'] else False,
            })

        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_string(self.template_name, context, request=self.request)


class PlantDivisionFilterMixinTemplate(TemplateView):
    parent_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = self.request.get_full_path()

        cur = self.parent_context['division_current']

        context['options'] = [{
            'querystring': UrlQuerystring.delete_param(url, 'division'),
            'name': 'Все',
            'selected': True if '' == cur else False,
        }]

        for value in self.parent_context['division_allowed']:
            context['options'].append({
                'querystring': UrlQuerystring.get_url(url, 'division', value.id),
                # 'name': value.name,
                'name': dict(PlantDivision.CHOICES)[value.name],
                'selected': True if str(value.id) == cur else False,
            })


        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_string(self.template_name, context, request=self.request)


class PlantGenusFilterMixinTemplate(TemplateView):
    parent_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # resolved = resolve(self.request.path_info)
        # print(resolved)
        # # reversed = reverse("admin:app_list", kwargs={"app_label": "auth"})
        # # reversed = reverse(
        # #     f"{resolved.app_names[0]}:{resolved.url_name}", kwargs=resolved.kwargs)
        # reversed = reverse(
        #     f"{resolved.app_names[0]}:list", kwargs={})
        # print(reversed)

        # q = urlsplit(self.request.get_full_path()).query
        # print(f"path: {urlsplit(self.request.get_full_path()).path}")
        # query = parse_qs(q, keep_blank_values=False)
        # # print(query)
        # query.pop('per_page', None)
        # # print(f"query: {query}")
        # print(urlencode(query, True))
    
        url = self.request.get_full_path()
        url = UrlQuerystring.delete_param(url, 'page')
        url = UrlQuerystring.delete_param(url, 'species')

        cur = self.parent_context['genus_current']

        context['options'] = [{
            'querystring': UrlQuerystring.delete_param(url, 'genus'),
            'name': 'Все',
            'selected': True if '' == cur else False,
        }]

        for value in self.parent_context['genus_allowed']:
            context['options'].append({
                'querystring': UrlQuerystring.get_url(url, 'genus', value.id),
                'name': value.name,
                'selected': True if str(value.id) == cur else False,
            })


        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_string(self.template_name, context, request=self.request)


class PlantSpeciesFilterMixinTemplate(TemplateView):
    parent_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = self.request.get_full_path()
        url = UrlQuerystring.delete_param(url, 'page')

        cur = self.parent_context['species_current']

        context['links'] = [{
            'url': UrlQuerystring.delete_param(url, 'species'),
            'name': 'все',
            'title': 'все',
            'active': True if cur is None else False,
        }]

        for value in self.parent_context['species_allowed']:
            genus_name = self.parent_context['genus_name']
            species_title = value.name
            species_name = value.name

            if species_name.startswith(genus_name) and species_name != genus_name:
                species_name = species_name.replace(genus_name, '').strip()
            else:
                if len(species_name) > 0:
                    species_name = species_name[0].lower() + species_name[1:]
            
            context['links'].append({
                'url': UrlQuerystring.get_url(url, 'species', value.id),
                'name': species_name,
                'title': species_title,
                'active': True if str(value.id) == cur else False,
            })

        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_string(self.template_name, context, request=self.request)
