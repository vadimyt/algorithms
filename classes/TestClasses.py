import random
import time
from Hero import Hero

def main():
    Warrior = Hero("Воин А", 100, 40, 15)
    Enemy = Hero("Бандит B", 100, 30, 40)
    i=1
    while Warrior.health>0 and Enemy.health>0:
        print("Ход " + str(i))
        i+=1
        if random.randint(0,1)==0:
            fight(Warrior,Enemy)
        else:
            fight(Enemy,Warrior)
    if Warrior.health>0:
        print("Победил " + Warrior.name)
    else:
        print("Победил " + Enemy.name)
    pass

def fight(a,b):
    print(a.name + " атакует " + b.name)
    d20=random.randint(1,20)
    time.sleep(0.05)
    if d20==1:
        print("\033[31m{}".format("Критический промах по "+ b.name +"!")+"\033[37m")
    else: 
        if d20==20:
            print("\033[31m{}".format("Критический удар по "+ b.name +"!")+"\033[37m")
            a.damage*=2
            a.punch(b)
            a.damage/=2
        else:
            a.punch(b)
    print("У " + b.name + " осталось " + str(b.armour) + " брони и " + str(b.health) + " хп" + "\n")
                        

if __name__ == '__main__':
    main()