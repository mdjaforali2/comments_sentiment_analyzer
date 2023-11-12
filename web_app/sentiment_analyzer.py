from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import os
from joblib import load
import base64
from io import BytesIO
from django.shortcuts import render


# Determine the path to the models folder within your app
models_folder = os.path.join(os.path.dirname(__file__), 'models')

# Load the pre-trained model and TF-IDF vectorizer
model_path = os.path.join(models_folder, 'sentiment_model.joblib')
tfidf_vectorizer_path = os.path.join(models_folder, 'tfidf_vectorizer.joblib')

model = load(model_path)
tfidf_vectorizer = load(tfidf_vectorizer_path)



def analyze_sentiment_with_plot(comment, threshold=0.5):
    # Preprocess the comment
    processed_comment = handle_negation(re.sub('[^a-zA-Z]', ' ', comment.lower()))

    # Transform the processed comment using the TF-IDF vectorizer
    comment_tfidf = tfidf_vectorizer.transform([processed_comment])

    # Predict the sentiment
    sentiment_probabilities = model.predict_proba(comment_tfidf)[0]

    # Determine sentiment based on the threshold
    sentiment_label = 'Positive' if sentiment_probabilities[1] > threshold else 'Negative'

    # Create a bar plot for the predicted probabilities
    classes = ['Negative', 'Positive']
    y_pos = np.arange(len(classes))

    plt.bar(y_pos, sentiment_probabilities, align='center', alpha=0.5)
    plt.xticks(y_pos, classes)
    plt.ylabel('Probability')
    plt.title('Sentiment Prediction Probabilities')

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convert the image to base64 encoding
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Close the plot
    plt.close()

    # Return sentiment label, probabilities, and image_base64
    return sentiment_label, sentiment_probabilities, image_base64



# Now, you can use the 'image_base64' variable to embed the plot in your web application.


def handle_negation(text):
    # Define a list of negative words
    negation_words = ['no', 'not', 'never']

    # Tokenize the text into words
    words = text.split()

    # Iterate through the words
    for i in range(len(words)):
        # If a negative word is encountered, invert the sentiment of the following word
        if words[i] in negation_words and i + 1 < len(words):
            words[i + 1] = 'not_' + words[i + 1]

    # Join the modified words back into a sentence
    modified_text = ' '.join(words)

    return modified_text
