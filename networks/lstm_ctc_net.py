import tensorflow as tf

from .common import label_error_rate, loss, model, optimizer


def create_network(features, seq_len, num_classes, is_training):

    num_hidden = 100
    num_layers = 3

    cells = [tf.contrib.rnn.LSTMCell(num_hidden, state_is_tuple=True)
             for i in range(num_layers)]
    stack = tf.contrib.rnn.MultiRNNCell(cells,
                                        state_is_tuple=True)

    outputs, _ = tf.nn.dynamic_rnn(stack, features, seq_len, dtype=tf.float32)

    shape = tf.shape(features)
    batch_s, max_time_steps = shape[0], shape[1]

    outputs = tf.reshape(outputs, [-1, num_hidden])

    W = tf.Variable(tf.truncated_normal([num_hidden,
                                         num_classes],
                                        stddev=0.1))

    b = tf.Variable(tf.constant(0., shape=[num_classes]))

    # Doing the affine projection
    logits = tf.matmul(outputs, W) + b

    # Reshaping back to the original shape
    logits = tf.reshape(logits, [batch_s, -1, num_classes])

    # Time major
    logits = tf.transpose(logits, (1, 0, 2))
    return logits
