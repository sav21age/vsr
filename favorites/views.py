import json
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse


@login_required
def favorites(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        return HttpResponse(status=405)
    
    user = request.user

    if request.GET.get('id') and (request.GET.get('id')).isdigit():
        object_id = request.GET.get('id')
    else:
        return HttpResponse(status=404)

    try:
        content_type = ContentType.objects.get_for_id(
            request.GET.get('ct_id'))
    except:
        return HttpResponse(status=404)

    try:
        content_type.get_object_for_this_type(pk=object_id)
    except:
        return HttpResponse(status=404)

    if user.favorites_set.filter(content_type=content_type, object_id=object_id):
        user.favorites_set.get(content_type=content_type,
                                object_id=object_id).delete()
        state = False
    else:
        user.favorites_set.create(
            content_type=content_type, object_id=object_id)
        state = True

    response = {
        'state': state,
    }

    return HttpResponse(json.dumps(response))




# def favorites(request):
#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_authenticated:
#         user = request.user

#         app_label = request.GET.get('a', None)
#         if not app_label:
#             return HttpResponse(status=405)

#         model_name = request.GET.get('m', None)
#         if not model_name:
#             return HttpResponse(status=405)

#         if request.GET.get('id') and (request.GET.get('id')).isdigit():
#             object_id = request.GET.get('id')
#         else:
#             return HttpResponse(status=405)

#         try:
#             model = apps.get_model(app_label, model_name)
#         except LookupError:
#             return HttpResponse(status=405)

#         content_type = ContentType.objects.get_for_model(model)

#         try:
#             content_type.get_object_for_this_type(pk=object_id)
#         except model.DoesNotExist:
#             return HttpResponse(status=404)

#         if user.favorites_set.filter(content_type=content_type, object_id=object_id):
#             user.favorites_set.get(content_type=content_type,
#                                   object_id=object_id).delete()
#             state = False
#         else:
#             user.favorites_set.create(
#                 content_type=content_type, object_id=object_id)
#             state = True

#         response = {
#             'state': state,
#         }

#         return HttpResponse(json.dumps(response))

#     raise Http404
