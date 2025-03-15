import tensorflow as tf
from tensorflow.keras.utils import plot_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Flatten, Dropout, Lambda, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import DenseNet121


# Función para crear el modelo con arquitectura multi-branch
def create_model(input_shape=(128, 128, 3)):
    # Base Model (DenseNet121)
    base_model = DenseNet121(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )

    layer_names = ['conv3_block12_concat', 'conv4_block24_concat', 'conv5_block16_concat']
    intermediate_outputs = [base_model.get_layer(name).output for name in layer_names]

    # Create a new model that outputs intermediate layers
    intermediate_model = Model(inputs=base_model.input, outputs=intermediate_outputs)

    # Define the branches for each intermediate output
    branch_outputs = []
    for output in intermediate_outputs:
        x = GlobalAveragePooling2D()(output)
        x = Lambda(lambda x: tf.math.l2_normalize(x, axis=-1), output_shape=lambda s: s)(x)
        x = Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001))(x)
        x = BatchNormalization()(x)
        branch_outputs.append(x)

    # Concatenate the branch outputs for score-level fusion
    fusion = tf.keras.layers.Concatenate()(branch_outputs)

    # Final dense layers
    x = Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001))(fusion)
    x = BatchNormalization()(x)
    x = Dropout(0.45)(x)
    final_output = Dense(2, activation='softmax')(x)

    # Combine everything into a model
    model = Model(inputs=base_model.input, outputs=final_output)

    optimizer = Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model
