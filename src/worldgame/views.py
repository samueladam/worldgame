#! -*- coding: utf-8 -*-
from random import shuffle

from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import Country, Highscore
from .forms import CountryForm


def question(request):
    "Shows countries and asks to find one."
    # initialize game
    if 'score' not in request.session:
        request.session['score'] = 0
    if 'played' not in request.session:
        request.session['played'] = []

    # get the next country
    next = Country.objects.svg().exclude(id__in=request.session['played'])[:1]
    if next:
        country = next[0]
    else:
        # game is finished
        redirect('highscore')

    # are we already playing ?
    countries = request.session.get('countries', [])

    if countries:
        # we're playing, do we have an answer?
        answer = request.GET.get('answer', None)

        if answer in ('0', '1', '2', '3'):
            if countries[int(answer)].id == country.id:
                # 3 points for a good guess
                request.session['score'] += 3
                request.session['played'].append(country.id)
                del request.session['countries']
                return redirect('answer', country.name)
            else:
                # -1 for a miss
                request.session['score'] -= 1
                messages.error(request, _('Try again...'))

    else:
        # this is a new game, create the list of four countries
        countries = Country.objects.svg().exclude(id=country.id).order_by('?')[:3]
        countries = [country] + list(countries)
        shuffle(countries)
        request.session['countries'] = countries

    return direct_to_template(request,
                              'worldgame/question.html',
                              {'country': country,
                               'countries': countries,
                               'score': request.session['score']})


def answer(request, name):
    "Shows the correct country on a map."
    country = get_object_or_404(Country, name=name)
    return direct_to_template(request,
                              'worldgame/answer.html',
                              {'country': country,
                               'form': CountryForm(instance=country),
                               'score': request.session['score']})


def reset_score(request):
    "Resets the game."
    for key in ('score', 'played', 'countries'):
        if key in request.session:
            del request.session[key]

    return redirect('question')


def highscore(request):
    "Shows 100 best scores."
    # do we record a score?
    score = request.session.get('score', None)
    name = request.POST.get('name', None)

    if score and name:
        Highscore.objects.create(name=name[:30], score=score)
        del request.session['score']
        return redirect('highscore')

    return object_list(request,
                       Highscore.objects.all()[:100],
                       template_name='worldgame/highscore.html',
                       extra_context={
                            'score': score,
                        })
