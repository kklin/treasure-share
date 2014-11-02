from django.shortcuts import render, render_to_response
from django.template import RequestContext
from treasure.models import Treasure, Dribble

def index(request):
  context = RequestContext(request)
  return render_to_response('treasure/index.jade', {}, context)