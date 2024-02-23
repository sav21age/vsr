from django.conf import settings
from search.forms import SearchForm

def main(request):
    context = {
      'debug': settings.DEBUG,
      'cache_timeout': settings.CACHE_TIMEOUT,
      'rel_canonical': request.build_absolute_uri(request.path),
      'host': '{0}://{1}'.format(request.is_secure() and 'https' or 'http', request.get_host()),
      'search_form': SearchForm(request.GET),
    }
    return context
