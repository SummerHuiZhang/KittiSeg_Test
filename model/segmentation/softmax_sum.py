from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ipdb

import tensorflow as tf


def decoder(hypes, logits):
    """ Applies decoder to the logits

    Args:
      logits: Logits tensor, float - [batch_size, NUM_CLASSES].

    Return:
      logits: the logits are already decoded.
    """

    return logits


def loss(hypes, logits, labels):
    """Calculates the loss from the logits and the labels.

    Args:
      logits: Logits tensor, float - [batch_size, NUM_CLASSES].
      labels: Labels tensor, int32 - [batch_size].

    Returns:
      loss: Loss tensor of type float.
    """
    # Convert from sparse integer labels in the range [0, NUM_CLASSSES)
    # to 1-hot dense float vectors (that is we will have batch_size vectors,
    # each with NUM_CLASSES values, all of which are 0.0 except there will
    # be a 1.0 in the entry corresponding to the label).
    with tf.name_scope('loss'):
        logits = tf.reshape(logits, (-1, 2))
        labels = tf.to_float(tf.reshape(labels, (-1, 2)))

        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
            logits, labels, name='xentropy')

        cross_entropy_mean = tf.reduce_mean(
            cross_entropy, name='xentropy_mean')
        tf.add_to_collection('losses', cross_entropy_mean)

        loss = tf.add_n(tf.get_collection('losses'), name='total_loss')
    return loss


def evaluation(hypes, logits, labels):
    """Evaluate the quality of the logits at predicting the label.

    Args:
      logits: Logits tensor, float - [batch_size, NUM_CLASSES].
      labels: Labels tensor, int32 - [batch_size], with values in the
        range [0, NUM_CLASSES).

    Returns:
      A scalar int32 tensor with the number of examples (out of batch_size)
      that were predicted correctly.
    """
    # For a classifier model, we can use the in_top_k Op.
    # It returns a bool tensor with shape [batch_size] that is true for
    # the examples where the label's is was in the top k (here k=1)
    # of all logits for that example.
    with tf.name_scope('eval'):
        logits = tf.reshape(logits, (-1, 2))
        labels = tf.reshape(labels, (-1, 2))
        dense_labels = labels[:, 1]
        correct = tf.nn.in_top_k(logits, dense_labels, 1)
        # Return the number of true entries.
        return tf.reduce_mean(tf.cast(correct, tf.float32)) 
