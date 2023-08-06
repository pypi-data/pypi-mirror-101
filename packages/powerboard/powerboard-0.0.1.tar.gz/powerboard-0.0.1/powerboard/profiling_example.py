#Copyright 2020 The TensorFlow Authors.
# Modifications Copyright 2020 MatheusCod, juliokiyoshi
#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
#from packaging import version

import os

#####################################################################
from powerboard import libipmi
#####################################################################

#!pip install -U tensorboard_plugin_profile

import tensorflow as tf

#!pip install tensorflow-datasets

import tensorflow_datasets as tfds
tfds.disable_progress_bar()

print("TensorFlow version: ", tf.__version__)


stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
logdir = 'logs/fit/%s' % stamp
writer = tf.summary.create_file_writer(logdir)
tf.summary.trace_on(profiler=True)

"""
device_name = tf.test.gpu_device_name()
if not device_name:
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))
"""

(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., label

ds_train = ds_train.map(normalize_img)
ds_train = ds_train.batch(128)

ds_test = ds_test.map(normalize_img)
ds_test = ds_test.batch(128)

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
  tf.keras.layers.Dense(128,activation='relu'),
  tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=tf.keras.optimizers.Adam(0.001),
    metrics=['accuracy']
)

# Create a TensorBoard callback

#####################################################################
libipmi.start()
#####################################################################

model.fit(ds_train,
          epochs=5,
          validation_data=ds_test)

#####################################################################
libipmi.stop()
libipmi.dbToCSV('./data')
#####################################################################

with writer.as_default():
  tf.summary.trace_export(
      name="conv", # optional name
      step=0,
      profiler_outdir=logdir)
