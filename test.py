import cv2
import os

# 1. 获取需要批量添加水印的文件夹的名字
folder_name = input("请输入要批量添加水印的文件夹的名字：")


# 2. 获取文件中所有文件的名字
file_names = os.listdir(folder_name)

# 3. 使用cv2进行处理
for name in file_names:
    img = cv2.imread(folder_name + "/" + name)
    font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型: 正常大小无衬线字体
    # 参数分别是图片, 输入文本数据，放置文本的位置坐标，字体类型，字体大小，颜色为白色，厚度为2
    cv2.putText(img, '内部文件,请勿外传'.encode('utf-8'), (500, 500), font, 50, (23, 76, 45), 3)
    # 保存添加文字后的图片
    cv2.imwrite(folder_name + "/new_" + name, img)