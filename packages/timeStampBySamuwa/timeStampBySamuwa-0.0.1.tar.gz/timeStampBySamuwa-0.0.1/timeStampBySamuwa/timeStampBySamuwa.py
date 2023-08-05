def timeStamp():
    import datetime
    time = str(datetime.datetime.now())
    numbers = [str(x) for x in range(0,10)]
    string = ''
    for x in time:
        for y in x:
            if y in numbers:
                string += y
    return string


