from collections import Counter
from dateutil.parser import parse
import json


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
    # TODO: Optimize + Caching
    data_counter = dict(Counter([f[field] if not is_datetype
                                 else parse(f[field]).year for f in records]))
    return sorted([{key: data_counter[key]} for key in data_counter])


def get_big_number(records, field, aggregate):
 
    if aggregate == "Count":
    	result = len(records)
    if aggregate == "Sum":
    	result = sum([float(f[field]) for f in records])
    if aggregate == "Min":
    	result = min([f[field] for f in records])
    if aggregate == "Max":
    	result = max([f[field] for f in records])

    print(result)
    return result
