import tensorflow as tf


class Model(tf.keras.Model):
    def __init__(self,initial_weigh,final_activation):
        super().__init__()

        self.layer_list = []

        for i,weights in enumerate(initial_weigh):

            if i != len(initial_weigh) -1:   #不是最后一层的时候，激活函数为rule
                exec("self.layer{} = tf.keras.layers.Dense(units=weights.shape[1],activation='relu' )".format(i))
            else:
                exec("self.layer{} = tf.keras.layers.Dense(units=weights.shape[1],activation='{}')".format(i,final_activation))

            exec('self.layer_list.append(self.layer{})'.format(i))

    def call(self, x):

        for layer in  self.layer_list:
            x = layer(x)


        return x



