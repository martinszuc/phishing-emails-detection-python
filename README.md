# Phishing Email Detection - Machine Learning Component

This repository hosts the machine learning component of a project aimed at detecting phishing emails. Android application that utilizes federated machine learning techniques for enhanced privacy and decentralized learning. Focused on preprocessing email data, training a machine learning model, and making predictions to identify potential phishing attempts, project is a part of my Bachelor's thesis on phishing email detection.

## Project Overview

The core of this project lies in its ability to effectively identify phishing attempts within emails by analyzing a wide range of features. Utilizing advanced machine learning techniques, the project employs a series of feature finders that extract and scrutinize email characteristics, such as embedded URLs, HTML content, attachments, and more. These features are then fed into a TensorFlow-based model, which is trained to discern between phishing and legitimate emails. The ultimate goal is to integrate this model into an Android application, leveraging federated learning to improve model accuracy while maintaining user privacy.

### Main Features

- **EML to MBOX Conversion**: A script designed to convert `.eml` email messages from a sample folder into an `.mbox` file, used for feature extraction, model training, and prediction processes.
- **Data Preparation**: Automated scripts that load, preprocess, and cleanse email datasets, preparing them for effective model training.
- **Model Training**: Utilizes TensorFlow to construct and train a sophisticated machine learning model adept at distinguishing phishing emails.
- **Prediction**: Employs the trained model to evaluate new datasets, predicting potential phishing attempts with a suite of evaluation metrics to gauge performance.

### Feature Finders and Detection Strategy

Our phishing detection uses several feature finders, each responsible for extracting specific elements from emails that are commonly used by phishing attempts:

- **HTMLFormFinder**: Identifies HTML forms within emails, a common phishing vector to solicit user information.
- **IFrameFinder**: Detects the use of IFrames, potentially embedding malicious content invisibly.
- **FlashFinder**: Searches for Flash content links, which could execute harmful scripts.
- **AttachmentFinder**: Counts email attachments, which may contain malicious payloads.
- **HTMLContentFinder**: Looks for specific HTML content indicative of phishing.
- **URLsFinder**: Extracts and evaluates URLs found within emails for malicious links.
- **ExternalResourcesFinder**: Identifies external resources linked within emails that could be harmful.
- **JavascriptFinder**: Detects JavaScript, which can be used in phishing for malicious activities.
- **CssFinder**: Searches for custom CSS that might be used to disguise phishing attempts.
- **IPsInURLs**: Checks for IP addresses in URLs, a technique used to bypass domain name suspicion.
- **AtInURLs**: Identifies '@' symbols in URLs, which can be a sign of deceptive links.
- **EncodingFinder**: Analyzes the content encoding for signs of obfuscation or unusual patterns.


### Project Context

This machine learning component is part of a larger system designed for phishing email detection on Android devices. For more information on the entire project, visit the main repository: [Phishing Emails Detection Project](https://github.com/martinszuc/phishing-emails-detection).

## Getting Started

Follow these instructions to set up the machine learning component of the phishing email detection project on your local machine for development, testing, and contribution purposes.

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- TensorFlow 2.x
- Pandas
- NumPy
- scikit-learn

### Usage
Usage of the scripts is better described and understandable in the [Main Notebook](https://github.com/martinszuc/phishing-emails-detection-python/blob/main/main.ipynb).

## Authors

-  [martinszuc](https://github.com/martinszuc)

## Acknowledgments and References

This project builds upon and extends the work found at [MachineLearningPhishing](https://github.com/diegoocampoh/MachineLearningPhishing) by Diego Ocampo.

### Data Sources

The data used for training the phishing detection model were sourced from two main repositories, which provided a rich dataset of phishing emails:

- [Phishing Pot Dataset](https://github.com/rf-peixoto/phishing_pot) by rf-peixoto
- [Phishing Dataset](https://monkey.org/~jose/phishing/) by jose at monkey.org

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
