import os
import librosa
import numpy as np
import pandas as pd
from librosa.beat import beat_track
from librosa.feature import chroma_cens, mfcc, spectral_centroid, zero_crossing_rate, spectral_contrast, \
    spectral_bandwidth, spectral_flatness, spectral_rolloff
import dir_paths


def extract_features() -> list[dict[str, any]]:
    paths: dict[str, str] = dir_paths.get_dir_names()
    features_list = []
    i: int = 0
    for directory in paths.values():
        for filename in os.listdir(directory):
            if filename.endswith('.wav'):
                print(f'Processing {i} - {filename}')
                y, sr = librosa.load(f'{directory}/{filename}', mono=True, duration=30)

                tempo, _ = beat_track(y=y, sr=sr)
                mfccs = mfcc(y=y, sr=sr, n_mfcc=13)
                mfcc_mean = np.mean(mfccs, axis=1)
                mfcc_std = np.std(mfccs, axis=1)

                harmonic, percussive = librosa.effects.hpss(y)
                hnr = np.mean(librosa.feature.rms(y=harmonic) / (librosa.feature.rms(y=percussive) + 1e-10))

                spectral_centroid_value = np.mean(spectral_centroid(y=y, sr=sr))
                spectral_rolloff_value = np.mean(spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
                zero_crossing_rate_value = np.mean(zero_crossing_rate(y))
                chroma = chroma_cens(y=y, sr=sr)
                chroma_mean = np.mean(chroma, axis=1)
                spectral_contrast_value = np.mean(spectral_contrast(y=y, sr=sr))
                spectral_bandwidth_value = np.mean(spectral_bandwidth(y=y, sr=sr))
                spectral_flatness_value = np.mean(spectral_flatness(y=y))
                energy = np.sum(librosa.feature.rms(y=y) ** 2)
                rms = np.mean(librosa.feature.rms(y=y))

                rms_std = np.std(librosa.feature.rms(y=y))
                rms_max = np.max(librosa.feature.rms(y=y))
                rms_min = np.min(librosa.feature.rms(y=y))

                features = {
                    "tempo": (tempo, np.float32),
                    "mfcc_0": (mfcc_mean[0], np.float32),
                    "mfcc_1": (mfcc_mean[1], np.float32),
                    "mfcc_2": (mfcc_mean[2], np.float32),
                    "mfcc_3": (mfcc_mean[3], np.float32),
                    "mfcc_4": (mfcc_mean[4], np.float32),
                    "mfcc_5": (mfcc_mean[5], np.float32),
                    "mfcc_6": (mfcc_mean[6], np.float32),
                    "mfcc_7": (mfcc_mean[7], np.float32),
                    "mfcc_8": (mfcc_mean[8], np.float32),
                    "mfcc_9": (mfcc_mean[9], np.float32),
                    "mfcc_10": (mfcc_mean[10], np.float32),
                    "mfcc_11": (mfcc_mean[11], np.float32),
                    "mfcc_12": (mfcc_mean[12], np.float32),
                    "mfcc_std_0": (mfcc_std[0], np.float32),
                    "mfcc_std_1": (mfcc_std[1], np.float32),
                    "mfcc_std_2": (mfcc_std[2], np.float32),
                    "mfcc_std_3": (mfcc_std[3], np.float32),
                    "mfcc_std_4": (mfcc_std[4], np.float32),
                    "mfcc_std_5": (mfcc_std[5], np.float32),
                    "mfcc_std_6": (mfcc_std[6], np.float32),
                    "mfcc_std_7": (mfcc_std[7], np.float32),
                    "mfcc_std_8": (mfcc_std[8], np.float32),
                    "mfcc_std_9": (mfcc_std[9], np.float32),
                    "mfcc_std_10": (mfcc_std[10], np.float32),
                    "mfcc_std_11": (mfcc_std[11], np.float32),
                    "spectral_centroid": (spectral_centroid_value, np.float32),
                    "spectral_rolloff": (spectral_rolloff_value, np.float32),
                    "zero_crossing_rate": (zero_crossing_rate_value, np.float32),
                    "chroma_0": (chroma_mean[0], np.float32),
                    "chroma_1": (chroma_mean[1], np.float32),
                    "chroma_2": (chroma_mean[2], np.float32),
                    "chroma_3": (chroma_mean[3], np.float32),
                    "chroma_4": (chroma_mean[4], np.float32),
                    "chroma_5": (chroma_mean[5], np.float32),
                    "chroma_6": (chroma_mean[6], np.float32),
                    "chroma_7": (chroma_mean[7], np.float32),
                    "chroma_8": (chroma_mean[8], np.float32),
                    "chroma_9": (chroma_mean[9], np.float32),
                    "chroma_10": (chroma_mean[10], np.float32),
                    "chroma_11": (chroma_mean[11], np.float32),
                    "spectral_contrast": (spectral_contrast_value, np.float32),
                    "spectral_bandwidth": (spectral_bandwidth_value, np.float32),
                    "spectral_flatness": (spectral_flatness_value, np.float32),
                    "energy": (energy, np.float32),
                    "rms": (rms, np.float32),
                    "rms_std": (rms_std, np.float32),
                    "rms_max": (rms_max, np.float32),
                    "rms_min": (rms_min, np.float32),
                    "hnr": (hnr, np.float32),
                    "genre": directory.split('/')[-1]
                }
                features_list.append(features)
                i += 1

    return features_list


def save_features_to_csv():
    features_data_to_save = extract_features()
    df = pd.DataFrame([{key: value[0] for key, value in feature.items()} for feature in features_data_to_save])

    if df.isnull().values.any():
        print("Warning: Data contains NaN values. Please check your features extraction.")
    else:
        df.to_csv('../src/data.csv', index=False)
        print("Features successfully saved to data.csv")


if __name__ == '__main__':
    save_features_to_csv()
