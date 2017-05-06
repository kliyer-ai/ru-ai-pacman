#Samarpan Rai: s4753763
#Nick Stracke: s4771192

"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    bestShop = fruitShops[0]
    for currentShop in fruitShops[1:]:
        if currentShop.getPriceOfOrder(orderList) < bestShop.getPriceOfOrder(orderList):
            bestShop = currentShop
    return bestShop

fruits1 = {'apples': 2.0, 'oranges':1.0}
fruits2 = {'apples': 1.0, 'oranges': 5.0}
shop1 =  shop.FruitShop('shop1',fruits1)
shop2 = shop.FruitShop('shop2',fruits2)
shops = [shop1, shop2]
orders1 = [('apples',1.0), ('oranges',3.0)]
orders2 = [('apples',3.0)]
print("For order", orders1, "the best shop is", shopSmart(orders1, shops).getName())
print("For order", orders2, "the best shop is", shopSmart(orders2, shops).getName())
