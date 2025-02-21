from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from roses.forms import (RoseProductBatchCopyAdminForm)


def roseproduct_batch_copy_admin(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = RoseProductBatchCopyAdminForm(request.POST)

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

                        if clean['flowering_chk']:
                            recipient.flowering = donor.flowering

                        if clean['quantity_on_stem_chk']:
                            recipient.quantity_on_stem = donor.quantity_on_stem

                        if clean['flavor_chk']:
                            recipient.flavor = donor.flavor

                        if clean['flower_size_chk']:
                            recipient.flower_size = donor.flower_size

                        if clean['resistance_fungus_chk']:
                            recipient.resistance_fungus = donor.resistance_fungus

                        if clean['resistance_rain_chk']:
                            recipient.resistance_rain = donor.resistance_rain

                        if clean['shelter_winter_chk']:
                            recipient.shelter_winter = donor.shelter_winter

                        if clean['winter_zone_chk']:
                            recipient.winter_zone = donor.winter_zone

                        if clean['advantages_chk']:
                            recipient.advantages.clear()
                            for attr in donor.advantages.all():
                                recipient.advantages.add(attr)
                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = RoseProductBatchCopyAdminForm(request.POST)
    else:
        form = RoseProductBatchCopyAdminForm(initial={
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


roseproduct_batch_copy_admin.short_description = 'Пакетное копирование свойств'
