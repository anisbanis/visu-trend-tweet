def progress_bar(iterator, length=None, *args, **kwargs):
    if ((not hasattr(iterator, '__next__')) and
        (not hasattr(iterator, '__iter__'))):
        raise TypeError('The argument you supplied is neither an iterator'
                        'nor an iterable.')

    if hasattr(iterator, '__len__'):
        length = len(iterator)
    elif length is None:
        raise ValueError('Could not inver total length of the iterator.')

    _print_progress_bar(0, length, *args, **kwargs)
    for i, _ in enumerate(iterator):
        _print_progress_bar(i+1, length, *args, **kwargs)

    return

def _print_progress_bar(progress, iter_length,
                 decimals = 1, bar_length = 100,
                 prefix = '',
                 filler = '█',
                 empty_char  = ' ',
                 suffix = '',
                 trailing_char = '\r'):
    progress_value = f'{{0:.{decimals}f}}'.format(100 * progress / float(iter_length))
    completed_len = (bar_length * progress // iter_length)
    bar = filler * completed_len + empty_char * (bar_length - completed_len)
    print(f'\r{prefix} {bar} {suffix} {progress_value}%', end=trailing_char)

if __name__ == '__main__':
    from time import sleep
    n = 55
    progress_bar(map(lambda _: sleep(.1), range(n)), n,
                 prefix='Progress : ',
                 suffix='Completed : ',
                 empty_char='-')
