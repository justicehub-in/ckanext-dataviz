from collections import Counter
from dateutil.parser import parse


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except:
        return False


def get_bar_chart(records, field):
    is_datetype = is_date(records[0][field])

    # TODO: Allow users to decide operations on datetime fields
    data_counter = dict(Counter([str(f[field]) if not is_datetype
                                 else str(parse(f[field]).year) for f in records]))
    return [{key: data_counter[key]} for key in data_counter]
