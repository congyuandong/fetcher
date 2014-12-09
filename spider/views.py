#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import EIHacker
import simplejson as json

# Create your views here.

def index(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('spider/index.html',context_dict,context)

#WEB端获取数据
def GetWebData(request):
	context_dict = {}
	if request.method == 'GET':
		title = request.GET.get('title','')
		if title:
			body = EIHacker.webHTML(title)
			if body == -1:
				context_dict['status'] = 0
			else:
				context_dict['status'] = 1
				context_dict['body'] = body

	return HttpResponse(json.dumps(context_dict),content_type="application/json")

def GetAPPData(request):
	context_dict = {}
	if request.method == 'GET':
		title = request.GET.get('title','')
		if title:
			body = EIHacker.appHTML(title)
			if body == -1:
				context_dict['status'] = 0
			else:
				context_dict['status'] = 1
				context_dict['result'] = body

	return HttpResponse(json.dumps(context_dict),content_type="application/json")