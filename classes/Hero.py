class Hero(object):
    def __init__(self, health , damage, armour):
        self.health = health
        self.damage = damage
        self.armour = armour

    def punch(self, enemy):
        enemy.health = enemy.health-self.damage