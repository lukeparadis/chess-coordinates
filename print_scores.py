import pickle

if __name__ == '__main__':

    filename = 'data/scores.pkl'

    with open(filename, 'rb') as fh:
        stats = pickle.load(fh)

    squares = sorted(list(stats[True].keys()))

    for square in squares:
    
        if stats[False][square]['attempts'] > 0:
            rate = stats[False][square]['correct'] / stats[False][square]['attempts']
        else:
            rate = 0
        if stats[True][square]['attempts'] > 0:
            rate_flipped = stats[True][square]['correct'] / stats[True][square]['attempts']
        else:
            rate_flipped = 0
    
        print('{:5}{:6.2f}{:6.2f}'.format(square, rate, rate_flipped))
