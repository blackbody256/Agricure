import tensorflow as tf



# Load your model
model = tf.keras.models.load_model("newresult.h5")

# Print full model summary
model.summary()

# Check output shape
print("\nOutput shape:", model.output_shape)

# If needed: test on a dummy image input
import numpy as np
dummy_input = np.random.rand(1, 224, 224, 3)  # match model input size
prediction = model.predict(dummy_input)
print("\nModel output:", prediction)
print("Output shape:", prediction.shape)
