import time
from tkinter import filedialog

import os
from tkinter import *
from PIL import Image


#### Author: ChenZihao
#### Date  : 2021/3/28
#### Usage : Create a folder named 'image' under the same path of generated exe file manually, click convert button and finally get 'output.pdf' under the same path.
#### Error Type:
####### 1. folder 'image' is not exist
####### 2. no pictures in folder(image)
####### 3. invalid image exists
####### 4. target file(output.pdf) is occupying by user

str_msg = None
message = None

def getTimeStr():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def img2pdf(path, pdf_name):
    # 将所有图片转换为jpg格式，统一处理
    try:
        names = os.listdir(path)    # path文件夹下所有文件的list
    except FileNotFoundError:
        message.configure(fg='red')
        str_msg.set('生成失败！\nimage文件夹不存在' + getTimeStr())
        return

    pic_need_to_convert = {}    # 待转换为pdf的图片dic，key：图片名 value：Image对象
    sorted_keys = None          # pic_need_to_convert字典中key的有序list

    valid_pic_suffix = ['jpg', 'png', 'gif', 'jpeg', 'bmp', 'svg']

    if len(names) == 0:
        message.configure(fg='red')
        str_msg.set('生成失败！\nimage文件夹中没有图片\n' + getTimeStr())
        print(str_msg.get())
        return

    for name in names:
        # 判断后缀是否非法
        name_list = name.split(".")
        if name_list[-1] not in valid_pic_suffix:
            message.configure(fg='red')
            str_msg.set('生成失败！\nimage文件夹中有非法的图片格式存在' + getTimeStr())
            print(str_msg.get())
            return

        img = Image.open(path + '/' + name) # 查找path文件

        if name_list[-1] != "jpg": # 当前这张照片如果不是jpg格式的则生成一张jpg格式的
            name_list[-1] = "jpg"
            name_jpg = str.join(".", name_list)
            if img.mode == "RGBA":
                img = img.convert('RGB')
                #r, g, b, a = img.split()
                #img = Image.merge("RGB", (r, g, b))
            else:
                r, g, b = img.split()
                img = Image.merge("RGB", (r, g, b))
            pic_need_to_convert[name_jpg] = img
        else:
            pic_need_to_convert[name] = img


    sorted_keys = sorted(pic_need_to_convert.keys())
    res = pic_need_to_convert[sorted_keys[0]] # 读取第一张图片
    sorted_keys.pop(0)
    img_list = []
    for cur_key in sorted_keys:
        img_list.append(pic_need_to_convert[cur_key])

    try:
        res.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=img_list)
    except PermissionError:
        message.configure(fg='red')
        str_msg.set('生成失败！\n请检查是否占用output.pdf\n' + getTimeStr())
        return
    message.configure(fg = 'green')
    str_msg.set('生成成功！\n\n' + getTimeStr())
    print(str_msg.get())


# 设置按钮事件
def func():
    output_pdf_name = 'output.pdf'
    img_path = 'image'
    if ".pdf" in output_pdf_name:
        img2pdf(img_path, pdf_name= output_pdf_name)
    else:
        img2pdf(img_path, pdf_name="{}.pdf".format(output_pdf_name))


if __name__ == '__main__':
    # output_pdf_name = 'output.pdf'
    # img_path = 'image'
    # if ".pdf" in output_pdf_name:
    #     rea(img_path, pdf_name= output_pdf_name)
    # else:
    #     rea(img_path, pdf_name="{}.pdf".format(output_pdf_name))


    win = Tk()  # 创建一个主窗口
    win.resizable(0, 0) # 设置窗口大小不可变
    win.title("CHENZIHAO") # 设置标题
    win.geometry("250x90+700+300") # 设置窗口大小和位置 长x宽+左边缘距离+上边缘距离


    button = Button(win,text="转换image文件夹下的所有图片为PDF",
                        command=func,
                        width = 30,
                        height = 2,)
    button.pack() # button显示


    str_msg = StringVar()
    message = Label(win, textvariable=str_msg, fg='red', font=('宋体', 10))  # 用于显示生成结果提示信息
    message.place(x=30, y=120, anchor='nw')
    message.pack()

    win.mainloop()