from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from treasure.models import Treasure, Dribble
from django.http import HttpResponse

from oauth2client.client import OAuth2WebServerFlow
import httplib2
from secrets import CALLBACK_URL, CLIENT_ID, CLIENT_SECRET

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
    return redirect('/display_oauth')

def display_oauth(request):
    response = HttpResponse(request.session['oauth_json'], content_type = 'text/plain')
    return response
