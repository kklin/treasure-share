from django.shortcuts import render, render_to_response
from django.template import RequestContext
from treasure.models import Donation, Dribble, Recipients, Profile
from . import treasure, profile, dribble


def index(request):
    context = RequestContext(request)
    return render_to_response('treasure/index.jade', {}, context)

def donate(request):
    context = RequestContext(request)
    return render_to_response('treasure/donate.jade', {}, context)

def action(request):
    charity_1 = profile.Profile(request.POST['name_1'])
    charity_1.add_email(request.POST['email_1'])

    charity_2 = profile.Profile(request.POST['name_2'])
    charity_2.add_email(request.POST['email_2'])

    dribble = dribble.Dribble(request.POST['frequency'], request.POST['percentage'], request.POST['delay'])

    charities = []
    charities.append(charity_1)
    charities.append(charity_2)

    donation = Donation(request.POST['donor_name'], charities, request.POST['amount'], dribble)
    #add donation to donation database

    return HttpResponseRedirect('$')
