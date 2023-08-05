from collections import Counter

def joke():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')

def shree():
    return ("HI SHREE")

def shivang():
    return "HI GUJJU"


def Count(x):
    dictionary = dict()
    array = list(x)
    countArray = dict(Counter(array))
    return countArray