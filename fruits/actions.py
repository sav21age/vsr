from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from fruits.forms import FruitProductBatchCopyAdminForm


def fruitproduct_batch_copy_admin(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = FruitProductBatchCopyAdminForm(request.POST)

        if form.is_valid():
            clean = form.cleaned_data
            donor = form.cleaned_data['object_donor']
            for recipient in queryset:
                try:
                    with transaction.atomic():
                        if clean['scientific_name_chk']:
                            recipient.scientific_name = donor.scientific_name

                        if clean['height_chk']:
                            recipient.height = donor.height

                        if clean['width_chk']:
                            recipient.width = donor.width

                        if clean['advantages_chk']:
                            recipient.advantages.clear()
                            for attr in donor.advantages.all():
                                recipient.advantages.add(attr)

                        if clean['flowering_chk']:
                            recipient.flowering = donor.flowering

                        if clean['self_fertility_chk']:
                            recipient.self_fertility = donor.self_fertility

                        # if clean['rootstock_chk']:
                        #     recipient.rootstock = donor.rootstock

                        if clean['fruit_ripening_chk']:
                            recipient.fruit_ripening = donor.fruit_ripening

                        if clean['fruit_taste_chk']:
                            recipient.fruit_taste = donor.fruit_taste

                        if clean['fruit_dimension_chk']:
                            recipient.fruit_dimension = donor.fruit_dimension

                        if clean['fruit_size_chk']:
                            recipient.fruit_size = donor.fruit_size

                        if clean['fruit_weight_chk']:
                            recipient.fruit_weight = donor.fruit_weight

                        if clean['fruit_keeping_quality_chk']:
                            recipient.fruit_keeping_quality = donor.fruit_keeping_quality

                        if clean['beginning_fruiting_chk']:
                            recipient.beginning_fruiting = donor.beginning_fruiting

                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = FruitProductBatchCopyAdminForm(request.POST)
    else:
        form = FruitProductBatchCopyAdminForm(initial={
            '_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})

    return render(
        request,
        'admin/batch_copy.html',
        {
            'object_recipients': queryset,
            'action': 'batch_copy',
            'form': form,
        }
    )


fruitproduct_batch_copy_admin.short_description = 'Пакетное копирование свойств'
