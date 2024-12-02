import os
import librosa
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from librosa.feature import chroma_cens, mfcc, spectral_centroid, zero_crossing_rate, spectral_contrast, spectral_bandwidth, spectral_flatness, spectral_rolloff
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def extract_features_from_file(file_path: str) -> dict:
    y, sr = librosa.load(file_path, mono=True, duration=30)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1)
    mfcc_std = np.std(mfccs, axis=1)

    harmonic, percussive = librosa.effects.hpss(y)
    hnr = np.mean(librosa.feature.rms(y=harmonic) / (librosa.feature.rms(y=percussive) + 1e-10))

    spectral_centroid_value = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_rolloff_value = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
    zero_crossing_rate_value = np.mean(librosa.feature.zero_crossing_rate(y))
    chroma = librosa.feature.chroma_cens(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    spectral_contrast_value = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))
    spectral_bandwidth_value = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    spectral_flatness_value = np.mean(librosa.feature.spectral_flatness(y=y))
    energy = np.sum(librosa.feature.rms(y=y) ** 2)
    rms = np.mean(librosa.feature.rms(y=y))

    rms_std = np.std(librosa.feature.rms(y=y))
    rms_max = np.max(librosa.feature.rms(y=y))
    rms_min = np.min(librosa.feature.rms(y=y))

    features = {
        "tempo": float(tempo),
        "mfcc_0": float(mfcc_mean[0]),
        "mfcc_1": float(mfcc_mean[1]),
        "mfcc_2": float(mfcc_mean[2]),
        "mfcc_3": float(mfcc_mean[3]),
        "mfcc_4": float(mfcc_mean[4]),
        "mfcc_5": float(mfcc_mean[5]),
        "mfcc_6": float(mfcc_mean[6]),
        "mfcc_7": float(mfcc_mean[7]),
        "mfcc_8": float(mfcc_mean[8]),
        "mfcc_9": float(mfcc_mean[9]),
        "mfcc_10": float(mfcc_mean[10]),
        "mfcc_11": float(mfcc_mean[11]),
        "mfcc_12": float(mfcc_mean[12]),
        "mfcc_std_0": float(mfcc_std[0]),
        "mfcc_std_1": float(mfcc_std[1]),
        "mfcc_std_2": float(mfcc_std[2]),
        "mfcc_std_3": float(mfcc_std[3]),
        "mfcc_std_4": float(mfcc_std[4]),
        "mfcc_std_5": float(mfcc_std[5]),
        "mfcc_std_6": float(mfcc_std[6]),
        "mfcc_std_7": float(mfcc_std[7]),
        "mfcc_std_8": float(mfcc_std[8]),
        "mfcc_std_9": float(mfcc_std[9]),
        "mfcc_std_10": float(mfcc_std[10]),
        "mfcc_std_11": float(mfcc_std[11]),
        "spectral_centroid": float(spectral_centroid_value),
        "spectral_rolloff": float(spectral_rolloff_value),
        "zero_crossing_rate": float(zero_crossing_rate_value),
        "chroma_0": float(chroma_mean[0]),
        "chroma_1": float(chroma_mean[1]),
        "chroma_2": float(chroma_mean[2]),
        "chroma_3": float(chroma_mean[3]),
        "chroma_4": float(chroma_mean[4]),
        "chroma_5": float(chroma_mean[5]),
        "chroma_6": float(chroma_mean[6]),
        "chroma_7": float(chroma_mean[7]),
        "chroma_8": float(chroma_mean[8]),
        "chroma_9": float(chroma_mean[9]),
        "chroma_10": float(chroma_mean[10]),
        "chroma_11": float(chroma_mean[11]),
        "spectral_contrast": float(spectral_contrast_value),
        "spectral_bandwidth": float(spectral_bandwidth_value),
        "spectral_flatness": float(spectral_flatness_value),
        "energy": float(energy),
        "rms": float(rms),
        "rms_std": float(rms_std),
        "rms_max": float(rms_max),
        "rms_min": float(rms_min),
        "hnr": float(hnr)
    }
    return features


def analyze_mp3_file(file_path: str) -> str:
    df = pd.DataFrame([extract_features_from_file(file_path)])
    model = joblib.load('model/trained_model.pkl')

    predicted_genre_from_model = model.predict(df)[0]
    os.remove(file_path)

    return predicted_genre_from_model


@app.route('/upload', methods=['POST'])
def upload_mp3():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if file and file.filename.endswith('.wav'):
        predictions = analyze_mp3_file(file_path=file_path)
        return jsonify({"predictions": predictions}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400


if __name__ == '__main__':
    app.run(debug=True)
