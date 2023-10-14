import os
import time
import pygame
import random
import threading

WIDTH = 360  # ширина игрового окна
HEIGHT = 360 # высота игрового окна
FPS = 60 # частота кадров в секунду
BLACK = (0, 0, 0)   
WHITE = (255, 255, 255) 
all_sprites = pygame.sprite.Group()

move_animation_cooldown=10
death_animation_cooldown=500

fight_cooldown=600

miss_text='Промах!'
crit_text='Крит!'

battle_text_pos=((140,10))

default_sound_volume=0.2
default_music_volume=0.2
default_attacksound_volume=0.1

character_list=['Knight', 'Thief']

default_y=60
default_x=0

class Character(pygame.sprite.Sprite):
    def __init__(self, name, position, sound_list, animation_list, idle, side, need_move=False, health=100 , damage=20, armour=15, level=1):
        self.name = name
        self.health = health
        self.damage = damage
        self.armour = armour
        self.sound_list = sound_list
        self.animation_list = animation_list        
        self.idle = idle
        self.level = level
        self.side = side
        self.need_move=need_move
        self.animation_cooldown=300/len(animation_list)
        pygame.sprite.Sprite.__init__(self)
        self.death_animation_list = [pygame.image.load('classes/Interface/death1.png'),
                                     pygame.image.load('classes/Interface/death2.png')]
        if self.side==0:
            self.image = pygame.transform.flip(pygame.image.load(self.idle), True, False)
        else:
            self.image = pygame.image.load(self.idle)
        self.rect = self.image.get_rect()
        self.rect.topleft = (position)

    def destroy(self):
        self.kill()
        self.__del__()

    def __del__(self):
        pass

    def SetRandomStats(self):
        self.health=random.randint(0+50*self.level,100+50*self.level)
        self.damage=random.randint(0+50*self.level,100+50*self.level)
        self.armour=random.randint(0+50*self.level,100+50*self.level)

    def punch(self, enemy):        
        enemy.armour = enemy.armour - self.damage
        if enemy.armour<0:
            enemy.health = enemy.health + enemy.armour
            enemy.armour = 0
        if enemy.health <=0:
            if enemy.side==0:
                enemy.image = pygame.transform.flip(enemy.death_animation_list[0], True, False)
            else:
                enemy.image = enemy.death_animation_list[0]

    def Throw_d20(self, enemy):
        d20=random.randint(1,20)
        if d20==1:
            return d20
        else: 
            if d20==20:
                self.damage*=2
                self.punch(enemy)
                self.damage/=2
                return d20
            else:
                self.punch(enemy)
                return d20

class UI():
    class Text(pygame.sprite.Sprite):
        def __init__(self, text, position, color=BLACK, size=28):
            base_font=pygame.font.Font(None,size)
            pygame.sprite.Sprite.__init__(self)
            self.image=base_font.render(str(text),True,(color))
            self.rect=self.image.get_rect()
            self.rect.topleft=position            
        def destroy(self):
            self.kill()
            UI.__del__(self)
    class Screen_devider(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((360, 10))
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect.topleft = (default_x+0,default_y+100)
        def destroy(self):
            self.kill()
            UI.__del__(self)
    class HealthSprite(pygame.sprite.Sprite):
        def __init__(self, side):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('classes/Interface/health.png')
            self.rect = self.image.get_rect()            
            if side==0:
                self.rect.topleft = (default_x+0,default_y+110)
            else:
                self.rect.topleft = (default_x+210,default_y+110)
        def destroy(self):
            self.kill()
            UI.__del__(self)
        def __del__(self):
            pass
    class ArmourSprite(pygame.sprite.Sprite):
        def __init__(self, side):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('classes/Interface/armour.png')
            self.rect = self.image.get_rect()
            if side==0:
                self.rect.topleft = (default_x+50,default_y+110)
            else:
                self.rect.topleft = (default_x+260,default_y+110)
        def destroy(self):
            self.kill()
            UI.__del__(self)
    class DamageSprite(pygame.sprite.Sprite):
        def __init__(self, side):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('classes/Interface/damage.png')
            self.rect = self.image.get_rect()
            if side==0:
                self.rect.topleft = (default_x+100,default_y+110)
            else:
                self.rect.topleft = (default_x+310,default_y+110)
        def destroy(self):
            self.kill()
            UI.__del__(self)
    def __del__(self):
            pass
def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    music=['classes/Audio/music/N21_-_peripleumonicis.mp3','classes/Audio/music/N14_-_evil_mage_theme.mp3']
    curtrack=random.randint(0,len(music)-1)
    ha_sound = pygame.mixer.Sound('classes/Audio/sounds/ha.mp3')
    ha_sound.set_volume(default_sound_volume)
    pygame.mixer.music.load(music[curtrack])
    pygame.mixer.music.set_volume(default_music_volume)
    pygame.mixer.music.play(loops = -1, fade_ms=5000)

    last_update=pygame.time.get_ticks()
    frame=0  

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()    

    base_font=pygame.font.Font(None,28)
    user_text=''
    name_text='Введите имя персонажа:'    
    input_rect=pygame.Rect(255,140,140,32)
    input_rect.x+=default_x
    input_rect.y+=default_y
    color_active=pygame.Color('lightskyblue3')
    color_passive=pygame.Color('grey15')
    color=color_passive
    user_text_active=False
    start_screen_active=True

    sceen_devider=UI.Screen_devider()
    all_sprites.add(sceen_devider)

    animateHero=False
    animateEnemy=False
    moveEnemy=False
    moveHero=False
    fightOver=False
    hero_turn=False
    enemy_turn=False  
    pause_game=False
    music_pause=False
    
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
                if user_text_active==False or start_screen_active==False:
                    if event.key==pygame.K_m:
                            if music_pause==False:
                                music_pause=True
                                pygame.mixer.music.pause()
                            else:
                                music_pause=False
                                pygame.mixer.music.unpause()
                    if event.key==pygame.K_p:                        
                        if curtrack==(len(music)-1):
                            curtrack=0
                        else:
                            curtrack+=1
                        pygame.mixer.music.load(music[curtrack])
                        pygame.mixer.music.play(loops = -1, fade_ms=5000)
                if start_screen_active==True:
                    if user_text_active==True:
                        match event.key:
                            case pygame.K_BACKSPACE:
                                user_text=user_text[:-1]
                            case pygame.K_RETURN:
                                hero=createCharacter(0, random.randint(0,len(character_list)-1), user_text=user_text)
                                enemy=createCharacter(1, random.randint(0,len(character_list)-1))
                                hero_ui=[UI.HealthSprite(0),
                                         UI.ArmourSprite(0),
                                         UI.DamageSprite(0),
                                         UI.Text(hero.health,(default_x+0, default_y+160)),
                                         UI.Text(hero.armour,(default_x+50, default_y+160)),
                                         UI.Text(hero.damage,(default_x+100, default_y+160))]
                                all_sprites.add(hero_ui)

                                enemy_ui=[UI.HealthSprite(1),
                                          UI.ArmourSprite(1),
                                          UI.DamageSprite(1),
                                          UI.Text(enemy.health,(default_x+210, default_y+160)),
                                          UI.Text(enemy.armour,(default_x+260, default_y+160)),
                                          UI.Text(enemy.damage,(default_x+310, default_y+160))]  
                                all_sprites.add(enemy_ui)
                                start_screen_active=False
                            case _:
                                user_text+=event.unicode
                else:
                    if fightOver==False:
                        if event.key==pygame.K_SPACE and animateHero==False and moveHero==False and enemy_turn==False:
                            hero_turn=True
                        if event.key==pygame.K_RETURN:
                            hero_turn=False
                            enemy_turn=False
                        if event.key==pygame.K_BACKSPACE:
                            if pause_game==False:
                                pause_game=True                               
                            else:
                                pause_game=False
                                    
                    if event.key==pygame.K_r:
                        frame=0
                        hero_turn=False
                        enemy_turn=False
                        animateHero=False
                        animateEnemy=False
                        moveHero=False
                        moveEnemy=False
                        fightOver=False
                        hero.destroy()
                        enemy.destroy()
                        hero=createCharacter(0,random.randint(0,len(character_list)-1),user_text)
                        enemy=createCharacter(1,random.randint(0,len(character_list)-1))
                        for i in range(6):
                            hero_ui[i].destroy()
                            enemy_ui[i].destroy()
                        hero_ui=[UI.HealthSprite(0),
                                 UI.ArmourSprite(0),
                                 UI.DamageSprite(0),
                                 UI.Text(hero.health,(default_x+0, default_y+160)),
                                 UI.Text(hero.armour,(default_x+50, default_y+160)),
                                 UI.Text(hero.damage,(default_x+100, default_y+160))]
                        all_sprites.add(hero_ui)
                        enemy_ui=[UI.HealthSprite(1),
                                  UI.ArmourSprite(1),
                                  UI.DamageSprite(1),
                                  UI.Text(enemy.health,(default_x+210, default_y+160)),
                                  UI.Text(enemy.armour,(default_x+260, default_y+160)),
                                  UI.Text(enemy.damage,(default_x+310, default_y+160))] 
                        all_sprites.add(enemy_ui)                    

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
            if pause_game!=True:
                current_time=pygame.time.get_ticks()
            if current_time - last_update >= fight_cooldown:
                last_update = current_time
                if hero_turn and fightOver!=True:
                    try:
                        battle_text.kill()
                    except UnboundLocalError:
                        pass
                    enemy_turn=True
                    hero_turn=False
                    animateHero=True
                    moveHero=True
                else:
                    if enemy_turn and fightOver!=True:
                        try:
                            battle_text.kill()
                        except UnboundLocalError:
                            pass
                        enemy_turn=False
                        hero_turn=True
                        animateEnemy=True
                        moveEnemy=True
            if (hero.health<=0):
                fightOver=True                
                if current_time - last_update >= death_animation_cooldown:
                    frame += 1
                    last_update = current_time
                    if frame >= len(hero.death_animation_list):
                        frame=0
                    hero.image = pygame.transform.flip(hero.death_animation_list[frame], True, False)
                    if frame==1:
                        ha_sound.play()                           
            else:
                if (moveHero and hero.need_move):
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
                else:
                    moveHero=False
                if (animateHero):                
                    if current_time - last_update >= hero.animation_cooldown:
                        if frame==0:
                            hero.sound_list[random.randint(0,len(hero.sound_list)-1)].play()
                        frame += 1
                        last_update = current_time
                        if frame >= len(hero.animation_list):
                            frame=0
                            animateHero=False
                            moveHero=True
                            d20=hero.Throw_d20(enemy)
                            text=''
                            if d20==1:
                                text=miss_text                                
                            elif d20==20:
                                text=crit_text
                            battle_text=UI.Text(text,battle_text_pos,(255,0,0),32)
                            all_sprites.add(battle_text)
                            for i in range(6):                            
                                    enemy_ui[i].destroy()
                            if enemy.health>0:                                
                                enemy_ui=[UI.HealthSprite(1),
                                    UI.ArmourSprite(1),
                                    UI.DamageSprite(1),
                                    UI.Text(enemy.health,(default_x+210, default_y+160)),
                                    UI.Text(enemy.armour,(default_x+260, default_y+160)),
                                    UI.Text(enemy.damage,(default_x+310, default_y+160))] 
                                all_sprites.add(enemy_ui)
                        hero.image = pygame.transform.flip(hero.animation_list[frame], True, False)
            if (enemy.health<=0):
                fightOver=True
                if current_time - last_update >= death_animation_cooldown:
                    frame += 1
                    last_update = current_time
                    if frame >= len(enemy.death_animation_list):
                        frame=0
                    enemy.image = enemy.death_animation_list[frame]
                    if frame==1:
                        ha_sound.play()
            else:                     
                if (moveEnemy and enemy.need_move):
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
                else:
                    moveEnemy=False
                if (animateEnemy):
                    if current_time - last_update >= enemy.animation_cooldown:
                        if frame==0:
                            enemy.sound_list[random.randint(0,len(enemy.sound_list)-1)].play()
                        frame += 1
                        last_update = current_time
                        if frame >= len(enemy.animation_list):
                            frame=0
                            animateEnemy=False
                            moveEnemy=True
                            d20=enemy.Throw_d20(hero)
                            text=''
                            if d20==1:
                                text=miss_text                                
                            elif d20==20:
                                text=crit_text
                            battle_text=UI.Text(text,battle_text_pos,(255,0,0),32)
                            all_sprites.add(battle_text)
                            for i in range(6):
                                    hero_ui[i].destroy()
                            if hero.health>0:
                                hero_ui=[UI.HealthSprite(0),
                                            UI.ArmourSprite(0),
                                            UI.DamageSprite(0),
                                            UI.Text(hero.health,(default_x+0, default_y+160)),
                                            UI.Text(hero.armour,(default_x+50, default_y+160)),
                                            UI.Text(hero.damage,(default_x+100, default_y+160))]
                                all_sprites.add(hero_ui)
                        enemy.image = enemy.animation_list[frame]

        pygame.display.flip()
    pygame.quit()

def createCharacter(side, character_int=99, user_text='none'):
    character_class=character_list[character_int]
    if user_text=='none':
        user_text=character_class
    animation_list=[]
    sound_list=[]    
    try:
        lst=os.listdir('classes/'+character_class+'Sprites/')
        for i in range(0,len(lst)):            
            if i==0:
                idle='classes/'+character_class+'Sprites/'+lst[i]                
            animation_list.append(pygame.image.load('classes/'+character_class+'Sprites/'+lst[i]))
    except FileNotFoundError:
        lst=os.listdir('classes/DefaultSprites/')
        for i in range(0,len(lst)):
            if i==0:
                idle='classes/DefaultSprites/'+lst[i]
            animation_list.append(pygame.image.load('classes/DefaultSprites/'+lst[i]))
    try:
        lst=os.listdir('classes/Audio/attacksounds/'+character_class+'SoundEffects/')
        for i in range(0,len(lst)):
            sound_list.append(pygame.mixer.Sound('classes/Audio/attacksounds/'+character_class+'SoundEffects/'+lst[i]))
            sound_list[i].set_volume(default_attacksound_volume)
    except FileNotFoundError:
        lst=os.listdir('classes/Audio/attacksounds/DefaultSoundEffects/')
        for i in range(0,len(lst)):
            sound_list.append(pygame.mixer.Sound('classes/Audio/attacksounds/DefaultSoundEffects/'+lst[i]))
            sound_list[i].set_volume(default_attacksound_volume)
    need_move=True
    if side==0:
        hero=Character(user_text, (default_x+0,default_y+0), sound_list, animation_list, idle, side, need_move)
        hero.SetRandomStats()
        all_sprites.add(hero)
        return hero
    else:
        enemy=Character(user_text, (default_x+260,default_y+0), sound_list, animation_list, idle, side, need_move)
        enemy.SetRandomStats()
        all_sprites.add(enemy)
        return enemy

if __name__ == '__main__':
    main()