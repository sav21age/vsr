from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from contacts.models import Contacts


def contacts(request):
    try:
        obj = Contacts.objects.get()
    except ObjectDoesNotExist as e:
        raise Http404 from e

    response = render(
        request,
        'contacts/index.html',
        {'object': obj, }
    )
    return response
