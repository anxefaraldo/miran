def golden_ration(number, duration):
    new = number / 1.618
    print int((duration-new) / 60), ':', int((duration-new) % 60)
    return new


def gr2(number):
    new = number * 1.618
    print int(new / 60), ':', int(new % 60)
    return new
