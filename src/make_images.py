import os
from PIL import Image

def resize_image(image):
    width, height = image.size
    if width > height : new = image.resize((500, round( 500 * (height / width) )))
    else : new = image.resize( ( round( 500 * (width / height) ) , 500))
    return new

def cut_image_on_standard(image):
    width, height = image.size
    new = resize_image( image.crop( ( 20, 20, width - 20, height - 20 ) ) )
    return new

def rotate_and_save_image(base_image, base_path, numbering):
    rotate_deg = [3, -3, 5, -5]
    base_image.save(base_path + str(numbering) + '_rot0.jpg')
    for i in range(0,4):
        rotated_image = base_image.rotate(rotate_deg[i])
        rotated_image = cut_image_on_standard( rotated_image)
        new_file_path = "{base}{number}_rot{degree}.jpg".format(
            base = base_path, number = i + 1, degree=rotate_deg[i])
        rotated_image.save(new_file_path)

def move_and_copy_image(new_dir_path, origin_dir_path):
    print('extending: {0} from {1}.'.format(new_dir_path, origin_dir_path))
    image_files_list = os.listdir(origin_dir_path)
    coord_deg_tups = [(0, 0, -20, -20), (20, 0, 0, -20),
                      (0, 20, -20, 0), (20, 20, 0, 0)]
    brights_value = [-70, -50,-30,0,30,50, 70]
    for file in image_files_list:
        image_path_base = new_dir_path + '/' + file.split('.')[0] + '_'
        origin_image = Image.open(origin_dir_path + '/' + file)
        resized_image = resize_image(origin_image)
        width, height = resized_image.size
        numbering = 1
        for coord_deg_tup in coord_deg_tups:
            area = (coord_deg_tup[0], coord_deg_tup[1],
                    width + coord_deg_tup[2], height + coord_deg_tup[3])
            new_image = resize_image(resized_image.crop(area))
            for bright_value in brights_value :
                brt_new_image = Image.eval(new_image, lambda x:x+bright_value)
                brt_new_image = brt_new_image.convert("RGB")
                rotate_and_save_image(brt_new_image, image_path_base + str(bright_value), numbering)
                numbering += 1