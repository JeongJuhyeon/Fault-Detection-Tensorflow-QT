import tensorflow as tf
import cv2
import numpy as np
import config


class ImportGraph():
    def __init__(self, path, number):
        self.path = path
        self.number = number
        self.location = path + "/model/model"
        self.graph = tf.Graph()

        #tf.add_to_collection(path, self.model)
        self.sess = tf.Session(graph=self.graph)
        with self.graph.as_default():
            saver = tf.train.import_meta_graph(self.location + '.meta',
                                               clear_devices=True)
            saver.restore(self.sess,self.location)

        #self.activation = tf.get_collection(path)[0]
        self.image_size = config.IMAGE_SIZE
        self.num_channels = config.NUM_CHANNEL

    def convert_image_to_npMatrix(self, filename):
        images = []
        image = cv2.imread(filename)
        image = cv2.resize(image, ( self.image_size, self.image_size), 0, 0, cv2.INTER_LINEAR)
        images.append(image)
        images = np.array(images, dtype = np.uint8)
        images = images.astype('float32')
        images = np.multiply(images, 1.0/ 255.0)
        return images

    def predict_image_on_tensor(self, image_path):
        images = self.convert(image_path)

        x_batch = images.reshape(1, self.image_size, self.image_size, self.num_channels)
        #graph name-y
        y_pred = self.graph.get_tensor_by_name(self.path + "_pred:0")
        x = self.graph.get_tensor_by_name(self.path + "_x:0")
        y_true = self.graph.get_tensor_by_name(self.path + "_true:0")
        y_test_images = np.zeros((1, self.number))

        feed_dict_testing = {x: x_batch, y_true: y_test_images}

        return self.sess.run(y_pred, feed_dict= feed_dict_testing)