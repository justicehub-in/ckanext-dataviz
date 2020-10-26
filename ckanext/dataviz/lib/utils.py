from collections import Counter


def get_bar_chart(records, field):
    data_counter = dict(Counter([str(f[field]) for f in records]))
    return [{key: data_counter[key]} for key in data_counter]
