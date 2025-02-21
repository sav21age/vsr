from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from perennials.forms import (PerProductBatchCopyAdminForm)


def perproduct_batch_copy_admin(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = PerProductBatchCopyAdminForm(request.POST)

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

                        if clean['leaves_chk']:
                            recipient.leaves = donor.leaves

                        if clean['flowering_chk']:
                            recipient.flowering.clear()
                            for attr in donor.flowering.all():
                                recipient.flowering.add(attr)

                        if clean['flowering_duration_chk']:
                            recipient.flowering_duration = donor.flowering_duration

                        if clean['flowering_period_chk']:
                            recipient.flowering_period = donor.flowering_period

                        if clean['flower_size_chk']:
                            recipient.flower_size = donor.flower_size

                        if clean['inflorescence_size_chk']:
                            recipient.inflorescence_size = donor.inflorescence_size

                        if clean['planting_chk']:
                            recipient.planting.clear()
                            for attr in donor.planting.all():
                                recipient.planting.add(attr)

                        if clean['shelter_winter_chk']:
                            recipient.shelter_winter = donor.shelter_winter

                        if clean['winter_zone_chk']:
                            recipient.winter_zone = donor.winter_zone

                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = PerProductBatchCopyAdminForm(request.POST)
    else:
        form = PerProductBatchCopyAdminForm(initial={
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


perproduct_batch_copy_admin.short_description = 'Пакетное копирование свойств'
