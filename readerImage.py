import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter
import os
import time
import matplotlib.pyplot as plt
import math
import sys
sys.stdout.reconfigure(encoding='utf-8')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# plt.imshow(pict)
# plt.show()

wpms = []
times = []
titles = []
names = []
counterForTitles = 0

# try:
#     fileForOut = open(r'1\outputData.txt', 'w')
# except Exception as e:
#     print(e)

try:
    for i in range(80, 228):  # 228
        print('o'*math.floor(((i-80)/14.8)) + '\t[' + str(math.floor(((i-80)/14.8))) + ' / 10]')
        path = r'1\imgs\Снимок экрана (' + str(i) + ').png'
        # proverka na existance
        if os.path.exists(path):
            titles.append('A')
            names.append(str(i))
            pict = Image.open(path)

            # crop image is unnecessary, its probably work only for my screen. It influents only to the speed I think.
            pict = pict.crop((260, 50, 1270, 1020))

            # converting to cherno belyi
            enhancer = ImageEnhance.Contrast(pict)
            pict = enhancer.enhance(2)
            def fn(x): return 255 if x > 200 else 0
            pict = pict.convert('L').point(fn, mode='1')
            # invertirovanie
            pict = Image.eval(pict, lambda x: 255 - x)


            # reading the image
            text = pytesseract.image_to_string(
                pict, lang="eng", config='--psm 12')
            text = text.replace('|' , 'I')
            text = text.replace('si' , '51')
            text = text.replace('Si' , '51')
            # print(text)

            # wordsSymbol = text.split(' ')
            # print(wordsSymbol)
            
            # raspredelenie na massiv
            words = text.split()
            # to lowercase words
            # print(words)
            if 'quote' in words:
                for j in range (words.index('quote'),len(words) - words[::-1].index('wpm') - 2):
                    titles[counterForTitles] +=' ' + words[j]
            else:
                titles[counterForTitles] = "Can\'t scan a text"
            counterForTitles+=1

            words = [word.lower() for word in words]
            # expecting wpm
            try:
                wpm = str(words[words.index('wpm')-1])[:2]
            except Exception as e:
                print('can\'t find a wpm')

            wpms.append(wpm)

            created = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.path.getctime(path))))
            times.append(created)
            # output
            # print(str(i) + ". " + wpm + " wpm" +
            #       ", Created: %s" % time.ctime(os.path.getctime(path)))


    #its realtive calculation for graphics
    relTimes = []
    fday = int(times[0][8:10])
    fmonth = int(times[0][5:7])
    for i in range(0, len(times)):
        minutes = int(times[i][14:16])/60
        hours = int(times[i][11:13])+minutes
        months = int(times[i][5:7])-fmonth
        relTimes.append((int(times[i][8:10])+(months*30))-fday+(hours/24))

    print(wpms)
    print(relTimes)
    print(times)
    print(titles)
    print(names)
    with open(r'1\outputData.txt', 'w', encoding='utf-8') as f:
        for i in range(len(wpms)):
            f.write(str(i+1) + '. ' + wpms[i] + ' wpm | ' + times[i] + ' | ' + names[i] + '\n' + titles[i] + '\n\n')


    plt.rcParams['figure.figsize'] = [20,3]
    plt.plot(times,wpms,label = "times")
    plt.xticks(rotation = 45)
    plt.subplots_adjust(bottom=0.33)
    plt.show()


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
