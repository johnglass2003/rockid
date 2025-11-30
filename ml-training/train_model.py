"""
Rock Classification Model Training Script
Uses MobileNetV2 for mobile-friendly deployment
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import json
import argparse
import matplotlib.pyplot as plt
import os

def create_model(num_classes, input_shape=(224, 224, 3)):
    """Create a MobileNetV2-based model for rock classification"""
    
    # Use MobileNetV2 as base (lightweight, mobile-friendly)
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Add classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_model(dataset_path, epochs=20, batch_size=32, img_size=224):
    """Train the rock classification model"""
    
    print("🪨 Starting Rock Classification Model Training...")
    print(f"📁 Dataset: {dataset_path}")
    print(f"📊 Epochs: {epochs}, Batch Size: {batch_size}")
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    
    # Load validation data
    validation_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    print(f"\n✅ Found {train_generator.num_classes} rock classes:")
    for class_name, idx in train_generator.class_indices.items():
        print(f"   {idx}: {class_name}")
    
    # Create model
    model = create_model(train_generator.num_classes)
    
    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print("\n📋 Model Summary:")
    model.summary()
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train model
    print("\n🏋️ Training model...")
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    # Fine-tune: Unfreeze some layers and train again
    print("\n🔧 Fine-tuning model...")
    base_model = model.layers[0]
    base_model.trainable = True
    
    # Freeze all layers except the last 20
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    history_fine = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=10,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('rock_classifier_model.h5')
    print("\n✅ Model saved as 'rock_classifier_model.h5'")
    
    # Save class names
    class_names = {v: k for k, v in train_generator.class_indices.items()}
    with open('class_names.json', 'w') as f:
        json.dump(class_names, f, indent=2)
    print("✅ Class names saved as 'class_names.json'")
    
    # Plot training history
    plot_history(history, history_fine)
    
    # Evaluate model
    print("\n📊 Final Evaluation:")
    results = model.evaluate(validation_generator)
    print(f"   Validation Loss: {results[0]:.4f}")
    print(f"   Validation Accuracy: {results[1]:.4f}")
    print(f"   Top-3 Accuracy: {results[2]:.4f}")
    
    return model, history

def plot_history(history1, history2):
    """Plot training history"""
    
    # Combine histories
    acc = history1.history['accuracy'] + history2.history['accuracy']
    val_acc = history1.history['val_accuracy'] + history2.history['val_accuracy']
    loss = history1.history['loss'] + history2.history['loss']
    val_loss = history1.history['val_loss'] + history2.history['val_loss']
    
    epochs_range = range(len(acc))
    
    plt.figure(figsize=(12, 5))
    
    # Accuracy plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    
    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    print("✅ Training history saved as 'training_history.png'")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train rock classification model')
    parser.add_argument('--dataset', type=str, required=True, help='Path to dataset folder')
    parser.add_argument('--epochs', type=int, default=20, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--img-size', type=int, default=224, help='Image size')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.dataset):
        print(f"❌ Error: Dataset path '{args.dataset}' does not exist")
        exit(1)
    
    train_model(args.dataset, args.epochs, args.batch_size, args.img_size)
    print("\n🎉 Training complete! Ready to deploy.")
