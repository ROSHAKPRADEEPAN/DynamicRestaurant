import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../churn_model.pkl')

def load_model():
    """
    Loads the pre-trained churn prediction model.
    """
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    return model

def predict_churn(features):
    """
    Predicts churn probability based on input features.
    :param features: List or array of input features
    :return: Churn probability
    """
    model = load_model()
    prediction = model.predict_proba([features])[0][1]  # Probability of churn
    return prediction