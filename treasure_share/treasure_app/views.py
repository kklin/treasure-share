from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from treasure_app.models import Dribble, Recipients, Profile
from treasure import Donation
import treasure, profile, dribble, multisig, key_funcs
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
    sf_wallet_id = request.POST['sf_wallet_id'].encode('utf8')
    sf_key = request.POST['sf_key'].encode('utf8')
    sf_key2 = request.POST['sf_key2'].encode('utf8')
    dest_id = request.POST['dest_id'].encode('utf8')
    amount = float(request.POST['amount'])

    keys = [ key_funcs.key_from_private_key(sf_key), key_funcs.key_from_private_key(sf_key2) ]

    account = multisig.get_account(request.session['oauth_json'])
    multisig.multisig_send_from(account = account, keys = keys, account_id = sf_wallet_id, address = dest_id, amount = amount)
    return HttpResponseRedirect('/')

def transaction(request):
    return render_to_response('treasure/sign_transaction.jade', {}, RequestContext(request))

def sign_transaction(request):
    account_id = request.POST['account_id'].encode('utf8')
    sf_key = request.POST['sf_key'].encode('utf8')
    sf_key2 = request.POST['sf_key2'].encode('utf8')
    transaction_id = request.POST['transaction_id'].encode('utf8')

    keys = [ key_funcs.key_from_private_key(sf_key), key_funcs.key_from_private_key(sf_key2) ]

    account = multisig.get_account(request.session['oauth_json'])
    resp = multisig.multisig_sign_from_transaction(account = account, keys = keys, transaction_id = transaction_id, account_id = account_id)
    print(resp)
    return HttpResponseRedirect('/')

coinbase_client = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, 'all', redirect_uri='https://198.199.112.146/auth2', auth_uri='https://www.coinbase.com/oauth/authorize', token_uri='https://www.coinbase.com/oauth/token')

def index(request):
  context = RequestContext(request)
  return render_to_response('treasure/index.jade', {}, context)

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
