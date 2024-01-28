class Quotes:

    open             = 0.0
    high             = 0.0
    low              = 0.0
    close            = 0.0


    def __init__(self,open,high,low,close) -> None:
        self.open   = open
        self.high   = high
        self.low    = low
        self.close  = close

    def print(self):
        print(f'{self.date}:{self.open}-{self.high}-{self.low}-{self.close}')

