from django.http import HttpResponse
from django.shortcuts import render_to_response
import os
import shutil
from django.http import HttpResponseRedirect

def labeling(request):
	print("request",request.GET)
	if 'label' in request.GET:
		old_path = 'static/' + request.GET['name']
		new_path = 'static/labeling_package/' + request.GET['label']
		print('\n')
		print(old_path)
		print(new_path)
		print('\n')
		shutil.move(old_path,new_path)    
		return HttpResponseRedirect(".")


	filenames = os.listdir("static/labeling_package/images")
	# 取得所有圖片的檔名
	images = filter(is_imag, filenames)

	for i in images:
		print("image:",i)
		get_imageName="labeling_package/images/"+str(i)
		break


	return render_to_response('index.html',locals())

#判斷檔案是否為圖片
def is_imag(filename):
    return filename[-4:] in ['.png', '.jpg']

# Create your views here.
