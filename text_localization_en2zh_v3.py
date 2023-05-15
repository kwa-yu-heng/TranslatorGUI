#from pytesseract import Output
#import pytesseract
import cv2
import translators.server as ts
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import argostranslate.package
import argostranslate.translate
import easyocr

reader = easyocr.Reader(['ch_sim','en'])



''' ONLY NEEDED WHEN PACKAGES NOT INSTALLED YET
argostranslate.package.update_package_index()

# Download and install Argos Translate package
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == 'en' and x.to_code == 'zh', available_packages
    )
)

argostranslate.package.install_from_path(package_to_install.download())
'''

 

def en2zh(filename,trans_filename):
  #pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files/Tesseract-OCR/tesseract.exe'  # your path may be different
  

  #conf_level=70

  # image path
  result = reader.readtext(filename)

  #filename = 'english_sentences.jpg'
  image = cv2.imread(filename)


  # 定义宋体路径
  fontpath = 'simsun.ttc'

  # 创建字体对象，并且指定字体大小
  font = ImageFont.truetype(fontpath, 20)

  # 把array格式转换成PIL的image格式
  img_pil = Image.fromarray(image)

  # 创建一个可用来对其进行draw的对象
  draw = ImageDraw.Draw(img_pil)

  # iterate on all results
  for res in result:  
      try:
          text=res[1]
          print(text)
          text = ts.alibaba(text, from_language='zh', to_language='en')  #seems to translate better
          print(text)
          top_left = tuple(res[0][0]) # top left coordinates as tuple
          bottom_right = tuple(res[0][2]) # bottom right coordinates as tuple
      
          #modifying for writing chinese characters
          
          bbox=draw.textbbox((top_left[0], top_left[1]-17), text=text,font=font)
          draw.rectangle(bbox,fill='green')
          draw.text((top_left[0], top_left[1]-17),text=text,font=font,fill='black')
          # draw rectangle on image
          #cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2) 
          draw.rectangle([top_left, bottom_right],outline='green',width=3)
          # write recognized text on image (top_left) minus 10 pixel on y
          #cv2.putText(image, res[1], (top_left[0], top_left[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



      except:
          pass


  image = np.array(img_pil)
  cv2.imwrite(trans_filename,image) #save written image
  #cv2.startWindowThread()
  #cv2.namedWindow("preview")   
  #cv2.imshow('preview',image)
  #cv2.waitKey(0)



####################test############################
#zh2en('chinese_test.jpg','chinese_test_trans.jpg')
#en2zh('english_sentences.jpg','english_sentences_trans.jpg')
#en2zh('final.jpg','easy_ocr.jpg')