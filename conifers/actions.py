from django.shortcuts import render
from django.db import transaction
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages
from django.http import HttpResponseRedirect
from conifers.forms import ConiferProductBatchCopyAdminForm


def coniferproduct_batch_copy_admin(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = ConiferProductBatchCopyAdminForm(request.POST)

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

                        if clean['needles_chk']:
                            recipient.needles = donor.needles

                        if clean['needles_chk']:
                            recipient.needles = donor.needles

                        if clean['height10_chk']:
                            recipient.height10 = donor.height10

                        if clean['width10_chk']:
                            recipient.width10 = donor.width10

                        if clean['height1_chk']:
                            recipient.height1 = donor.height1

                        if clean['width1_chk']:
                            recipient.width1 = donor.width1

                        if clean['planting_chk']:
                            recipient.planting.clear()
                            for attr in donor.planting.all():
                                recipient.planting.add(attr)

                        if clean['shelter_chk']:
                            recipient.shelter = donor.shelter

                        if clean['winter_zone_chk']:
                            recipient.winter_zone = donor.winter_zone

                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = ConiferProductBatchCopyAdminForm(request.POST)
    else:
        form = ConiferProductBatchCopyAdminForm(initial={
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


coniferproduct_batch_copy_admin.short_description = 'Пакетное копирование свойств'
