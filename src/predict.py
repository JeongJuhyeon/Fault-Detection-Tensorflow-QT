import os

import numpy as np
import tensorflow as tf


def create_graph(modelFullPath):
    with tf.gfile.FastGFile(modelFullPath, 'rb') as graphFile :
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(graphFile.read())
        _ = tf.import_graph_def(graph_def, name='')

def run_inference_on_image(modelFullPath, labelsFullPath, imageDir, tensorName):
    images = os.listdir(imageDir)
    create_graph(modelFullPath)

    f = open(labelsFullPath, 'rb')
    lines = f.readlines()
    labels = [line.rstrip() for line in lines]

    print('labels: ', labels)
    print('images: ', images)
    rtValue = []

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name(tensorName + ':0')
        for image in images :
            imagePath = imageDir + '/' + image
            if not tf.gfile.Exists(imagePath):
                tf.logging.fatal('File does not exist %s', imagePath)
                break
            cur = {'imageName':image, 'results':[]}
            print('Now predict:', imagePath)
            image_data = tf.gfile.FastGFile(imagePath, 'rb').read()
            #image_data = np.fromfile(imagePath, dtype=np.float32)

            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-2:][::-1]
            for node_id in top_k :
                human_string = labels[node_id].decode('ascii')
                score = predictions[node_id]
                print('%s (score = %.5f)'% (human_string, score))
                cur['results'].append([human_string, score])

            rtValue.append(cur)

    return rtValue