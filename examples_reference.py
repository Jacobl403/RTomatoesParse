import tensorflow as tf
import keras
def init_examples():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    print(train_images[:1].reshape(-1, 28 * 28) / 255.0)
    model = keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=[keras.metrics.SparseCategoricalAccuracy()])

    model.summary()
    # keras.utils.plot_model(model, to_file='model_1.png', show_shapes=True)
    print(model.get_state_tree())
