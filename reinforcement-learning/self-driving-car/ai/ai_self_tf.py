import numpy as np
import random
import shutil
import tensorflow as tf
import tensorflow.contrib.slim as slim
import collections
import os
from tensorflow.python import debug as tf_debug

HIDDEN_LAYER_SIZE = 30

Transition = collections.namedtuple("Transition", "state action reward next_state")


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)


class Dqn():
    def __init__(self, input_size, nb_action, gamma):
        try:
            shutil.rmtree("train/")
        except OSError:
            print ""
        self.reward_window = []
        self.gamma = gamma
        self.memory = ReplayMemory(300000)
        self.last_action = 0
        self.last_state = np.zeros(input_size)
        self.num_action = nb_action

        self.input_tensor = tf.placeholder(shape=[None, input_size], dtype=tf.float32)

        self.fc1 = slim.fully_connected(inputs=self.input_tensor, num_outputs=30, activation_fn=tf.nn.relu, scope="fc1")
        # self.fc2 = slim.fully_connected(inputs=self.fc1, num_outputs=30, activation_fn=tf.nn.relu, scope="fc2")
        self.q = slim.fully_connected(inputs=self.fc1, num_outputs=nb_action, activation_fn=None, scope="q")
        self.softmax = slim.softmax(self.q * 70, scope="softmax")
        slim.summary.tensor_summary("softmax", self.softmax)
        self.chosen_action = tf.argmax(self.softmax, axis=1)

        self.action = tf.placeholder(shape=[100], dtype=tf.int32)
        self.target = tf.placeholder(shape=[100], dtype=tf.float32)

        self.hot = slim.one_hot_encoding(self.action, self.num_action, scope="one_hot")
        self.predictions = tf.reduce_sum(self.hot * self.q, axis=1)
        self.loss = tf.reduce_sum((self.predictions - self.target) ** 2)
        # self.loss = slim.losses.mean_squared_error(predictions=self.predictions, labels=self.target)

        self.optimizer = slim.train.AdamOptimizer()
        # slim.losses.get_total_loss()
        # slim.summary.scalar("loss", self.loss)
        # slim.summary.histogram("loss", self.loss)

        self.training = slim.learning.create_train_op(total_loss=self.loss, optimizer=self.optimizer,
                                                      summarize_gradients=True)

        # self.grads_and_vars = self.optimizer.compute_gradients(self.loss)
        # Change grads_and_vars as you wish
        # self.training = self.optimizer.apply_gradients(self.grads_and_vars)

        sess = tf.Session()
        self.sess = sess
        # self.sess = tf_debug.LocalCLIDebugWrapperSession(sess)
        # self.sess = tf_debug.TensorBoardDebugWrapperSession(sess, "localhost:54027")

        self.ctr = 0

        self.summary_op = slim.summary.merge_all()
        self.train_writer = tf.summary.FileWriter('train/', sess.graph)
        init = tf.global_variables_initializer()
        self.saver = tf.train.Saver()
        self.sess.run(init)

    def _learn(self, transitions):
        states = np.array(map(lambda transition: transition.state, transitions))

        next_stateQs = self.sess.run(self.q, feed_dict={
            self.input_tensor: np.array(map(lambda transition: transition.next_state, transitions))})

        rewards = np.array(map(lambda transition: transition.reward, transitions))
        actions = np.array(map(lambda transition: transition.action, transitions))
        next_max_qs = next_stateQs.max(1)
        target = (self.gamma * next_max_qs) + rewards

        predictions, loss, training, summary = self.sess.run(
            [self.predictions, self.loss, self.training, self.summary_op],
            feed_dict={
                self.input_tensor: states,
                self.action: actions,
                self.target: target})
        print loss
        self.train_writer.add_summary(summary)

    def update(self, reward, new_signal):
        self.memory.push(
            Transition(state=self.last_state, action=self.last_action, reward=reward, next_state=new_signal))

        q_orig, softmax, action_value = self.sess.run([self.q, self.softmax, self.chosen_action],
                                                      feed_dict={self.input_tensor: [new_signal]})
        print "Qvalues"
        print q_orig
        # print "Qvalues after softmax"
        # print softmax
        print reward
        action = action_value[0]

        if len(self.memory.memory) > 300:
            transitions = self.memory.sample(100)
            self._learn(transitions)

        self.last_action = action
        self.last_state = new_signal
        self.reward_window.append(reward)

        return action

    def score(self):
        return sum(self.reward_window) / len(self.reward_window) + 1.

    def save(self):
        self.saver.save(self.sess, "./last_brain_tf.tf")

    def load(self):
        if os.path.exists("last_brain_tf.tf"):
            print("===>> Loading checkpoint ...")
            self.saver.restore(self.sess, "./last_brain_tf.tf")
        else:
            print("Nothing to load")
