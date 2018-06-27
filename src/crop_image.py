from PIL import Image

def reduce_and_save_image(origin_image, crop_coords, saved_base_path):
    print(origin_image)
    image_obj = Image.open(origin_image)
    cropped_image = image_obj.crop(crop_coords)
    cropped_image.save(saved_base_path + 'Origin.jpg')
    save_new_images(image_obj, crop_coords, saved_base_path)

def is_in_bound(size, coords):
    if coords[0] < 0 or coords[1] < 0 or coords[2] > size[0] or coords[3] > size[1] :
        return False
    else :
        return True

def save_new_images(image, coords, saved_location) :
    for i in range(5,7):
        ext_width = round( (coords[2] - coords[0]) / i)
        ext_height = round( (coords[3] - coords[1]) / i)
        size = image.size
        coord_info_tups = [(-ext_width, -ext_height, 0, 0, 'ld'), (0,-ext_height,ext_width,0, 'rd'),
                          (-ext_width,0,0,ext_height, 'lu'), (0,0,ext_width,ext_height,'ru'),
                          (-ext_width, -ext_height, ext_width,ext_height, 'ct')]
        for coord_info in coord_info_tups:
            new_coords = (coords[0] + coord_info[0], coords[1] + coord_info[1],
                          coords[2] + coord_info[2], coords[3] + coord_info[3])
            if is_in_bound( size, new_coords):
                new_image = image.crop(new_coords)
                new_image.save(saved_location + '_' + str(i) + coord_info[4] + '.jpg')