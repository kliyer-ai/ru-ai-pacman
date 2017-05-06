#Samarpan Rai: s4753763
#Nick Stracke: s4771192

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75,
               'limes': 0.75, 'strawberries': 1.00}


def buyLotsOfFruit(orderList):

    totalCost = 0;
    for name,quantity in orderList:

        if quantity < 0:
            print('Wrong quantity of' ,name,':', quantity)
        elif name not in fruitPrices:
            print(name ,'not in list')
        else:
            perFruitPrice = fruitPrices[name]
            totalCost = totalCost + quantity * perFruitPrice

    return totalCost


orderList = [('apples', 2), ('pears', 3), ('limes', 4), ('apples', -10), ('pineapple', 10)]
print('Cost of', orderList, 'is', buyLotsOfFruit(orderList))
