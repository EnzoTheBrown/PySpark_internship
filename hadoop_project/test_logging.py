import logging

logger = logging.getLogger('example')

# CRITICAL _ 50
# ERROR _ 40
# WARNING _ 30
# INFO _ 20
# DEBUG _ 10

format = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(format=format, level=logging.WARNING)

class Item(object):
    '''Base Item class'''

    def __init__(self, name, value):
        self.name = name
        self.value = value
        logger.debug("Item created: {}({})".format(self.name, self.value))

    def buy(self, quantity=1):
        '''Buys item'''
        logger.debug("Bought item {}".format(self.name))

    def sell(self, quantity=1):
        '''Sells item'''
        logger.warn("Sold item {}".format(self.name))

item_01 = Item('Sword', 150)
item_01.buy()
item_01.sell()