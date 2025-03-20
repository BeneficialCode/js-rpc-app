import cv2
import numpy as np
import base64
from matplotlib import pyplot as plt

def show_image_with_matplotlib(title, image):
    """使用 Matplotlib 显示图像"""
    # 将 BGR 转换为 RGB（Matplotlib 使用 RGB 格式）
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis("off")  # 隐藏坐标轴
    plt.show()

def crop_slider(slider_image_path):
    """裁剪掉滑块图片的透明背景，只留下滑块本身"""
    # 读取滑块图片（支持 PNG 格式，包含透明通道）
    slider_image = cv2.imread(slider_image_path, cv2.IMREAD_UNCHANGED)

    # 检查是否包含透明通道
    if slider_image.shape[2] == 4:  # 包含透明通道
        alpha_channel = slider_image[:, :, 3]  # 提取透明通道
        # 找到包含滑块的最小矩形区域
        contours, _ = cv2.findContours(alpha_channel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bounding_box = cv2.boundingRect(contours[0])

        # 裁剪滑块图片
        cropped_slider = slider_image[bounding_box[1]:bounding_box[1] + bounding_box[3],
                                      bounding_box[0]:bounding_box[0] + bounding_box[2]]
    else:
        # 如果没有透明通道，直接返回原图
        cropped_slider = slider_image
        bounding_box = (0, 0, slider_image.shape[1], slider_image.shape[0])

    return cropped_slider, bounding_box


def compute_slide_offset(back_img_path, sliding_img_path):
    """计算滑块在背景图中的偏移量并可视化"""
    # 读取背景图和滑块图（支持 PNG 格式）
    back_img = cv2.imread(back_img_path, cv2.IMREAD_COLOR)
    sliding_img, bounding_box = crop_slider(sliding_img_path)

    # 识别图片边缘
    back_edge = cv2.Canny(back_img, 100, 200)
    sliding_edge = cv2.Canny(sliding_img, 100, 200)

    # 缺口匹配
    res = cv2.matchTemplate(back_edge, sliding_edge, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 计算滑块的偏移量
    x = max_loc[0] - bounding_box[0]
    y = max_loc[1] - bounding_box[1]

    # 可视化：在背景图上绘制匹配位置
    h, w = sliding_img.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(back_img, top_left, bottom_right, (0, 255, 0), 2)  # 绿色矩形框

    # 获取矩形框四个顶点
    top_left_x, top_left_y = top_left
    bottom_right_x, bottom_right_y = bottom_right
    top_right = (bottom_right_x, top_left_y)
    bottom_left = (top_left_x, bottom_right_y)

    # 绘制坐标系
    center_x, center_y = top_left[0] + w // 2, top_left[1] + h // 2
    cv2.line(back_img, (center_x, 0), (center_x, back_img.shape[0]), (255, 0, 0), 1)  # 竖直线
    cv2.line(back_img, (0, center_y), (back_img.shape[1], center_y), (255, 0, 0), 1)  # 水平线

    # 标记偏移量位置
    cv2.circle(back_img, (center_x, center_y), 5, (0, 0, 255), -1)  # 红色圆点

    # 显示背景图上的匹配结果
    show_image_with_matplotlib("Matched Result with Coordinates", back_img)

    return x, y

xy_array = []
real_array = []
# 测试代码
p1_path = 'P1.png'  # 背景图路径
p2_path = 'P2.png'  # 滑块图路径
real_x = 144
real_y = 27
x, y = compute_slide_offset(p1_path, p2_path)
xy_array.append((x, y))
real_array.append((real_x, real_y))


real_x = 183
real_y = 72
p1_path = 'P3.png'  # 背景图路径
p2_path = 'P4.png'  # 滑块图路径
x, y = compute_slide_offset(p1_path, p2_path)
xy_array.append((x, y))
real_array.append((real_x, real_y))

real_x = 226
real_y = 51
p1_path = 'P5.png'  # 背景图路径
p2_path = 'P6.png'  # 滑块图路径
x, y = compute_slide_offset(p1_path, p2_path)
xy_array.append((x, y))
real_array.append((real_x, real_y))

real_x = 132
real_y = 65
p1_path = 'P8.png'  # 背景图路径
p2_path = 'P9.png'  # 滑块图路径
x, y = compute_slide_offset(p1_path, p2_path)
xy_array.append((x, y))
real_array.append((real_x, real_y))

real_x = 175
real_y = 63
p1_path = 'P10.png'  # 背景图路径
p2_path = 'P11.png'  # 滑块图路径
x, y = compute_slide_offset(p1_path, p2_path)
xy_array.append((x, y))
real_array.append((real_x, real_y))

real_x = 158
real_y = 37
p1_path = 'P13.png'  # 背景图路径
p2_path = 'P14.png'  # 滑块图路径
x, y = compute_slide_offset(p1_path, p2_path)
xy_array.append((x, y))
real_array.append((real_x, real_y))


for i in range(len(xy_array)):
    x = int(xy_array[i][0]/400*315)
    y = int(xy_array[i][1]/200*150)
    print(f"真实值: {real_array[i]},识别值:({xy_array[i][0]},{xy_array[i][1]}) 调整值：({x}, {y})")

