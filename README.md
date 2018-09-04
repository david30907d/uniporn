# Uniporn

1. 主架構:
	1. 把人臉依照臉型、角度、髮型等等編碼成向量
		1. [用inceptionV3當圖片vector](https://github.com/david30907d/artificio/blob/master/similar_images_TL/similar_images_TL.py)
		2. [找到人臉的角度](https://github.com/mpatacchiola/deepgaze)
		3. MTCNN
		4. FaceNet
	2. 找到近似的臉 
		1. [artificio](https://github.com/david30907d/artificio/blob/master/similar_images_TL/similar_images_TL.py)
	3. FaceSwap:
		1. [FaceSwap](https://github.com/wuhuikai/FaceSwap)
		2. [FaceSwap Gan](https://github.com/shaoanlu/faceswap-GAN)
		3. [Unsupervised Im2Im](https://github.com/zsdonghao/Unsup-Im2Im)
		4. [原版deepfake faceswap](https://github.com/deepfakes/faceswap)
		5. [Reference](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.limitlessiq.com%2Fnews%2Fpost%2Fview%2Fid%2F3874%2F&h=AT3PyIoCqSShQv4V4Y3FSLli4_ma1fY3JR1jEScyPpqNdjeTc_OU8_LeZJ2XBqOGnd_ffh24dN-VLMjRS8Hun8i997TIS-TPM0IKyB5depoqoDw3AtBBIYBK4Ar-dV8VLReurXJtRlLKtuL6VAYxxywOo2c)
2. FaceSwap架構：
	1. 換臉部分可替換模組：
		1. dlib
		2. [face-recognition](https://github.com/ageitgey/face_recognition)
		3. [MTCNN or FaceNet](https://hk.saowen.com/a/9b30c255320206df2fe9c91f021473e8aa0ceaa09e4e2e60aad09b0afe3429ab)
			1. [MTCNN](https://github.com/ipazc/mtcnn)
			2. [MTCNN2](https://github.com/pangyupo/mxnet_mtcnn_face_detection)
			3. [FaceNet](https://github.com/davidsandberg/facenet)