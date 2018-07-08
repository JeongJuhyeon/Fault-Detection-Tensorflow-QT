from subprocess import call
import os
from src import make_images, config

def copy_images(device_path_to_copy):
    print('##-COPY IMAGES FOR TRAINING')
    dirs_list = os.listdir(device_path_to_copy)

    new_base_path = os.path.join(device_path_to_copy, 't_images')
    if not os.path.isdir(new_base_path): os.mkdir(new_base_path)

    if 'model' in dirs_list : dirs_list.remove('model')
    if 't_images' in dirs_list : dirs_list.remove('t_images')
    if 'locationInfo.txt' in dirs_list: dirs_list.remove('locationInfo.txt')
    if 'Origin.jpg' in dirs_list: dirs_list.remove('Origin.jpg')

    for side_dir in dirs_list:
        side_path = os.path.join(device_path_to_copy, side_dir)
        classes = os.listdir(side_path)
        print("Copy image classes: ", classes, "in", side_path)

        for element in classes:
            dir_path = os.path.join(side_path , element)
            element_path = os.path.join(new_base_path, element)
            config.makeDir(element_path)
            make_images.move_and_copy_image(new_dir_path=element_path,
                                            origin_dir_path=dir_path)

def execute_training_on_tensor(device, base_path):
    print('## TRAINING START')
    print('# base path:', base_path)

    _store_path = base_path + '/model/bottleneck'
    _iteration = config.ITERATION
    _model_dir = base_path + '/model/inception'
    _output_graph = base_path + '/model/retrained_graph.pb'
    _output_label = base_path + '/model/retrained_labels.txt'
    _image_dir = base_path + '/t_images'
    _summaries_dir = base_path + '/model/log'
    _tensor_name = device
    cmd = "python src/inception.py --image_dir={image_dir} \
                                    --saved_model_dir={model_dir} \
                                    --bottleneck_dir={store_path} \
                                    --how_many_training_steps={iteration} \
                                    --output_graph={output_graph} \
                                    --output_labels={output_label} \
                                    --summaries_dir={summaries_dir} \
                                    --final_tensor_name={tensor_name}".format(image_dir=_image_dir,
                                                                            model_dir=_model_dir,
                                                                            store_path=_store_path,
                                                                            iteration=_iteration,
                                                                            output_graph=_output_graph,
                                                                            output_label=_output_label,
                                                                            summaries_dir=_summaries_dir,
                                                                            tensor_name=_tensor_name)
    cmd_args = cmd.split()
    call(cmd_args)