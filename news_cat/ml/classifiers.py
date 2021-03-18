from numpy import ndarray
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score


def tfidf_logistic_classifier(
    trainX: ndarray, trainY: ndarray, testX: ndarray, testY: ndarray
):
    clf = LogisticRegression(multi_class="multinomial")
    clf.fit(trainX, trainY)

    print("Evaluating the model...")
    metrics = {}
    preds = clf.predict(testX)

    metrics["embed"] = "tfidf"
    metrics["clf"] = "logistic"
    metrics["acc"] = accuracy_score(preds, testY)
    metrics["f1"] = f1_score(preds, testY, average="weighted")
    metrics["precision"] = precision_score(preds, testY, average="weighted")

    return clf, metrics
