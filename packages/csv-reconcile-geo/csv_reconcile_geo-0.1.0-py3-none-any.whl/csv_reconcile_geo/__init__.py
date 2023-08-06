__version__ = '0.1.0'

from csv_reconcile import scorer
from geopy import distance
from math import pi, atan, log


# [[https://en.wikipedia.org/wiki/Sigmoid_function]]
def scaleScore(dist):
    '''
    Scaling function so that distances from 0 -> inf get mapped to 100% -> 0%
    Uses atan() as a sigmoid function and log(1/dist) to convert from 0 -> inf to inf -> -inf.

    Since log(1/dist) is strictly descreasing and atan(x+K) is strictly increasing (i.e. order
    preserving), this scaling function is strictly decreasing and inversely preserves the ordering
    of the distances.

    I.e. The closer the distance is to zero the higher the score.
    '''
    scale = 10  # km at which score is 50%
    return (atan(log(scale / dist)) + pi / 2) / pi * 100


@scorer.register
def getNormalizedFields():
    return ('lat', 'long')


@scorer.register
def scoreMatch(left, right):
    dist = distance.geodesic(left, right).km
    # report max straight off to avoid division by zeron in scaling function
    if dist == 0.0:
        return 100.0

    # Normalize so 0 -> 100% and big number -> 0%
    # FIX ME - Add a scaling factor to control how fast the decay happens.
    return scaleScore(dist)


@scorer.register
def normalizeWord(word, **scoreOptions):
    originalWord = word
    typ = None

    if '^^' in word:
        word, typ = word.split('^^', 1)
        # FIX ME - Check type against valid wktLiteral types??

    # Remove quotes if there for casting to type
    if word[0] == word[-1] == '"':
        word = word[1:-1]

    if not (word.lower()[:6] == 'point(' and word[-1] == ')'):
        raise RuntimeError('Expected wktLiteral POINT value.  Got "%s"',
                           originalWord)

    return tuple(float(x) for x in word[6:-1].split(None, 1))
