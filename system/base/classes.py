__author__ = 'andrew.sielen'

import collections


###
# Simple classes that don't deserve their own file
###

class OrderedDictV2(collections.OrderedDict):
    """
    Like a normal ordered dict, but with a couple useful functions
    - next_key(key), returns the next key in the dict
    - previous_key(key), returns the previous key in the dict
    - first key(key), returns the first key in the dict
    """

    def next_key(self, key):
        next = self._OrderedDict__map[key].next
        if next is self._OrderedDict__root:
            raise ValueError("{!r} is the last key".format(key))
        return next.key

    def previous_key(self, key):
        previous = self._OrderedDict__map[key].prev
        return previous.key

    def first_key(self):
        for key in self: return key
        raise ValueError("OrderedDict() is empty")