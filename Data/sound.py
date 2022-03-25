import winsound

def makeNoice(frequency = 2500, duration = 1000):
    winsound.Beep(frequency, duration)