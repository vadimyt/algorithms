from Hero import Hero

def main():
    Warrior = Hero(100,40,15)
    Enemy = Hero(50,30,10)
    Warrior.punch(Enemy)
    print(Enemy.health)
    pass

if __name__ == '__main__':
    main()