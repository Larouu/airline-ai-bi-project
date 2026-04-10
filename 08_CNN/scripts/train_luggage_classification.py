#!/usr/bin/env python3
"""
Baggage Handling QC Classification Model
Trains a CNN to classify luggage as:
- damaged_luggage: Luggage with visible damage or mishandling marks
- good_luggage: Luggage in good condition

Automatically generates incident reports and improves SDG 12 responsible operations.
Uses MobileNetV2 transfer learning.
"""

import os
import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from datetime import datetime

def create_model(input_shape=(224, 224, 3), num_classes=2):
    """Create transfer learning model using MobileNetV2."""
    base_model = keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = False
    
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Rescaling(1./255),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0001)),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0001)),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model, base_model

def train_luggage_classification(data_root, epochs=20, batch_size=16, learning_rate=0.001):
    """Train luggage/baggage QC classification model."""
    
    print("=" * 70)
    print("🧳 BAGGAGE HANDLING QC CLASSIFICATION MODEL")
    print("=" * 70)
    print(f"📂 Data root: {data_root}")
    print(f"⚙️  Configuration: epochs={epochs}, batch_size={batch_size}, lr={learning_rate}")
    
    # Setup paths
    train_dir = os.path.join(data_root, "train")
    val_dir = os.path.join(data_root, "val")
    test_dir = os.path.join(data_root, "test")
    model_dir = os.path.join(data_root, "..", "..", "models")
    os.makedirs(model_dir, exist_ok=True)
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load data
    print("\n📥 Loading training data...")
    train_generator = train_datagen.flow_from_directory(
        train_dir, target_size=(224, 224), batch_size=batch_size, class_mode='categorical'
    )
    
    print("📥 Loading validation data...")
    val_generator = val_test_datagen.flow_from_directory(
        val_dir, target_size=(224, 224), batch_size=batch_size, class_mode='categorical'
    )
    
    print("📥 Loading test data...")
    test_generator = val_test_datagen.flow_from_directory(
        test_dir, target_size=(224, 224), batch_size=batch_size, class_mode='categorical', shuffle=False
    )
    
    # Get class names
    class_names = sorted(train_generator.class_indices.keys())
    print(f"\n🏷️  Classes: {class_names}")
    print(f"📊 Train samples: {train_generator.samples}")
    print(f"📊 Val samples: {val_generator.samples}")
    print(f"📊 Test samples: {test_generator.samples}")
    
    # Create model
    print("\n🏗️  Creating model...")
    model, base_model = create_model(num_classes=len(class_names))
    model.summary()
    
    # Compile
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train
    print("\n🚀 Starting training...")
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate on test set
    print("\n📊 Evaluating on test set...")
    test_loss, test_acc, test_prec, test_rec = model.evaluate(test_generator, verbose=0)
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Precision: {test_prec:.4f}")
    print(f"Test Recall: {test_rec:.4f}")
    
    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(model_dir, f"luggage_classification_model_{timestamp}.keras")
    model.save(model_path)
    print(f"\n✅ Model saved: {model_path}")
    
    # Plot history
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    
    axes[0].plot(history.history['loss'], label='Train Loss')
    axes[0].plot(history.history['val_loss'], label='Val Loss')
    axes[0].set_title('Model Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].plot(history.history['accuracy'], label='Train Acc')
    axes[1].plot(history.history['val_accuracy'], label='Val Acc')
    axes[1].set_title('Model Accuracy')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].legend()
    axes[1].grid(True)
    
    plot_path = os.path.join(model_dir, f"luggage_classification_history_{timestamp}.png")
    plt.savefig(plot_path, dpi=100, bbox_inches='tight')
    print(f"✅ Training plot saved: {plot_path}")
    
    return model, history

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train luggage classification model")
    parser.add_argument("--data-root", type=str,
                       default=r"c:\Users\achre\Downloads\Esprit\DL\Ailines project\08_CNN\data\luggage",
                       help="Root data directory")
    parser.add_argument("--epochs", type=int, default=20, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    
    args = parser.parse_args()
    
    train_luggage_classification(
        data_root=args.data_root,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr
    )
