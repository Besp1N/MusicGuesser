import os
import librosa
import numpy as np
from librosa.beat import beat_track
from librosa.feature import chroma_cens, mfcc, spectral_centroid, zero_crossing_rate, spectral_contrast
import dir_paths


def extract_features() -> np.ndarray:
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
                energy = np.sum(librosa.feature.rms(y=y)**2)
                rms = np.mean(librosa.feature.rms(y=y))

                features = {
                    "filename": filename,
                    "tempo": tempo,
                    "mfcc": mfcc_mean,
                    "spectral_centroid": spectral_centroid_value,
                    "zero_crossing_rate": zero_crossing_rate_value,
                    "chroma": chroma_mean,
                    "spectral_contrast": spectral_contrast_value,
                    "energy": energy,
                    "rms": rms,
                    "genre": directory.split('/')[-1]
                }
                features_list.append(features)
                i += 1

    return np.array(features_list)


if __name__ == '__main__':
    features_data = extract_features()
    print(features_data)
