import tensorflow as tf
from jhsp.Sann.weights22netweights import W22NW


class Model(tf.keras.Model):
    def __init__(self,ori_weights,final_activation,hp):
        super().__init__()

        self.layer_list = []

        hidden_layers = []
        w22n = W22NW()


        for i in range(hp.Int('num_layers', 1, 5)):
            hidden_layers.append(hp.Int('units_' + str(i),
                                            min_value=32,
                                            max_value=512,
                                            step=32))

        initial_weigh, error = w22n.Weights2HW(ori_weights, hidden_layers, False)

        for i,weights in enumerate(initial_weigh):

            kernel_initializer = tf.constant_initializer(weights)

            if i != len(initial_weigh) -1:   #不是最后一层的时候，激活函数为rule

                exec("self.layer{} = tf.keras.layers.Dense(units=weights.shape[1],activation='relu' ,kernel_initializer=kernel_initializer)".format(i))
            else:
                exec("self.layer{0} = tf.keras.layers.Dense(units=weights.shape[1],activation='{1}',kernel_initializer=kernel_initializer)".format(i,final_activation))

            exec('self.layer_list.append(self.layer{})'.format(i))

    def build(self, input_shape):
        super(Model, self).build(input_shape)

    def call(self, x):

        for layer in  self.layer_list:
            x = layer(x)

        return x


