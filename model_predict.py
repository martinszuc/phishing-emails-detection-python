import numpy as np
import pandas as pd
import tensorflow as tf
import utils_feature_extraction as ufe
import utils_data_preparation as udp


def predict_email_class(model, filepath):
    # Load and preprocess mbox file
    ufe.process_mbox_to_csv(filepath, "iso-8859-1", limit=200, is_phishy=None)
    
    # Load features from the processed CSV
    data = pd.read_csv(filepath + "-export.csv")
    print(f"Number of emails processed: {data.shape[0]}")
    print("Sample of loaded data:")
    print(data.head())
    
    # Information on data types and columns
    print("\nColumns and their data types:")
    print(data.dtypes)
    
    # Drop 'is_phishy' column if it exists (it's not needed for prediction)
    if 'is_phishy' in data.columns:
        data.drop(columns=['is_phishy'], inplace=True)
    
    # Preprocess features
    preprocessed_df = udp.preprocess_features(data, is_for_prediction=True)

    # Print preprocessed data information
    print("\nColumns and their data types after preprocessing:")
    print(preprocessed_df.dtypes)
    print(preprocessed_df.head())  # Optionally print a sample of preprocessed data
    
    # Convert DataFrame to the dictionary format for TensorFlow prediction
    feature_dict = {name: np.array(value) for name, value in preprocessed_df.items()}

    # Make predictions
    predictions = model.predict(feature_dict)
    return predictions

def main():
    # Load the trained model
    model_path = 'tf_model_saved'
    model = tf.keras.models.load_model(model_path)

    # Filepath to the mbox file
    filepath = 'samples_res/emails-samples.mbox'

    # Predict on the mbox file
    predictions = predict_email_class(model, filepath)
    print("Predictions:")
    print(predictions)

if __name__ == '__main__':
    main()