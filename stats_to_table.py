import pickle
import common
import pandas as pd

if __name__ == '__main__':

    filename = common.STATS_FILENAME

    with open(filename, 'rb') as fh:
        stats = pickle.load(fh)

    squares = sorted(list(stats['white'].keys()))

    rows = []

    for square in squares:
        for side in ('white','black'):
        
            row = [
                square,
                side,
                stats[side][square]['correct'],
                stats[side][square]['total'],
            ]

            rows.append(row)

    df = pd.DataFrame(rows, columns=['square', 'side', 'correct', 'total' ] )
    df.set_index(['square','side'], inplace=True)

    df['accuracy'] = df['correct'] / df['total']

