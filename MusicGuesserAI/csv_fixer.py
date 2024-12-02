import pandas as pd


def update_genres():
    df = pd.read_csv('src/data.csv')

    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

    records_per_genre = 100

    for i, genre in enumerate(genres):
        start_index = i * records_per_genre
        end_index = start_index + records_per_genre
        df.loc[start_index:end_index - 1, 'genre'] = genre

    df.to_csv('src/data_updated.csv', index=False)


if __name__ == '__main__':
    update_genres()
