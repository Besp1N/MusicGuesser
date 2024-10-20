import joblib
import pandas as pd

model = joblib.load('src/trained_model.pkl')


def predict_genre_from_csv(csv_file: str) -> str:
    df = pd.read_csv(csv_file)
    predicted_genre_from_model = model.predict(df)[0]

    return predicted_genre_from_model


if __name__ == '__main__':
    predicted_genre = predict_genre_from_csv('test_features.csv')
    print(f"Predicted genre: {predicted_genre}")
