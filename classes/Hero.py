class Hero(object):
    def __init__(self, name, health , damage, armour):
        self.name = name
        self.health = health
        self.damage = damage
        self.armour = armour        

    def punch(self, enemy):
        enemy.armour = enemy.armour - self.damage
        if enemy.armour<0:
            enemy.health = enemy.health + enemy.armour
            enemy.armour = 0