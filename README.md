## 目的

1. 透過AI把幫色情 圖片穿衣服
2. 上傳任何一個人，有穿衣服的照片,要透過GAN去『想像』該人物裸體的照片
3. 同樣的技術，只 要有足夠多的pair data，例如魔戒精靈王子和奧蘭多布魯平常的照片當作一筆pair data，GAN就會學到輸入我日常生活照，輸出我在魔戒世界應有的樣子

## Commands

1. Install: `pip3 install -r requirements.txt`
2. Crawler:
	1. Crawl pics as much as you can:
		* nonporn pictures:
			* `python3 manage.py huaban`
			* `python3 manage.py keaitupian`
		* porn pictures:
			* `python3 manage.py jkforum`
		* hybrid pictures:
			* `python3 manage.py timliao`
	2. Compress folders into a single folder with name porn or nonporn:
		* `python3 manage.py autotar <types of pics:nonporn, porn, hybrid>`
3. CNN:
	* train: 
		1. Use the two folders, porn and nonporn created by `python3 manage.py autotar`, to start training
		2. `python3 manage.py cnn --train true`
	* use a picture to do prediction: `python3 manage.py cnn --img <filepath of that pic>`
	* use a url of pic to do prediction: `python3 manage.py cnn --url <url>`
	* generate GAN training_data: `python3 manage.py genData --p2n < default = 1 => GAN[output:non, input:porn]>`
4. GAN:
	* `coming soon`
	* <https://github.com/eriklindernoren/Keras-GAN>

## Training Data

1. [清純女孩幾乎沒露的](http://huaban.com/explore/qingchunkeaimeinv/) [清純2](http://www.keaitupian.com/girl/) [清純3](https://www.pakutaso.com/person/woman/index_68.html)
2. [有露的 提姆](http://www.timliao.com/bbs/forumdisplay.php?fid=18) [ptt表特](https://www.ptt.cc/bbs/Beauty/index.html)
1. [珍尼佛勞倫司等女星裸照](https://www.celebjihad.com/category/jennifer-lawrence/) [西洋女星](https://dark.getez.info/158751) [大補貼](http://tw.dufeed.com/article/content_136492.html?is_adult=1) [載點2](https://thefappening.wiki/) [真正的載點](https://kutlime.wordpress.com/fappening-celebrity-photo-foto-download/)
2. [正妹圖 不能是女優](https://www.jkforum.net/forum.php?gid=573)
3. 不能是女優的理由是因為背景都有屌、男生等圖片雜訊，一開始先用最乾淨的圖片，只有一位女生（兩位女生也不行，有男優有屌都不要）
4. [A片網 儘量不要有奇怪的字樣再照片上，我怕會變雜訊，要單人女優 不要有屌，不要有兩位以上人物入境](http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=juy00377/?i3_ref=list&i3_ord=3)

## 流程

1. 首先要訓練一個是否有露的分類器，把Traiining Data做一次清洗，分出有穿衣服的正常照片（input data），和露奶露屁股露點的照片（之後複雜一點也許可以把露奶和露點分成兩類label data）
	* [tensorflow版本](https://github.com/bakwc/PornDetector)
	* 色情分類器:[yahoo的](https://github.com/yahoo/open_nsfw)
	* 更細的色情分類器，真的能偵測6種性行為:[miles_deeps](https://github.com/ryanjay0/miles-deep)
		* blowjob_handjob
		* cunnilingus
		* other
		* sex_back
		* sex_front
		* titfuck
	* 之後想要抓到男上女下的圖片、口交的圖片等等比較難判斷的，可能試試看[img2txt](https://github.com/tensorflow/models/tree/master/research/im2txt)能不能產出正確的句子，如果可以我們就只有偵測關鍵字就好。
2. 再來就是訓練GAN，把有穿衣服的照片餵進去，要output出漏奶漏點的照片，GAN會嘗試辨別這是真的還是合成的照片，直到分不太出來為止。
3. GAN產出來的圖片可能會有點模糊，用[srez](https://github.com/david-gpu/srez)去得到超清晰的圖片。

## 可能需要文字探勘的部份

1. 因為整體的訓練資料會很少，所以可能會需要用爬蟲到處亂爬，那這篇文章出現一張女生的圖，到底是再講林志玲還是小S（假設文章兩位女生的名子都出現），會需要一個演算法能精準自動上label給圖片，累積有穿衣服的input Data
2. 也可以做三圍偵測器，AV女優基本都會給三維，把他當成regression的方法就訓練就行，因為三圍是連續值

## 人工標記色情圖

1. 執行 `python3 manage.py runserver`
2. 把未標記照片放入 `static/labeling_package/images` 底下
3. 在網址列輸入 `127.0.0.1:8000/labeling` 就可以開始標記了
4. 標記好的圖片會移動至以下資料夾
	* `static/labeling_package/Aporn` (色情圖片)
	* `static/labeling_package/non-porn` (非色情圖片)
	* `static/labeling_package/trash`  (只是個不能拿去訓練的垃圾)
   
<img src="https://i.imgur.com/VSblYwi.jpg" />

色情類網站:
1. porn:
	* 肉色衣物
	* ![肉色也PORN](gold_standard/PORN_standard/PORN/肉色也PORN.jpg)
	* 正面照但姿勢不影響
	* ![坐著也可以PORN](gold_standard/PORN_standard/PORN/坐著也可以PORN.jpg)
2. trash:
	* 倒著
	* ![倒著](gold_standard/PORN_standard/TRASH/倒著.jpg)
	* 包覆過多，臉部被遮住且雜物太多
	* ![包覆_遮住臉](gold_standard/PORN_standard/TRASH/包覆_遮住臉.jpg)

非色情類網站:
1. nonporn:
	* 正常照片
	* ![圓領條紋四面彈上衣](gold_standard/NONPORN_standard/NONPORN/圓領條紋四面彈上衣.jpg)
	* ![休閒甜感兔子彩色條紋上衣](gold_standard/NONPORN_standard/NONPORN/休閒甜感兔子彩色條紋上衣.jpg)
2. trash:
	* 側面
	* ![直條紋棉質長襯衫](gold_standard/NONPORN_standard/TRASH/直條紋棉質長襯衫.jpg)
	* 沒有五官
	* ![好感刺繡側開衩襯衫](gold_standard/NONPORN_standard/TRASH/好感刺繡側開衩襯衫.jpg)
