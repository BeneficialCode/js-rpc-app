import cv2
from PIL import Image

# 天眼查底图还原
def image_recover(image_path,save_path):
    img  = Image.open(image_path)
    location_list = [{"x": -157, "y": -58}, {"x": -145, "y": -58}, {"x": -265, "y": -58}, {"x": -277, "y": -58},
                     {"x": -181, "y": -58}, {"x": -169, "y": -58}, {"x": -241, "y": -58}, {"x": -253, "y": -58},
                     {"x": -109, "y": -58}, {"x": -97, "y": -58}, {"x": -289, "y": -58}, {"x": -301, "y": -58},
                     {"x": -85, "y": -58}, {"x": -73, "y": -58}, {"x": -25, "y": -58}, {"x": -37, "y": -58},
                     {"x": -13, "y": -58}, {"x": -1, "y": -58}, {"x": -121, "y": -58}, {"x": -133, "y": -58},
                     {"x": -61, "y": -58}, {"x": -49, "y": -58}, {"x": -217, "y": -58}, {"x": -229, "y": -58},
                     {"x": -205, "y": -58}, {"x": -193, "y": -58}, {"x": -145, "y": 0}, {"x": -157, "y": 0},
                     {"x": -277, "y": 0}, {"x": -265, "y": 0}, {"x": -169, "y": 0}, {"x": -181, "y": 0},
                     {"x": -253, "y": 0}, {"x": -241, "y": 0}, {"x": -97, "y": 0}, {"x": -109, "y": 0},
                     {"x": -301, "y": 0}, {"x": -289, "y": 0}, {"x": -73, "y": 0}, {"x": -85, "y": 0},
                     {"x": -37, "y": 0}, {"x": -25, "y": 0}, {"x": -1, "y": 0}, {"x": -13, "y": 0},
                     {"x": -133, "y": 0}, {"x": -121, "y": 0}, {"x": -49, "y": 0}, {"x": -61, "y": 0},
                     {"x": -229, "y": 0}, {"x": -217, "y": 0}, {"x": -193, "y": 0}, {"x": -205, "y": 0}]
    im_list_upper = []
    im_list_down = []
    for location in location_list:
        if location['y'] == -58:
            im_list_upper.append(
                img.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
        if location['y'] == 0:
            im_list_down.append(img.crop((abs(location['x']), 0, abs(location['x']) + 10, 0 + 58)))
    new_img = Image.new('RGB', (260, 116))
    x_offset = 0
    for im in im_list_upper:
        new_img.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    x_offset = 0
    for im in im_list_down:
        new_img.paste(im, (x_offset, 58))
        x_offset += im.size[0]
    new_img.save(save_path)

image_path = '895656306.jpg'
save_path = 'recover.jpg'
image_recover(image_path, save_path)

background_path = '747db4a16.jpg'
save_path = 'background.jpg'
image_recover(background_path, save_path)