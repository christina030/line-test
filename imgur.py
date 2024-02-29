# -*- coding: utf-8 -*-

import pyimgur

"""
[圖片URL](https://medium.com/@fidhaley/line-bot-python-%E5%BB%BA%E7%AB%8B%E6%88%91%E7%9A%84%E7%AC%AC%E4%B8%80%E5%80%8Bapp-3-linebot%E6%96%87%E5%AD%97%E6%8C%87%E4%BB%A4-%E5%AD%98%E5%8F%96%E5%9C%96%E7%89%87-%E6%9B%B4%E6%8F%9B%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%A4%A7%E9%A0%AD%E8%B2%BC%E6%95%88%E6%9E%9C-1cbb61647d60)
"""

client_id = 'bde19e3500c4e17'
def glucose_graph(client_id, imgpath):
    im = pyimgur.Imgur(client_id)
    upload_image = im.upload_image(imgpath, title='Uploaded with PyImgur')
    return upload_image.link

"""
[自動回覆圖片](https://steam.oxxostudio.tw/category/python/example/line-reply-message.html)
[編輯圖片](https://blog.gtwang.org/programming/opencv-drawing-functions-tutorial/)
"""
