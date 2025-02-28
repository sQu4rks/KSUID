import datetime
import os
import sys
import time

from functools import total_ordering

from .base62 import decodebytes, encodebytes
from .utils import int_from_bytes, int_to_bytes

# Used instead of zero(January 1, 1970), so that the lifespan of KSUIDs
# will be considerably longer
EPOCH_TIME = 1400000000

TIME_STAMP_LENGTH = 4  # number  bytes storing the timestamp
BODY_LENGTH = 16  # Number of bytes consisting of the UUID

@total_ordering
class ksuid():
    """ The primary classes that encompasses ksuid functionality.
    When given optional timestamp argument, the ksuid will be generated
    with the given timestamp. Else the current time is used.
    """

    def __init__(self, timestamp=None):
        payload = os.urandom(BODY_LENGTH)  # generates the payload
        if timestamp is None:
            currTime = int(time.time())
        else:
            currTime = timestamp
        # Note, this code may throw an overflow exception, far into the future
        byteEncoding = int_to_bytes(int(currTime - EPOCH_TIME), 4,  "big")

        self.__uid = list(byteEncoding) + list(payload)

    def getDatetime(self):
        """ getDatetime() returns a python date object which represents the approximate time
        that the ksuid was created """

        unixTime = self.getTimestamp()
        return datetime.datetime.fromtimestamp(unixTime)

    def getTimestamp(self):
        """ Returns the value of the timestamp, as a unix timestamp"""

        unixTime = int_from_bytes(
            self.__uid[:TIME_STAMP_LENGTH], byteorder="big")
        return unixTime + EPOCH_TIME

    # Returns the payload without the unix timestamp
    def getPayload(self):
        """ Returns the value of the payload, with the timestamp encoded portion removed
        Returns:
             list : An array of integers, that represent the bytes used to encode the UID """

        return self.__uid[TIME_STAMP_LENGTH:]

    def bytes(self):
        """ Returns the UID as raw bytes """

        if sys.version_info[0] >= 3:
            return bytes(self.__uid)

        return bytes("".join(self.__uid))

    def toBytes(self):
        return self.bytes()

    @staticmethod
    def fromBytes(value):
        """initializes KSUID from bytes"""
        if len(value) != TIME_STAMP_LENGTH + BODY_LENGTH:
            raise Exception("Wrong bytearray length")

        res = ksuid()
        res.__uid = value
        return res

    def toBase62(self):
        """ encodes KSUID with Base62 encoding """
        return encodebytes(self.bytes())

    @staticmethod
    def fromBase62(data):
        """ decodes KSUID from base62 encoding """
        v = decodebytes(data)
        return ksuid.fromBytes(v)

    def __lt__(self, other) -> bool:
        """ Compare two ksuids based on the timestamp.
        
        Note that the timestamps need to be at least one
        second appart from each other to satisfy a  x < y
        comparisson.

        This adds the ability to get a k-sorted list using
        the standard libraries sorted() function instead 
        of a helper function.
        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"'<' not supported between instances of '{self.__class__}' and '{other.__class__}'")
        
        return self.getTimestamp() < other.getTimestamp()

    def __eq__(self, other):
        """Check if the "other" object is the same as this object."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"'=' not supported between instances of '{self.__class__}' and '{other.__class__}'")
        
        return self.getTimestamp() == other.getTimestamp() and self.getPayload() == other.getPayload()

    def __hash__(self):
        key_list = [b for b in self.getPayload()]
        key_list.insert(0, self.getTimestamp())

        key_tuple = tuple(key_list)
        return hash(key_tuple)

    def __str__(self):
        """ Creates a string representation of the Ksuid from the  bytelist """
        if sys.version_info[0] >= 3:
            return "".join(list(map(lambda x: format(x, "02x"), self.__uid)))

        return "".join(x.encode("hex") for x in self.__uid)
