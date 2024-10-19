import os
import librosa
import numpy as np
import pandas as pd
from librosa.beat import beat_track
from librosa.feature import chroma_cens, mfcc, spectral_centroid, zero_crossing_rate, spectral_contrast, \
    spectral_bandwidth, spectral_flatness
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

                spectral_centroid_value = np.mean(spectral_centroid(y=y, sr=sr))
                zero_crossing_rate_value = np.mean(zero_crossing_rate(y))
                chroma = chroma_cens(y=y, sr=sr)
                chroma_mean = np.mean(chroma, axis=1)
                spectral_contrast_value = np.mean(spectral_contrast(y=y, sr=sr))
                spectral_bandwidth_value = np.mean(spectral_bandwidth(y=y, sr=sr))
                spectral_flatness_value = np.mean(spectral_flatness(y=y))
                energy = np.sum(librosa.feature.rms(y=y) ** 2)
                rms = np.mean(librosa.feature.rms(y=y))

                features = {
                    "tempo": tempo,
                    "mfcc_0": mfcc_mean[0],
                    "mfcc_1": mfcc_mean[1],
                    "mfcc_2": mfcc_mean[2],
                    "mfcc_3": mfcc_mean[3],
                    "mfcc_4": mfcc_mean[4],
                    "mfcc_5": mfcc_mean[5],
                    "mfcc_6": mfcc_mean[6],
                    "mfcc_7": mfcc_mean[7],
                    "mfcc_8": mfcc_mean[8],
                    "mfcc_9": mfcc_mean[9],
                    "mfcc_10": mfcc_mean[10],
                    "mfcc_11": mfcc_mean[11],
                    "mfcc_12": mfcc_mean[12],
                    "spectral_centroid": spectral_centroid_value,
                    "zero_crossing_rate": zero_crossing_rate_value,
                    "chroma_0": chroma_mean[0],
                    "chroma_1": chroma_mean[1],
                    "chroma_2": chroma_mean[2],
                    "chroma_3": chroma_mean[3],
                    "chroma_4": chroma_mean[4],
                    "chroma_5": chroma_mean[5],
                    "chroma_6": chroma_mean[6],
                    "chroma_7": chroma_mean[7],
                    "chroma_8": chroma_mean[8],
                    "chroma_9": chroma_mean[9],
                    "chroma_10": chroma_mean[10],
                    "chroma_11": chroma_mean[11],
                    "spectral_contrast": spectral_contrast_value,
                    "spectral_bandwidth": spectral_bandwidth_value,
                    "spectral_flatness": spectral_flatness_value,
                    "energy": energy,
                    "rms": rms,
                    "genre": directory.split('/')[-1]
                }
                features_list.append(features)
                i += 1

    return features_list


def save_features_to_csv():
    features_data_to_save = extract_features()
    df = pd.DataFrame(features_data_to_save)

    if df.isnull().values.any():
        print("Warning: Data contains NaN values. Please check your features extraction.")
    else:
        df.to_csv('../src/data.csv', index=False)
        print("Features successfully saved to data.csv")


if __name__ == '__main__':
    save_features_to_csv()
