import os
import caer
import canaro
import gc
import tensorflow as tf


IMAGE_SIZE = (100, 100)
channel = 1
char_path = r'C:\Users\johnj\OneDrive\Desktop\Coding\Cat Recognition APP\Cat Images\Training Images' #the path where the data is imported

#char_dict = {}
characters = []
for char in os.listdir(char_path):
    characters.append(char) #(name_of_folder:number_of_images)
print(characters)
# char_dict = caer.sort_dict(char_dict, descending=True) #sorting char_dict by the number of images in each folder
# characters = []
# for a in char_dict:
#     characters.append(a[0])

#creating the training data
#looping through characters and finding the folder of each character from char_path and adding them into the training set
train = caer.preprocess_from_dir(char_path, characters, channels=channel, IMG_SIZE=IMAGE_SIZE, isShuffle=True)
print('finished preprocessing')

#separating the training set into figures and labels
featureSet, labels = caer.sep_train(train, IMG_SIZE=IMAGE_SIZE)

#normalizing the features into 0s and 1s (converting numerical integers into binary class vectors)
featureSet = caer.normalize(featureSet)
labels = tf.keras.utils.to_categorical(labels, len(characters))

#val_ratio means the ratio of validation data to the number of input data (2:8)
x_train, x_val, y_train, y_val = caer.train_val_split(featureSet, labels, val_ratio=0.2)

#deleting useless variables
del train
del featureSet
del labels
gc.collect()

BATCH_SIZE = 32
EPOCHS = 10

#image data generator
#it's generating new images to train on
dataGen = canaro.generators.imageDataGenerator()
train_gen = dataGen.flow(x_train, y_train, batch_size=BATCH_SIZE)

#creating the model
model = canaro.models.createDefaultModel(IMG_SIZE=IMAGE_SIZE[0], channels=channel, output_dim=len(characters))

model.summary()

#callback list
#schedules the model to train between certain intervals so it's more efficient and fast 
callbacks_list = [tf.keras.callbacks.LearningRateScheduler(canaro.lr_schedule)]

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss=tf.keras.losses.BinaryCrossentropy(), metrics=["accuracy", "binary_accuracy"])
print('finished compiling')

training = model.fit(train_gen, steps_per_epoch=len(x_train)//BATCH_SIZE, epochs=EPOCHS, validation_data=(x_val, y_val), validation_steps=len(y_val)//BATCH_SIZE, callbacks = callbacks_list)
print('finished training')

# save model and architecture to single file
model.save("final_model3.h5")
print("Saved model to disk")
