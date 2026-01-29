import tensorflow as tf

_model = None

def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(
            "model/transfer_learned_model.h5",
            compile=False
        )
    return _model