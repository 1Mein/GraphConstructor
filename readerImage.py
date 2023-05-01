import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter
import os
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# plt.imshow(pict)
# plt.show()
try:
    for i in range(80, 228):
        path = '1\imgs\Снимок экрана (' + str(i) + ').png'

        #proverka na existance
        if os.path.exists(r'1\imgs\Снимок экрана (' + str(i) + ').png'): 
            pict = Image.open(path)
            pict = pict.crop((260, 50, 1270, 1020))

            #converting to cherno belyi
            enhancer = ImageEnhance.Contrast(pict)
            pict = enhancer.enhance(2)
            fn = lambda x : 255 if x > 200 else 0
            pict = pict.convert('L').point(fn, mode='1')

            #invertirovanie
            pict = Image.eval(pict, lambda x: 255 - x)

            #reading the image
            text = pytesseract.image_to_string(pict, lang="eng", config='--psm 12')

            #raspredelenie na massiv
            words = text.split()
            #to lowercase words
            words = [word.lower() for word in words]

            #expecting wpm
            try:
                wpm = str(words[words.index('wpm')-1])[:2]
            except Exception as e:
                print('can\'t find a wpm')

            if wpm == 'si': wpm = '51'

            #output
            print(str(i) + ". " + wpm + " wpm" +
                  ", Created: %s" % time.ctime(os.path.getctime(path)))

    # pict = Image.open('1\imgs\Снимок экрана (111).png')
    # pict = pict.crop((260, 50, 1270, 1020))

    # enhancer = ImageEnhance.Contrast(pict)
    # pict = enhancer.enhance(2)
    # def fn(x): return 255 if x > 200 else 0
    # res = pict.convert('L').point(fn, mode='1')
    # res = Image.eval(res, lambda x: 255 - x)
    # plt.imshow(res)
    # plt.show()

    # text = pytesseract.image_to_string(res, lang="eng", config='--psm 12')
    # words = text.split()
    # print(text)
    # print(str(words[words.index('wpm')-1]) + " wpm")
except Exception as e:
    print(e)
