import tensorflow as tf

data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255, # normalize pixel values
    rotation_range=20, # randomly rotate images by up to 20 degrees
    width_shift_range=0.2, # randomly shift images horizontally by up to 20% of image width
    height_shift_range=0.2, # randomly shift images vertically by up to 20% of image height
    shear_range=0.2, # randomly apply shearing transformations
    zoom_range=0.2, # randomly zoom in on images
    horizontal_flip=True, # randomly flip images horizontally
    fill_mode='nearest', # fill in any missing pixels with the nearest value
)

train_generator = data_generator.flow_from_directory(
    r'C:\Users\johnj\OneDrive\Desktop\Coding\Cat Recognition APP\output\train',
    target_size=(80, 80),
    batch_size=32,
    class_mode='categorical',
)

validation_generator = data_generator.flow_from_directory(
    r'C:\Users\johnj\OneDrive\Desktop\Coding\Cat Recognition APP\output\val',
    target_size=(80, 80),
    batch_size=32,
    class_mode='categorical',
)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(80, 80, 3)), #224, 224, 3
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(28, activation='softmax'),
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy', 'binary_accuracy'])

history = model.fit(
    train_generator,
    epochs=30,
    steps_per_epoch=974,
    validation_data=validation_generator,
    validation_steps=38992//32
)

# Save the model
model.save('cat_recognition_model.h5')