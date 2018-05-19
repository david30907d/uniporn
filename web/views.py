from django.shortcuts import render
from django.http import JsonResponse
from cnn import *
pcr = NNPCR()
pcr.loadModel('nnmodel.bin')

# Create your views here.
def cnn_api(request):
	img = request.GET['img']
	result = pcr.predict([img])[0]
	if result:
		return JsonResponse({'result':'porn'}, safe=False)
	else:
		return JsonResponse({'result':'non-porn'}, safe=False)