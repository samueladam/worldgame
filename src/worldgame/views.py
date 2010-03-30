#! -*- coding: utf-8 -*-
from django.db import transaction
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import Country
from .forms import CountryForm

PAGINATE_BY = 30

def list_country(request):
    "List every country."
    return object_list(request,
                       Country.objects.all(),
                       paginate_by=PAGINATE_BY,
                       template_name='worldgame/list.html',
                       extra_context={})

def show_country(request, id):
    "Show an country."
    country = get_object_or_404(Country, pk=id)
    return direct_to_template(request,
                              'worldgame/object.html',
                              {'object': country})

@login_required
@transaction.commit_on_success
def edit_country(request, id=None, delete=False):
    "Create, delete or edit an country."

    if id:
        country = get_object_or_404(Country, pk=id)

        if delete:
            country.delete()
            messages.success(request, _('deleted.'))
            return redirect('list_country')

    else:
        country = Country()

    form = CountryForm(request.POST or None,
                       request.FILES or None,
                       instance=country)

    if form.is_valid():
        country = form.save(commit=False)
        country.user = request.user
        country.save()

        messages.success(request, _('updated.'))

        return redirect(country)

    return direct_to_template(request,
                              'worldgame/form.html',
                              {'form': form})



