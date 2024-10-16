import os
import dir_paths
import numpy as np


def extract_genres() -> np.ndarray:
    paths: dict[str, str] = dir_paths.get_dir_names()
    features_list = []

    for genre, directory in paths.items():
        for filename in os.listdir(directory):
            if filename.endswith('.wav'):
                features_list.append(genre)

    return np.array(features_list)


if __name__ == '__main__':
    features_data = extract_genres()
    print(features_data)