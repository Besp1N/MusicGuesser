from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib


def prepare_data(df):
    y = df['genre']
    X = df.drop(columns=['genre'])

    for column in X.columns:
        if X[column].dtype == 'object':
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column])

    return X, y


def balance_data(X, y):
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    return X_resampled, y_resampled


def train_model(df):
    X, y = prepare_data(df)
    X_balanced, y_balanced = balance_data(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

    model = RandomForestClassifier(
        n_estimators=138,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model


if __name__ == '__main__':
    df = pd.read_csv('src/data_updated.csv')
    model = train_model(df)
    joblib.dump(model, 'src/trained_model.pkl')
