import time
import pygame
import random
import threading

class Character(pygame.sprite.Sprite):
    def __init__(self, name, health , damage, armour, position, animation_list, idle, side):
        self.name = name
        self.health = health
        self.damage = damage
        self.armour = armour
        self.animation_list = animation_list
        self.idle = idle
        pygame.sprite.Sprite.__init__(self)
        self.death = pygame.image.load('classes/Interface/death.png')
        if side==0:
            self.image = pygame.transform.flip(pygame.image.load(self.idle), True, False)
        else:
            self.image = pygame.image.load(self.idle)
        self.rect = self.image.get_rect()
        self.rect.topleft = (position)

    def destroy(self):
        self.kill()
    def punch(self, enemy):
        enemy.armour = enemy.armour - self.damage
        if enemy.armour<0:
            enemy.health = enemy.health + enemy.armour
            enemy.armour = 0

class Screen_devider(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((360, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,100)

class HealthSprite(pygame.sprite.Sprite):
    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('classes/Interface/health.png')
        self.rect = self.image.get_rect()
        if side==0:
            self.rect.topleft = (0,110)
        else:
            self.rect.topleft = (210,110)

class ArmourSprite(pygame.sprite.Sprite):
    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('classes/Interface/armour.png')
        self.rect = self.image.get_rect()
        if side==0:
            self.rect.topleft = (50,110)
        else:
            self.rect.topleft = (260,110)

class DamageSprite(pygame.sprite.Sprite):
    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('classes/Interface/damage.png')
        self.rect = self.image.get_rect()
        if side==0:
            self.rect.topleft = (100,110)
        else:
            self.rect.topleft = (310,110)

WIDTH = 360  # ширина игрового окна
HEIGHT = 210 # высота игрового окна
FPS = 60 # частота кадров в секунду
BLACK = (0, 0, 0)   
WHITE = (255, 255, 255) 
all_sprites = pygame.sprite.Group()

hero_animation_steps=4
hero_animation_cooldown=75

enemy_animation_steps=4
enemy_animation_cooldown=75
move_animation_cooldown=10
fight_cooldown=600

hero_character='Thief'
enemy_character='Knight'

def main():
    pygame.init()

    pygame.mixer.music.load('classes/Audio/N21_-_peripleumonicis.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    last_update=pygame.time.get_ticks()
    frame=0  

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()    

    base_font=pygame.font.Font(None,28)
    user_text=''
    name_text='Введите имя персонажа:'    
    input_rect=pygame.Rect(255,140,140,32)
    color_active=pygame.Color('lightskyblue3')
    color_passive=pygame.Color('grey15')
    color=color_passive
    user_text_active=False
    start_screen_active=True

    sceen_devider=Screen_devider()
    all_sprites.add(sceen_devider)

    animateHero=False
    animateEnemy=False
    moveEnemy=False
    moveHero=False
    fightOver=False
    hero_turn=False
    enemy_turn=False  
    pause_game=False
    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    user_text_active=True
                else:
                    user_text_active=False
            if event.type==pygame.KEYDOWN:
                if start_screen_active==True:
                    if user_text_active==True:
                        match event.key:
                            case pygame.K_BACKSPACE:
                                user_text=user_text[:-1]
                            case pygame.K_RETURN:
                                hero=createCharacter(hero_character,0,user_text)
                                enemy=createCharacter(enemy_character,1)
                                hero_healthsprite=HealthSprite(0)
                                hero_armoursprite=ArmourSprite(0)
                                hero_damagesprite=DamageSprite(0)
                                all_sprites.add(hero_healthsprite)
                                all_sprites.add(hero_armoursprite)
                                all_sprites.add(hero_damagesprite)

                                enemy_healthsprite=HealthSprite(1)
                                enemy_armoursprite=ArmourSprite(1)
                                enemy_damagesprite=DamageSprite(1)
                                all_sprites.add(enemy_healthsprite)
                                all_sprites.add(enemy_armoursprite)
                                all_sprites.add(enemy_damagesprite)
                                start_screen_active=False
                            case _:
                                user_text+=event.unicode
                else:
                    if fightOver==False:
                        if event.key==pygame.K_SPACE and animateHero==False and moveHero==False and enemy_turn==False:
                            #animateHero=True
                            #moveHero=True
                            hero_turn=True
                        if event.key==pygame.K_RETURN:
                            #animateEnemy=True
                            #moveEnemy=True
                            hero_turn=False
                            enemy_turn=False
                        if event.key==pygame.K_BACKSPACE:
                            if pause_game==False:
                                pause_game=True
                            else:
                                pause_game=False
                    if event.key==pygame.K_r:
                        hero_turn=False
                        enemy_turn=False
                        animateHero=False
                        animateEnemy=False
                        moveHero=False
                        moveEnemy=False
                        fightOver=False
                        hero.destroy()
                        enemy.destroy()
                        hero=createCharacter(hero_character,0,user_text)
                        enemy=createCharacter(enemy_character,1)
                        hero_healthsprite=HealthSprite(0)
                        hero_armoursprite=ArmourSprite(0)
                        hero_damagesprite=DamageSprite(0)
                        all_sprites.add(hero_healthsprite)
                        all_sprites.add(hero_armoursprite)
                        all_sprites.add(hero_damagesprite)

                        enemy_healthsprite=HealthSprite(1)
                        enemy_armoursprite=ArmourSprite(1)
                        enemy_damagesprite=DamageSprite(1)
                        all_sprites.add(enemy_healthsprite)
                        all_sprites.add(enemy_armoursprite)
                        all_sprites.add(enemy_damagesprite)

        all_sprites.update()
        screen.fill(WHITE)
        all_sprites.draw(screen)

        if user_text_active:
            color=color_active
        else:
            color=color_passive
        
        if start_screen_active:
            pygame.draw.rect(screen,color,input_rect,2)
            user_text_surface=base_font.render(user_text,True,(BLACK))
            name_text_surface=base_font.render(name_text,True,(BLACK))
            screen.blit(user_text_surface,(input_rect.x + 5, input_rect.y + 5))
            screen.blit(name_text_surface,(input_rect.x - 250, input_rect.y + 5))
            input_rect.w=max(100,user_text_surface.get_width()+10)
        else:
            if pause_game==False:
                current_time=pygame.time.get_ticks()
            if current_time - last_update >= fight_cooldown:
                last_update = current_time
                if hero_turn and fightOver!=True:
                    enemy_turn=True
                    hero_turn=False
                    animateHero=True
                    moveHero=True
                else:
                    if enemy_turn and fightOver!=True:
                        enemy_turn=False
                        hero_turn=True
                        animateEnemy=True
                        moveEnemy=True
            if (hero.health<=0):
                fightOver=True
                hero.image = pygame.transform.flip(hero.death, True, False)
                all_sprites.remove(hero_healthsprite)
                all_sprites.remove(hero_armoursprite)
                all_sprites.remove(hero_damagesprite)                                
            else:
                hero_health_text=str(hero.health)
                hero_armour_text=str(hero.armour)
                hero_damage_text=str(hero.damage)
                hero_health_text_surface=base_font.render(hero_health_text,True,(BLACK))
                screen.blit(hero_health_text_surface,(0, 160))
                hero_armour_text_surface=base_font.render(hero_armour_text,True,(BLACK))
                screen.blit(hero_armour_text_surface,(50, 160))
                hero_damage_text_surface=base_font.render(hero_damage_text,True,(BLACK))
                screen.blit(hero_damage_text_surface,(100, 160))
                if (moveHero):
                    if current_time - last_update >= move_animation_cooldown:
                        last_update = current_time
                        if animateHero==False:
                            hero.rect.x -=10
                            if hero.rect.x<=0:
                                moveHero=False
                        else:
                            hero.rect.x +=10
                            if hero.rect.x>=190:
                                moveHero=False
                if (animateHero):                
                    if current_time - last_update >= hero_animation_cooldown:
                        frame += 1
                        last_update = current_time
                        if frame >= len(hero.animation_list):
                            frame=0
                            animateHero=False
                            moveHero=True
                            hero.punch(enemy)
                        hero.image = pygame.transform.flip(hero.animation_list[frame], True, False)
            if (enemy.health<=0):
                fightOver=True
                enemy.image = enemy.death
                all_sprites.remove(enemy_healthsprite)
                all_sprites.remove(enemy_armoursprite)
                all_sprites.remove(enemy_damagesprite) 
            else:
                enemy_health_text=str(enemy.health)
                enemy_armour_text=str(enemy.armour)
                enemy_damage_text=str(enemy.damage)            
                enemy_health_text_surface=base_font.render(enemy_health_text,True,(BLACK))
                screen.blit(enemy_health_text_surface,(210, 160))
                enemy_armour_text_surface=base_font.render(enemy_armour_text,True,(BLACK))
                screen.blit(enemy_armour_text_surface,(260, 160))
                enemy_damage_text_surface=base_font.render(enemy_damage_text,True,(BLACK))
                screen.blit(enemy_damage_text_surface,(310, 160)) 
                if (moveEnemy):
                    if current_time - last_update >= move_animation_cooldown:
                        last_update = current_time
                        if animateEnemy==False:
                            enemy.rect.x +=10
                            if enemy.rect.x>=260:
                                moveEnemy=False
                        else:
                            enemy.rect.x -=10
                            if enemy.rect.x<=80:
                                moveEnemy=False
                if (animateEnemy):
                    if current_time - last_update >= enemy_animation_cooldown:
                        frame += 1
                        last_update = current_time
                        if frame >= len(enemy.animation_list):
                            frame=0
                            animateEnemy=False
                            moveEnemy=True
                            enemy.punch(hero)
                        enemy.image = enemy.animation_list[frame]

        pygame.display.flip()
    pygame.quit()

def createCharacter(character_class, side, user_text='none'):
    if user_text=='none':
        user_text=character_class
    animation_list=[]
    idle='classes/'+character_class+'Sprites/'+character_class+'1.png'
    for i in range(1,4):
        animation_list.append(pygame.image.load('classes/'+character_class+'Sprites/'+character_class+str(i)+'.png'))
    if side==0:
        hero=Character(user_text, 50, 30, 15, (0,0), animation_list, idle,side)
        all_sprites.add(hero)
        return hero
    else:
        enemy=Character(user_text, 200, 10, 20, (260,0), animation_list, idle,side)
        all_sprites.add(enemy)
        return enemy 

if __name__ == '__main__':
    main()