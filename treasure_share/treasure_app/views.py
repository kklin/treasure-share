from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from treasure_app.models import Dribble, Recipients, Profile
import treasure, profile, dribble, multisig
from oauth2client.client import OAuth2WebServerFlow
import httplib2
from secrets import CALLBACK_URL, CLIENT_ID, CLIENT_SECRET
from django.http import HttpResponseRedirect, HttpResponse



def index(request):
    context = RequestContext(request)
    return render_to_response('treasure/index.jade', {}, context)

def donate(request):
    context = RequestContext(request)
    return render_to_response('treasure/donate.jade', {}, context)

def action(request):
    print(request.POST)
    
    charity_1 = profile.Profile(request.POST['name_1'])
    charity_1.add_email(request.POST['email_1'])

    charity_2 = profile.Profile(request.POST['name_2'])
    charity_2.add_email(request.POST['email_2'])

    dribble_obj = dribble.Dribble(float(request.POST['frequency']), float(request.POST['percentage']), float(request.POST['delay']))

    charities = []
    charities.append(charity_1)
    charities.append(charity_2)

    donation = Donation(request.POST['donor_name'], charities, float(request.POST['amount']), dribble_obj, request.session['oauth_json'])
    #add donation to donation database

    return HttpResponseRedirect('/')

def withdraw(request):
    context = RequestContext(request)
    return render_to_response('treasure/withdraw.jade', {}, context)

def action_withdraw(request):
    sf_wallet_id = request.POST['sf_wallet_id']
    sf_key = request.POST['sf_key']
    sf_key2 = request.POST['sf_key2']
    dest_id = request.POST['dest_id']
    amount = float(request.POST['amount'])

    keys = [ key_from_private_key(sf_key), key_from_private_key(sf_key2) ]

    account = multisig.get_account(request.session['oauth_json'])
    multisig.send_from(account = account, keys = keys, account_id = sf_wallet_id, to_address = dest_id, amount = amount)
    return HttpResponseRedirect('/')

coinbase_client = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, 'all', redirect_uri='https://198.199.112.146/auth2', auth_uri='https://www.coinbase.com/oauth/authorize', token_uri='https://www.coinbase.com/oauth/token')

def ty_donate(request):
    context = RequestContext(request)
    return render_to_response('treasure/ty_donate.jade', {}, context)

def ty_withdraw(request):
    context = RequestContext(request)
    return render_to_response('treasure/ty_withdraw.jade', {}, context)

def auth(request):
  auth_url = coinbase_client.step1_get_authorize_url()
  return redirect(auth_url)

def auth2(request):
    oauth_code = request.GET['code']

    print(oauth_code)

    http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')

    token = coinbase_client.step2_exchange(oauth_code, http=http)
    print(token.to_json())
    #response = HttpResponse(token.to_json(), content_type = 'text/plain')
    request.session['oauth_json'] = token.to_json()
    return redirect('/donate/')

def display_oauth(request):
    response = HttpResponse(request.session['oauth_json'], content_type = 'text/plain')
    return response
