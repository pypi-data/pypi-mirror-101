from keras.layers import *
import keras.backend as K
from keras.models import Model


def add_noise_in_trian(x):
    """

    :param x: layers input
    :return:  x+noise
    :useage: x_in = Input(shape=(10,))
             x = Lambda(add_noise_in_trian)(x_in)
    """

    noise = K.random_normal(K.shape(x))
    _x = x + noise
    return K.in_train_phase(_x, x)


class Mylayer(Layer):
    """
         single layers example
    """

    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(Mylayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='kernel',
            shape=(input_shape[0, self.ouput_dim]),
            initializer='uniform',
            trainable=True
        )

    def call(self, inputs, **kwargs):
        return K.dot(inputs, inputs)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)


class Dense_with_center_loss(Layer):
    """
    usage :

    x_in = Input(shape=(784,))
    f = Dense(2)(x_in)
    dense_center = Dense_with_center_loss(10)
    output = dense_center(f)
    model = Model(x_in,output)
    model.compile(loss=dense_center.loss,optimizer='adam',metrics=['sparse_categorical_crossentropy'])
    model.fit(x_train,y_train,epochs=10,callbacks=[])

    """

    def __init__(self, out_dim, **kwargs):
        self.out_dim = out_dim
        super(Dense_with_center_loss, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='kernel',
            shape=(input_shape[1], self.out_dim),
            initializer='glorot_normal',
            trainable=True
        )
        self.bias = self.add_weight(
            name='bias',
            shape=(self.out_dim),
            initializer='zeros',
            trainable=True
        )
        self.center = self.add_weight(
            name='center',
            shape=(self.out_dim, input_shape[1]),  ##
            initializers='glorot',
            trainable=True
        )

    def call(self, inputs, **kwargs):
        self.inputs = inputs
        return K.dot(inputs, self.kernel) + self.bias

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.out_dim)

    def loss(self, y_true, y_pred, lamb=0.5):
        y_true = K.cast(y_true, 'int32')
        crossentropy = K.sparse_categorical_crossentropy(y_true, y_pred, from_logits=True)
        centers = K.gather(self.center, y_pred[:, 0])
        center_loss = K.sum(K.square(centers - self.inputs), axis=1)
        return crossentropy + lamb * center_loss
