from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

import os

# from cnn import *
# pcr = NNPCR()
# pcr.loadModel('nnmodel.bin')

# Create your views here.
def web_home(request):
	a=1
	filenames = os.listdir(".") # "."可以找出目前位置
	print(filenames) # 會回傳一個list
	return render_to_response('web_home.html',locals())

def demo_model(request):
	# return render_to_response('test.html',locals())	
	if request.method == 'POST' and request.FILES['upload_file']:
		myfile = request.FILES['upload_file'] # 取得上傳的檔案
		fs = FileSystemStorage()
		path = 'web/static/user_upload/' + myfile.name
		filename = fs.save(path, myfile) # 儲存檔案
		uploaded_file_url = fs.url(filename) # 取得存檔路徑
		print('uploaded_file_url:',uploaded_file_url)
		img_static_path = get_static_path(uploaded_file_url)
		print(img_static_path)
		print('/*******************/')
		# return render_to_response('demo_model.html',locals())	
		# return render_to_response('/home/demo_model#upload_porn',locals())	
		return render_to_response('demo_model.html',locals())
	return render_to_response('demo_model.html',locals())	

def cnn_api(request):
	img = request.GET['img']
	result = pcr.predict([img])[0]
	if result:
		return JsonResponse({'result':'porn'}, safe=False)
	else:
		return JsonResponse({'result':'non-porn'}, safe=False)



def get_static_path(path):
	path=path.split('static')[1]
	return path[1:]


