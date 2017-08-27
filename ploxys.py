from random import randint
from collections import OrderedDict




# never let the children number get below zero
def nozero(inteiro):
    if inteiro > 0:
        return inteiro
    else:
        return 0
lista = []
def main(num_ploxys,num_foods,min_lifespan,max_lifespan):
    stringui = str(num_ploxys) + "," + str(num_foods) + "," + str(min_lifespan) + "," + str(max_lifespan)

    # here the ploxys are creates, each ploxy is a list holding its x, its y , how many roudns it will live, his birthdate and his generation and how many children it will give birth respectively
    ploxys = [[randint(1,900),randint(1,900),randint(min_lifespan,max_lifespan),randint(((-1) * (min_lifespan - 1)),0),0,randint(1,4)]   for i in range(0,num_ploxys)  ]




    # here the inital foods are create, each one is a list holding its position in x and y
    foods = [[randint(1,901),randint(1,901)] for i in range (0,num_foods)]

    conta = 0
    # the simulation starts
    while True:

        if len(ploxys) == 0 or len(ploxys) > 1000 or conta >= 10000:
            return conta
            break

        # each ploxy moves ramdomly from -5 to 5 pixels in each round, if the ploxy lifespan is over, the ploxy does not goes into the next round
        ploxys = [ [(ploxy[0] + randint(-5,5)) % 900 ,(ploxy[1] + randint(-5,5)) % 900,ploxy[2],ploxy[3], ploxy[4],ploxy[5]] for ploxy in ploxys if ploxy[2] + ploxy[3] > conta]



        # it chekcs if any food has been eaten, if it has, the food will be deleted
        for food in foods:
            eaten = False
            for ploxy in ploxys:
                if [ploxy[0],ploxy[1]] == food:
                    eaten = True
                    # the ploxy that ate the food, generates children and a new food is generated
                    for i in range(0,ploxy[5]):
                        ploxys.append([ploxy[0],ploxy[1],ploxy[2] + randint(-5,5),conta,ploxy[4] + 1,nozero(ploxy[5] + randint(-1,1))])
                    foods.append([randint(0,900),randint(0,900)])
                    break

            # if the food is eaten, it is removed
            if eaten ==  False:
                pass
            else:
                foods.remove(food)
        #if all the ploxs are dead, the population reached the 1000 limit or the round is 10000 it finishes the simulation and return how many rounds they survived
        if len(ploxys) == 0 or len(ploxys) > 1000 or conta >= 10000:
            return conta
            break
        conta += 1