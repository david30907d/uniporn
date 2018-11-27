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
		4. 疑似可以偵測戴口罩的人臉:
			1. [mtcnn-anonymization](https://github.com/CyberAILab/MTCNN-tf-anonymization)

## Business Model

1. [主體是戀愛養成遊戲](https://www.youtube.com/watch?v=lr4iC910gWE)
	1. 可以不用這麼多影片，用圖片跟表情就好
	2. 然後用每週六日更新劇情的方式，讓大家一直上線
2. 獲利：
	1. 無，只是會丟一些女生的照片給user label，讓他選這是裙子還是牛仔褲之類的，答完就可以繼續玩
3. 內容：
	1. 劇情內容：請model來，然後用deepfake換臉，需要的話再請人工修圖，務必高畫質
	2. 非劇情的劇照：像神魔一樣讓user每天登入抽女生卡，這些東西用比較低畫質的deepfake或是faceswap濫竽充數就好
		1. 這類劇照可以選擇裙子、牛仔褲、浴衣等等不同款式，訓練資料其實就是user標好的

## 小工具

* 把很多層次的資料夾裡的圖片集中到同一個資料夾的SCRIPT: `squash.py`
