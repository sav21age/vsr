from django.shortcuts import render
from django.db import transaction
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages
from django.http import HttpResponseRedirect
from deciduous.forms import DecProductBatchCopyAdminForm


def decproduct_batch_copy_admin(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = DecProductBatchCopyAdminForm(request.POST)

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

                        if clean['crown_chk']:
                            recipient.crown = donor.crown

                        if clean['flowering_chk']:
                            recipient.flowering = donor.flowering

                        if clean['flowering_period_chk']:
                            recipient.flowering_period = donor.flowering_period

                        if clean['flower_size_chk']:
                            recipient.flower_size = donor.flower_size

                        if clean['inflorescence_chk']:
                            recipient.inflorescence = donor.inflorescence

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
            form = DecProductBatchCopyAdminForm(request.POST)
    else:
        form = DecProductBatchCopyAdminForm(initial={
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


decproduct_batch_copy_admin.short_description = 'Пакетное копирование свойств'
