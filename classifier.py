from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Dummy training data
TRAINING_DATA = [
    ("My internet is not working", "Technical Support"),
    ("I want to upgrade my plan", "Sales"),
    ("I have billing issues", "Billing"),
    ("I want to cancel my subscription", "Sales"),
    ("There is a connection problem", "Technical Support"),
]

texts, labels = zip(*TRAINING_DATA)

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(texts)

classifier = LogisticRegression()
classifier.fit(X_train, labels)

def classify_issue(issue_text):
    X_test = vectorizer.transform([issue_text])
    prediction = classifier.predict(X_test)
    return prediction[0]
