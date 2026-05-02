import random


def update_reservoir_sample(sample, new_record, n_seen, k=5):
    """
    Update a reservoir sample with one new streaming record.

    Parameters
    ----------
    sample : list
        Current reservoir sample.

    new_record : dict
        New streaming record.

    n_seen : int
        Number of records seen so far.

    k : int
        Maximum sample size.

    Returns
    -------
    list
        Updated reservoir sample.
    """

    if len(sample) < k:
        sample.append(new_record)
    else:
        j = random.randint(1, n_seen)

        if j <= k:
            replace_index = random.randint(0, k - 1)
            sample[replace_index] = new_record

    return sample