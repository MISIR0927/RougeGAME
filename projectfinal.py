
#Import the pygame module
from math import sqrt
import pygame, time, random,sys,math
import numpy as np
from pygame.sprite import Sprite
from pygame.math import Vector2
import time




SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_SIZE =(SCREEN_WIDTH,SCREEN_HEIGHT)
background_image = pygame.image.load('img/fightingplace.png')
background_image = pygame.transform.scale(background_image, SCREEN_SIZE)
BG_COLOR = pygame.Color(0,255,0)
TEXT_COLOR = pygame.Color(255,0,0)
monster_img1 = pygame.image.load("img/enemy1L.gif")
monster_img2 = pygame.image.load("img/enemy1R.gif")
reload_interval = 1000
shoot_interval = 500
last_shot_time = 0
last_creat_time = 0
object_x = random.randint(100,200)
object_y = random.randint(100,600)
pygame.mixer.init()
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
game_pause = False
selection = False




# 定义地图矩阵
maps = [
    {
        'map1': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            
        ],
    },
     {
        'map2': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    },
     {
        'map3': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ],
    },
    {
        'map4': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    },
     {
        'map5': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    }
]

tile_size = 60

#Define a base class
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


class Maingame():
    window=None
    my_Character=None

    enemyList = []
    boommonsterlist = []
    enemyCount = 3
    myBulletList= []
    enemyBulletList = []
    explodeList = []
    wallList = []
    mySkillList = []
    roomlist=[]
    bufflist=[]
    
    tokens=[]
    
    
    img_0 = 'img/0_0.png'
    img_1 = 'img/0_1.png'
    img_2 = 'img/0_2.png'
    img_3 = 'img/0_3.png'
    img_4 = 'img/0_4.png'
    img_5 = 'img/0_5.png'
    imgw = 'img/z_6.png'
    imgwall = 'img/steels.gif'
    mimg_0 = 'img/e0_0.png'
    mimg_1 = 'img/e0_1.png'
    mimg_2 = 'img/e0_2.png'
    mimg_3 = 'img/e0_3.png'
    mimg_4 = 'img/e0_4.png'
    mimg_5 = 'img/e0_5.png'
    m1img_0 = 'img/e1_0.png'
    m1img_1 = 'img/e1_1.png'
    m1img_2 = 'img/e1_2.png'
    m1img_3 = 'img/e1_3.png'
    m1img_4 = 'img/e1_4.png'
    m1img_5 = 'img/e1_5.png'
    imgbullet = 'img/enemymissile.gif'
    imgbullet1 = 'img/red.png'
    imgbullet2 = 'img/yellow.png'
    imgbullet3 = 'img/green.png'
    manchoose = 'img/red.png'
    hp1 = 10
    hp2 = 3
    hp3 = 10
    hpboss = 50
    dmg1 = 0
    dmg2 = 0
    played_warning = False
    old_room_level = 0
    room_level =0
    level = 1
    token_group = pygame.sprite.Group()

    def __init__(self):
        pass

    def draw_text(text):
        
        font = pygame.font.SysFont(None, 32)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        Maingame.window.blit(text_surface, text_rect)

    def show_pause_window():
        global game_paused
        game_paused = True
        button_width = 200
        button_height = 50
        font = pygame.font.Font(None,32)
        font_surface = font.render('Game Paused' , True , 'black')
        text1=Maingame.window.blit(font_surface, ((SCREEN_WIDTH-200)//2,(SCREEN_HEIGHT-50)//2))
        
        pygame.display.update(text1)
        
        
        button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT + 32) // 2, button_width, button_height)
        pygame.draw.rect(Maingame.window,(255,255,255), button_rect)       
        pygame.display.update(button_rect)

        while game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()                   
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    game_paused = False
                    pygame.mixer.unpause()
                    channel2.unpause()      

    #Start the game
    def startgame(self):
        global last_shot_time,current_shot_time,selection
        self.current_map = 0  
        pygame.display.init()
        Maingame.window=pygame.display.set_mode(SCREEN_SIZE)
        room_level = 0
           
        self.createEnemy()
        self.createWall()
        #Set window title
        pygame.display.set_caption('group2game5.0')
        clock = pygame.time.Clock()
        #sound2 = pygame.mixer.Sound('music/start.wav')   
        #channel2.play(sound2)
        # waiting channel1 over
        #while channel2.get_busy():
        #    pygame.time.delay(100)            
        #sound1 = pygame.mixer.Sound('music/enemyclose.wav')
        #channel1.play(sound1,loops=-1)
        bool1 = True
        bool3 = False
        bool4 = False
        start_button_clicked = False
        quit_button_clicked = False


        while bool1:
            # 处理事件
            # 第一个界面的绘制代码
            fengmian = pygame.image.load('img/fengmian.png')
            fengmian = pygame.transform.scale(fengmian, SCREEN_SIZE)
            Maingame.window.blit(fengmian, (0, 0))
            
            # 创建并绘制“开始游戏”按钮
            start_button_img = pygame.image.load("img/startgame.png")  
            start_button_rect = start_button_img.get_rect(center=(600, 450))  
            Maingame.window.blit(start_button_img, start_button_rect)  
            
            # 创建并绘制“退出游戏”按钮
            quit_button_img = pygame.image.load("img/quitgame.png") 
            quit_button_rect = quit_button_img.get_rect(center=(600, 600))  
            Maingame.window.blit(quit_button_img, quit_button_rect)  


            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                # 处理鼠标按键事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if start_button_rect.collidepoint(event.pos):
                        start_button_clicked = True
                        bool1 = False 
                        bool2 = True
                        
                    
                    elif quit_button_rect.collidepoint(event.pos):
                        quit_button_clicked = True
                
                # 处理按键事件
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                        
            
            if quit_button_clicked:
                pygame.quit()
                exit()


        selected_model_rect = None
        selected_weapon_rect = None
        
        while bool2:
            
            beijing2 = pygame.image.load('img/beijing2.png')
            beijing2 = pygame.transform.scale(beijing2, SCREEN_SIZE)
            Maingame.window.blit(beijing2, (0, 0))

           
            title_surf = self.gettextsuface('CHOOSE YOUR CHARACTER')
            title_rect = title_surf.get_rect(center=(640, 50))
            Maingame.window.blit(title_surf, title_rect)

            
            start_button_img = pygame.image.load("img/startgame.png")  
            start_button_rect = start_button_img.get_rect(center=(600, 600))  
            Maingame.window.blit(start_button_img, start_button_rect)  

           
            model1_image = pygame.image.load('img/0_0.png')
            model1_rect = pygame.Rect(100, 150, 200, 200)
            Maingame.window.blit(model1_image, model1_rect)

            model2_image = pygame.image.load('img/5_0.png')
            model2_rect = pygame.Rect(400, 150, 200, 200)
            Maingame.window.blit(model2_image, model2_rect)

            model3_image = pygame.image.load('img/104_0.png')
            model3_rect = pygame.Rect(700, 150, 200, 200)
            Maingame.window.blit(model3_image, model3_rect)

            #创建武器模型
            weapon1_image = pygame.image.load('img/z_6.png')
            weapon1_rect = pygame.Rect(100, 350, 200, 200)
            Maingame.window.blit(weapon1_image, weapon1_rect)

            weapon2_image = pygame.image.load('img/z_7.png')
            weapon2_rect = pygame.Rect(400, 350, 200, 200)
            Maingame.window.blit(weapon2_image, weapon2_rect)

            weapon3_image = pygame.image.load('img/z_8.png')
            weapon3_rect = pygame.Rect(700, 350, 200, 200)
            Maingame.window.blit(weapon3_image, weapon3_rect)
            
            if selected_model_rect is not None:
                selection_rect = pygame.Rect(0, 0, 20, 20)
                selection_rect.center = selected_model_rect.center  
                pygame.draw.rect(Maingame.window, (255, 0, 0), selection_rect)

            if selected_weapon_rect is not None:
                selectionweapon_rect = pygame.Rect(0, 0, 20, 20)
                selectionweapon_rect.center = selected_weapon_rect.center  
                pygame.draw.rect(Maingame.window, (255, 0, 0), selectionweapon_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # 处理鼠标按键事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 判断是否在模型1区域内
                    if model1_rect.collidepoint(event.pos):
                        # 选择人物模型1
                        Maingame.img_0 = 'img/0_0.png'
                        Maingame.img_1 = 'img/0_1.png'
                        Maingame.img_2 = 'img/0_2.png'
                        Maingame.img_3 = 'img/0_3.png'
                        Maingame.img_4 = 'img/0_4.png'
                        Maingame.img_5 = 'img/0_5.png'
                        Maingame.manchoose = Maingame.imgbullet1
                        selected_model_rect = model1_rect  
                        

                    # 判断是否在模型2区域内
                    elif model2_rect.collidepoint(event.pos):
                        # 选择人物模型2
                        Maingame.img_0 = 'img/5_0.png'
                        Maingame.img_1 = 'img/5_1.png'
                        Maingame.img_2 = 'img/5_2.png'
                        Maingame.img_3 = 'img/5_3.png'
                        Maingame.img_4 = 'img/5_4.png'
                        Maingame.img_5 = 'img/5_5.png'
                        Maingame.manchoose = Maingame.imgbullet2
                        selected_model_rect = model2_rect  
                        

                    # 判断是否在模型3区域内
                    elif model3_rect.collidepoint(event.pos):
                        # 选择人物模型3 
                        Maingame.img_0 = 'img/104_0.png'
                        Maingame.img_1 = 'img/104_1.png'
                        Maingame.img_2 = 'img/104_2.png'
                        Maingame.img_3 = 'img/104_3.png'
                        Maingame.img_4 = 'img/104_4.png'
                        Maingame.img_5 = 'img/104_5.png'                       
                        selected_model_rect = model3_rect  
                        Maingame.manchoose = Maingame.imgbullet3
                    elif weapon1_rect.collidepoint(event.pos):
                        # 选择人物模型1
                        Maingame.imgw = 'img/z_6.png'
                        selected_weapon_rect = weapon1_rect  
                        

                    # 判断是否在模型2区域内
                    elif weapon2_rect.collidepoint(event.pos):
                        # 选择人物模型2
                        Maingame.imgw = 'img/z_7.png'
                        
                        selected_weapon_rect = weapon2_rect  
                        

                    # 判断是否在模型3区域内
                    elif weapon3_rect.collidepoint(event.pos):
                        # 选择人物模型3 
                        Maingame.imgw = 'img/z_8.png'                       
                        selected_weapon_rect = weapon3_rect 

                    # 判断是否在“开始游戏”按钮区域内
                    elif start_button_rect.collidepoint(event.pos):
                        start_button_clicked = True
                        selected_model_rect = None
                        bool2 = False  # 第二个界面的循环结束
                        bool3 = True

                    

            # 处理按键事件
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()


        self.createMycharacter() 
        while bool3:
           
            
            Maingame.window.blit(background_image, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            #Fetch event
            self.getevent()
           
            
            #Draw text
            Maingame.window.blit(self.gettextsuface('Enemy survival: %d'%len(Maingame.enemyList+Maingame.boommonsterlist)),(10,10))
            Maingame.window.blit(self.gettextsuface('level:%d'%(Maingame.level)),(1220,10))
            
            try:
                Maingame.window.blit(self.gettextsuface('DMG:%d'%(Maingame.my_Character.dmg+1)),(10,70))
                Maingame.window.blit(self.gettextsuface('HP: %d'%(Maingame.my_Character.hp)),(10,30))
                Maingame.window.blit(self.gettextsuface('Speed: %d'%(Maingame.my_Character.speed)),(10,90))
                pygame.draw.rect(Maingame.window,(255,255,255),(30,60,50,10))
                hp_width = Maingame.my_Character.hp/10*50
                pygame.draw.rect(Maingame.window,(255,0,0),(30,60,hp_width,10))
            except AttributeError as e:
                Maingame.window.blit(self.gettextsuface('YOU DIE!'),(640,400))
                pass
            
            #Method that invokes the display of the character
            if Maingame.my_Character and Maingame.my_Character.live:
                Maingame.my_Character.displayCharacter()
                Maingame.my_Character.myCharacter_moving()
            else:
                #删除我方人物
                del Maingame.my_Character
                Maingame.my_Character=None

            try:
                # 加载您的图像
                weapon_img = pygame.image.load(Maingame.imgw)
                # 旋转并缩放您的图像以匹配武器长度和角度
                rotated_weapon_img = pygame.transform.rotate(weapon_img, Maingame.my_Character.weapon_angle)
                scaled_weapon_img = pygame.transform.scale(rotated_weapon_img, (Maingame.my_Character.weapon_length, rotated_weapon_img.get_height()))
                weapon_rect = weapon_img.get_rect()
                weapon_rect.center = Maingame.my_Character.rect.center
                weapon_start1 = Maingame.my_Character.rect.center 
                weapon_end_x1 = Maingame.my_Character.rect.centerx - Maingame.my_Character.weapon_length * math.sin(Maingame.my_Character.weapon_angle/180*math.pi)
                weapon_end_y1 = Maingame.my_Character.rect.centery - Maingame.my_Character.weapon_length * math.cos(Maingame.my_Character.weapon_angle/180*math.pi)
                weapon_end1 = (weapon_end_x1, weapon_end_y1)
                # 绘制武器图像
                #pygame.draw(Maingame.window,weapon_start1,weapon_end1)
                Maingame.window.blit(rotated_weapon_img,weapon_rect)
                #pygame.draw.line(Maingame.window, (0,0,0), weapon_start1, weapon_end1, 2)
            except:
                pass
            
            
            self.blitEnemy()
            self.blitboommonster()
            if Maingame.enemyList or Maingame.boommonsterlist:
                self.blitMyBullet()
            self.blitEnemyBullet()
            self.blitExplode()
            self.blitWall()
            self.blitMySkill()
            
            
            
        
           
            if Maingame.my_Character and Maingame.my_Character.live:
                if not Maingame.my_Character.stop:
                    Maingame.my_Character.move()
                    #检测我方人物是否与墙壁发生碰撞
                    Maingame.my_Character.hitWall()
                    #检测我方人物是否与敌方人物发生碰撞text,True,TEXT_COLOR
                    Maingame.my_Character.myCharacter_hit_enemy()
                    Maingame.my_Character.myCharacter_collision_room()
                    #Maingame.my_Character.myCharacter_hit_monster_1()
            if not Maingame.enemyList:
                Maingame.enemyBulletList.clear()
            if not Maingame.boommonsterlist:
                Maingame.boommonsterlist.clear()
            if (not Maingame.enemyList) and (not Maingame.boommonsterlist):
                Maingame.myBulletList.clear()               
                alive = False
                # 创建传送门
                portal_img = pygame.image.load('img/0250001.png')
                portal_pos = (1000, 350)
                Maingame.window.blit(portal_img, portal_pos)
                my_character_pos = Maingame.my_Character.rect.center
                

                # 计算人物和传送门之间的距离
                dx = my_character_pos[0] - portal_pos[0]
                dy = my_character_pos[1] - portal_pos[1]
                distance = math.sqrt(dx*dx + dy*dy)
                portal_rect= portal_img.get_rect()
                

                # 判断是否接近传送门
                if 1000<=Maingame.my_Character.rect.left<=1020 and 350<=Maingame.my_Character.rect.top<=370:
                    
                    bool4 = True
                    hpbool = False
                    dmgbool = False
                    while bool4:
                        
                        button_width = 200
                        button_height = 50
                        beijing2 = pygame.image.load('img/beijing2.png')
                        beijing2 = pygame.transform.scale(beijing2, SCREEN_SIZE)
                        Maingame.window.blit(beijing2, (0, 0))
                        
                        # 创建并绘制“继续游戏”按钮
                        continue_button_rect = pygame.Rect(800, 400, 200, 100)
                        continue_button = pygame.draw.rect(Maingame.window, (0, 255, 0), continue_button_rect)   
                        continue_text_surf = self.gettextsuface('CONTINUE THE GAME')
                        continue_text_rect = continue_text_surf.get_rect(center=continue_button.center)
                        Maingame.window.blit(continue_text_surf, continue_text_rect)

                        
                        hp_image = pygame.image.load('img/hp.png')
                        hp_rect = pygame.Rect(100, 150, 200, 200)
                        Maingame.window.blit(hp_image, hp_rect)

                        dmg_image = pygame.image.load('img/dmg.png')
                        dmg_rect = pygame.Rect(400, 150, 200, 200)
                        Maingame.window.blit(dmg_image, dmg_rect)

                        if selected_model_rect is not None:
                            selection_rect = pygame.Rect(0, 0, 20, 20)
                            selection_rect.center = selected_model_rect.center  # 设置选中标记的位置为选中人物的中心
                            pygame.draw.rect(Maingame.window, (255, 0, 0), selection_rect)


                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            
                            # 处理鼠标按键事件
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                # 判断是否在“继续游戏”按钮区域内
                                if continue_button.collidepoint(event.pos):
                                    continue_button_clicked = True
                                    alive = True
                                    if hpbool:
                                        Maingame.hp1+=2
                                    if dmgbool:
                                        Maingame.dmg1+=1
                                    selected_model_rect = None
                                    bool4 = False

                                elif hp_rect.collidepoint(event.pos):
                                    # 选择人物模型1
                                    Maingame.my_Character.hp+=1                                    
                                    selected_model_rect = hp_rect                                   
                                    hpbool = True  
                                    

                                # 判断是否在模型2区域内
                                elif dmg_rect.collidepoint(event.pos):
                                    # 选择人物模型2
                                    Maingame.my_Character.dmg+=1                        
                                    selected_model_rect = dmg_rect                                    
                                    dmgbool = True      
                                                               
                            # 处理按键事件
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    pygame.quit()
                                    exit()
                                 
                               
                #Maingame.wallList.clear()
                self.current_map = (self.current_map + 1) % 5
                if alive:                    
                    self.createMycharacter()
                    self.createWall()
                    if (Maingame.level % 5) != 0:
                        Maingame.enemyCount += 1
                        self.createEnemy()
                        self.createboommonster()

                    if (Maingame.level % 5) == 0:
                        Maingame.enemyCount = 3
                        self.createEnemy()
                        self.createBoss()
                        self.createboommonster()
                        Maingame.hp2 +=1
                        Maingame.hp3 +=5
                        Maingame.hpboss +=25

                    Maingame.level +=1
                    
                    

            pygame.display.update()

     # 循环遍历墙壁列表，展示墙壁            
    def blitWall(self):
        for wall in Maingame.wallList:
            #判断墙壁是否存活
            if wall.live:
                #调用墙壁的显示方法
                wall.displayWall()
            else:
                #从墙壁列表移出
                Maingame.wallList.remove(wall)
    #初始化墙壁
    def createWall(self):
        # 循环遍历地图矩阵，并绘制地图
        map_data = maps[self.current_map][f"map{self.current_map % 5 + 1}"]
        for row in range(len(map_data)):
            for col in range(len(map_data[row])):
                tile = map_data[row][col]
                x = col * tile_size
                y = row * tile_size
                if tile == 1:
                    # 绘制墙壁
                    Maingame.imgwall = 'img/steels.gif'
                    wall = Wall(x+300,y+150)
                    wall.displayWall()
                    Maingame.wallList.append(wall)
                if tile == 2:
                    # 绘制墙壁
                    Maingame.imgwall = 'img/flower.png'
                    wall = Wall(x+400,y+150)
                    wall.displayWall()
                    Maingame.wallList.append(wall)
                         
    def createMycharacter(self):
        Maingame.my_Character = MyCharacter(640,400)
        
    #Initializes enemies and adds enemies to the list        
    def createEnemy(self):
        top = 50
        Maingame.mimg_0 = 'img/e0_0.png'
        Maingame.mimg_1 = 'img/e0_1.png'
        Maingame.mimg_2 = 'img/e0_2.png'
        Maingame.mimg_3 = 'img/e0_3.png'
        Maingame.mimg_4 = 'img/e0_4.png'
        Maingame.mimg_5 = 'img/e0_5.png'
        #Loop spawn enemies
        if Maingame.level % 5 == 0:
                Maingame.dmg2 += 2
                
        for i in range(Maingame.enemyCount):
            left = random.randint(0,1000)
            speed = 1
            hp = Maingame.hp3
            enemy = monster(left,top,speed,hp,dmg=Maingame.dmg2)
            Maingame.enemyList.append(enemy)

    def createBoss(self):
        top = 50

        #Loop spawn enemies        
        left = random.randint(0,1000)
        speed = 0
        hp = Maingame.hpboss
        Maingame.mimg_0 = 'img/e3_0.png'
        Maingame.mimg_1 = 'img/e3_1.png'
        Maingame.mimg_2 = 'img/e3_2.png'
        Maingame.mimg_3 = 'img/e3_3.png'
        Maingame.mimg_4 = 'img/e3_4.png'
        Maingame.mimg_5 = 'img/e3_5.png'
        enemy = monster(left,top,speed,hp,dmg=Maingame.dmg2)
        Maingame.enemyList.append(enemy)

    def createboommonster(self):
        left = 50
        Maingame.mimg_0 = 'img/e1_0.png'
        Maingame.mimg_1 = 'img/e1_1.png'
        Maingame.mimg_2 = 'img/e1_2.png'
        Maingame.mimg_3 = 'img/e1_3.png'
        Maingame.mimg_4 = 'img/e1_4.png'
        Maingame.mimg_5 = 'img/e1_5.png'
        #Loop spawn enemies
        if Maingame.level % 5 == 0:
                Maingame.dmg2 += 2
                
                
        for i in range(Maingame.enemyCount-2):
            top = random.randint(200,600)
            speed = 9
            hp = Maingame.hp2
            enemy = monster(left,top,speed,hp,dmg=1)
            Maingame.boommonsterlist.append(enemy)

    #循环展示爆炸效果
    def blitExplode(self):
        for explode in Maingame.explodeList:
            #判断是否活着
            if explode.live:
                #展示
                explode.displayExplode()
            else:
                #在爆炸列表中移除
                Maingame.explodeList.remove(explode) 

    #Loop through the enemies list, displaying enemies
    def blitEnemy(self):       
        global last_shot_time,current_shot_time
        current_shot_time = pygame.time.get_ticks()
        time = (last_shot_time - current_shot_time)
        for monster in Maingame.enemyList:
            #Determine if the current enemy tank is alive
            if monster.live:
                monster.displayCharacter()
                monster.randMove()
                monster.track(Maingame.my_Character)
                #调用检测是否与墙壁碰撞
                monster.hitWall()
                if Maingame.my_Character and Maingame.my_Character.live:
                    monster.enemy_hit_myCharacter()                
                    #fire bollet
                    (x2,y2) = (Maingame.my_Character.rect.left,Maingame.my_Character.rect.top)
                    (x1,y1) = monster.rect.center                    
                    if (sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) < 300:
                        dx = x2 - x1
                        dy = y2 - y1
                        angle = math.atan2(-dy, dx) * 180 / math.pi 
                        enemyBullet = Bullet(monster, monster.rect.centerx, monster.rect.bottom, angle-90)           
                        if enemyBullet:
                            if current_shot_time - last_shot_time >=shoot_interval:
                                Maingame.imgbullet = 'img/enemymissile.gif'
                                Maingame.enemyBulletList.append(enemyBullet)
                                last_shot_time = current_shot_time
            #Not alive, removed from enemy tank list
            else:
                Maingame.enemyList.remove(monster)
                music = Music('music/dead.wav')
                music.play()

    def blitboommonster(self):       
        global last_shot_time,current_shot_time
        current_shot_time = pygame.time.get_ticks()
        time = (last_shot_time - current_shot_time)
        for monster in Maingame.boommonsterlist:
            #Determine if the current enemy tank is alive
            if monster.live:
                monster.displayCharacter()
                monster.randMove()
                monster.track(Maingame.my_Character)
                #调用检测是否与墙壁碰撞
                monster.hitWall()
                if Maingame.my_Character and Maingame.my_Character.live:
                    monster.boom_hit_myCharacter()                
                    #fire bollet
                    (x2,y2) = (Maingame.my_Character.rect.left,Maingame.my_Character.rect.top)
                    (x1,y1) = monster.rect.center                    
                    if (sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) < 300:
                        dx = x2 - x1
                        dy = y2 - y1
                        angle = math.atan2(-dy, dx) * 180 / math.pi 
                        enemyBullet = Bullet(monster, monster.rect.centerx, monster.rect.bottom, angle-90)           
                        if enemyBullet:
                            if current_shot_time - last_shot_time >=shoot_interval:
                                Maingame.imgbullet = 'img/enemymissile.gif'
                                Maingame.enemyBulletList.append(enemyBullet)
                                last_shot_time = current_shot_time
            #Not alive, removed from enemy tank list
            else:
                Maingame.boommonsterlist.remove(monster)
                music = Music('music/dead.wav')
                music.play()

                
    def blitRoom(self):
        if (not Maingame.enemyList) and (not Maingame.boommonsterlist):
            pygame.draw.rect(Maingame.window, (0, 255, 0), pygame.Rect(640, 400, 50, 80))
            
    def creatRoom(self):
        for j in range(2):
                for i in range(7):
                    #初始化墙壁
                    room=Room(i*200,200 + j*300)
                    #将墙壁添加到列表中
                    Maingame.roomList.append(Room)
    
    #Loop through our bullet store list
    def blitMyBullet(self):  
        try:
            Maingame.imgbullet = Maingame.manchoose 
            for myBullet in Maingame.myBulletList:
            #Determine whether the current bullet is alive, if so, display and move
                if myBullet.live:              
                    myBullet.displayBullet()
                    myBullet.move()
                    myBullet.myBullet_hit_enemy()
                    myBullet.hitWall()
                    
                else:
                    Maingame.myBulletList.remove(myBullet)
                    sound3 = pygame.mixer.Sound('music/loadbullet.wav')   
                    channel3.play(sound3)
                                   
                
        except:
            pass
    #Loop through bullets that show enemy,displaying enemy bullet
    def blitEnemyBullet(self): 
        Maingame.imgbullet = 'img/enemymissile.gif'       
        for enemyBullet in Maingame.enemyBulletList:
            if enemyBullet.live :                              
                enemyBullet.displayBullet()               
                enemyBullet.move()
                enemyBullet.enemyBullet_hit_myCharacter()
                enemyBullet.hitWall()
            else:
                Maingame.enemyBulletList.remove(enemyBullet)
                
    def blitMySkill(self):
        for mySkill in Maingame.mySkillList:
            if mySkill.live:
                    mySkill.displaySkill()
                    mySkill.move()
                    mySkill.mySkill_hit_enemy()
                    mySkill.hitWall()
            else:
                Maingame.mySkillList.remove(mySkill)

    #End the game
    def endgame(self):
        print('Thanks for using, and welcome to use again')
        exit()
   
    #The drawing of the upper-left text
    def gettextsuface(self,text):
        #Initializes the font module
        pygame.font.init()
        #Gets the font font object
        font=pygame.font.SysFont('arial',18)

        #Draw text information
        textsurface = font.render(text,True,TEXT_COLOR)
        return textsurface
        
    #Fetch event
    def getevent(self): 
        global last_shot_time
        #Fetch all event
        eventlist = pygame.event.get()
        #Traversal event
        
        for event in eventlist:
            #Determine whether the press is off or keyboard down
            #If exit is pressed, close the window
            if event.type == pygame.QUIT:
                self.endgame()
            #If it's a keyboard press
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.endgame()
                if event.key == pygame.K_TAB:                   
                    Maingame.show_pause_window()


                #当人物不存在或者死亡时
                if not Maingame.my_Character:
                    #判断按下的是LSHIFT键时，让人物重生
                    if event.key == pygame.K_LSHIFT:
                        self.createMycharacter()
                if Maingame.my_Character and Maingame.my_Character.live:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        if keys[pygame.K_UP]:
                            Maingame.my_Character.direction = 'UL'
                            Maingame.my_Character.stop=False
                            Maingame.my_Character.moving = True
                            print('Turn up left')
                        elif keys[pygame.K_DOWN]:
                            Maingame.my_Character.direction = 'DL'
                            Maingame.my_Character.stop=False
                            Maingame.my_Character.moving = True
                            print('Turn down left')
                        else:
                            Maingame.my_Character.direction = 'L'
                            Maingame.my_Character.stop=False
                            Maingame.my_Character.moving = True
                            print('Turn left')
                            
                    elif keys[pygame.K_RIGHT]:
                        if keys[pygame.K_UP]:
                            Maingame.my_Character.direction = 'UR'
                            Maingame.my_Character.stop=False
                            Maingame.my_Character.moving = True
                            print('Turn up right')
                            
                        elif keys[pygame.K_DOWN]:
                            Maingame.my_Character.direction = 'DR'
                            Maingame.my_Character.stop=False
                            Maingame.my_Character.moving = True
                            print('Turn down right')
                            
                        else:
                            Maingame.my_Character.direction = 'R'
                            Maingame.my_Character.stop=False
                            Maingame.my_Character.moving = True
                            print('Turn right')
                    elif keys[pygame.K_UP]:
                        Maingame.my_Character.direction = 'U'
                        Maingame.my_Character.stop=False
                        Maingame.my_Character.moving = True
                        print('Turn up')
                    elif keys[pygame.K_DOWN]:
                        Maingame.my_Character.direction = 'D'
                        Maingame.my_Character.stop=False
                        Maingame.my_Character.moving = True
                        print('Turn down')
                    
                    elif keys[pygame.K_RCTRL]:
                        print('spell')
                        if len(Maingame.mySkillList)<1:
                            mySkill = Skill(Maingame.my_Character)
                            Maingame.mySkillList.append(mySkill)
                          

            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                # 鼠标左键点击
                    if event.button == 1 and Maingame.my_Character and Maingame.my_Character.live and len(Maingame.myBulletList)<5:
                    # 获取鼠标位置
                        mouse_pos = pygame.mouse.get_pos()
                    # 获取人物中心位置
                        character_center = self.my_Character.rect.left + self.my_Character.rect.width / 2, self.my_Character.rect.top + self.my_Character.rect.height / 2
                    # 计算鼠标与人物中心位置的夹角
                        angle = math.atan2(mouse_pos[1] - character_center[1], mouse_pos[0] - character_center[0])
                    # 将夹角转换为人物朝向
                        if -math.pi / 4 <= angle <= math.pi / 4:
                            self.my_Character.image = pygame.image.load(Maingame.img_0)
                        elif math.pi / 4 < angle <= 3 * math.pi / 4:
                            pass
                        elif -3 * math.pi / 4 <= angle < -math.pi / 4:
                            pass
                        else:
                            self.my_Character.image = pygame.image.load(Maingame.img_1)
                    
                    #if len(Maingame.myBulletList)<4:
                    # Create a new bullet object
                        Maingame.imgbullet = Maingame.manchoose
                        bullet = Bullet(Maingame.my_Character,Maingame.my_Character.rect.centerx,Maingame.my_Character.rect.centery,Maingame.my_Character.weapon_angle)
                        Maingame.myBulletList.append(bullet)            
                        music = Music('music/shot.wav')
                        music.play()
                    if event.button == 1 and Maingame.my_Character and Maingame.my_Character.live and len(Maingame.myBulletList)>=4 and len(Maingame.myBulletList)<5 and current_shot_time - last_shot_time >= reload_interval:
                        #if current_shot_time - last_shot_time >= reload_interval:
                        mouse_pos = pygame.mouse.get_pos()
                    # 获取人物中心位置
                        character_center = self.my_Character.rect.left + self.my_Character.rect.width / 2, self.my_Character.rect.top + self.my_Character.rect.height / 2
                    # 计算鼠标与人物中心位置的夹角
                        angle = math.atan2(mouse_pos[1] - character_center[1], mouse_pos[0] - character_center[0])
                    # 将夹角转换为人物朝向
                        if -math.pi / 4 <= angle <= math.pi / 4:
                            self.my_Character.image = pygame.image.load(Maingame.img_0)
                        elif math.pi / 4 < angle <= 3 * math.pi / 4:
                            pass
                        elif -3 * math.pi / 4 <= angle < -math.pi / 4:
                            pass
                        else:
                            self.my_Character.image = pygame.image.load(Maingame.img_1)
                    
                    #if len(Maingame.myBulletList)<4:
                    # Create a new bullet object
                        Maingame.imgbullet = Maingame.manchoose
                        bullet = Bullet(Maingame.my_Character,Maingame.my_Character.rect.centerx,Maingame.my_Character.rect.centery,Maingame.my_Character.weapon_angle)
                        Maingame.myBulletList.append(bullet)            
                        music = Music('music/shot.wav')
                        music.play()
                        last_shot_time = current_shot_time
                except:
                    pass    

            #Release the arrow key, stop moving, and modify the switch status of the character
            if event.type == pygame.KEYUP:
                #Determine if the released key is up/down/left/right before you stop moving
                if event.key ==pygame.K_UP or event.key ==pygame.K_DOWN or event.key ==pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                    if Maingame.my_Character and Maingame.my_Character.live:
                        Maingame.my_Character.stop = True


class Character(BaseItem):
    
    #Add distance left, distance top
    def __init__(self,left,top):
        
        #Save the loaded image
        self.images = {
            'U':pygame.image.load(Maingame.img_0),
            'D':pygame.image.load(Maingame.img_0),
            'L':pygame.image.load(Maingame.img_3),
            'R':pygame.image.load(Maingame.img_0),
            'DL':pygame.image.load(Maingame.img_3),
            'DR':pygame.image.load(Maingame.img_0),
            'UL':pygame.image.load(Maingame.img_3),
            'UR':pygame.image.load(Maingame.img_0),
        }

        
        #direction
        self.direction = 'L'
        self.image = self.images[self.direction]
        self.rect =self.image.get_rect()
        self.dmg = Maingame.dmg1
        self.rect.left = left
        self.rect.top = top
        self.pos = (left,top)
        self.hp = Maingame.hp1
        self.hp_box = (self.rect.left + 17, self.rect.top + 2, 31, 57)
        

        #speed 
        self.speed = 5
        self.diagonal_speed = 3.5
        #The switch that the character moves
        self.stop = True
        #To keep track of whether a person is alive or not
        self.live = True
        #新增属性原来坐标
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top
        
        self.step = 0
        self.moving = True
        self.move_imageR = [
            pygame.image.load(Maingame.img_1),
            pygame.image.load(Maingame.img_2)
        ]
        self.move_imageL = [
            pygame.image.load(Maingame.img_4),
            pygame.image.load(Maingame.img_5)
        ]

    #move
    def move(self):
        #移动后记录原始的坐标
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top
        #Judge the direction of the character
        
        
        if self.direction =='L':
            if self.rect.left >0:
                self.rect.left -= self.speed
        elif self.direction =='U':
            if self.rect.top >0:
                self.rect.top -= self.speed                
        elif self.direction =='D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed        
        elif self.direction =='R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction =='UL':
            if self.rect.top >0 and self.rect.left >0:
                self.rect.top -= self.diagonal_speed
                self.rect.left -= self.diagonal_speed               
        elif self.direction =='UR':
            if self.rect.top >0 and (self.rect.left + self.rect.height) < SCREEN_WIDTH:
                self.rect.top -= self.diagonal_speed
                self.rect.left += self.diagonal_speed        
        elif self.direction =='DL':
            if (self.rect.top + self.rect.height) < SCREEN_HEIGHT and self.rect.left >0:
                self.rect.top += self.diagonal_speed
                self.rect.left -= self.diagonal_speed
        elif self.direction =='DR':
            if (self.rect.top + self.rect.height) < SCREEN_HEIGHT and (self.rect.left + self.rect.height) < SCREEN_WIDTH:
                self.rect.top += self.diagonal_speed
                self.rect.left += self.diagonal_speed
        
    #Health/Blue/Damage
    def CharacterAttribute(self):
        pass
    
    def enemy_die(self):
        return monster(self)

    #shot
    def shot(self):
        Maingame.imgbullet = Maingame.manchoose
        return Bullet(self)    
    #spell
    def spell(self):
        return Skill(self)

    def stay(self):
        self.rect.left=self.oldLeft
        self.rect.top=self.oldTop
    
    #检测人物是否与墙壁发生碰撞
    def hitWall(self):
        for wall in Maingame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                #将坐标设置为移动之前的坐标
                self.stay()
    #Show the player's approach
    def displayCharacter(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = self.rect.center
        self.weapon_angle = math.atan2(player_x-mouse_x, player_y-mouse_y)*180/math.pi
        self.weapon_angle %= 360
        if self.weapon_angle > 180:
            self.image = pygame.image.load(Maingame.img_1) 
        if self.weapon_angle<180:
            self.image = pygame.image.load(Maingame.img_0)

        #Gets the object to display
        self.image = self.images[self.direction]
        #Call the blit method display
        Maingame.window.blit(self.image,self.rect)
        
    def draw_hp_box(self,window):
        pygame.draw.rect(window,(0,128,0),(self.hp_box[0],self.hp_box[1]-10,40,8) )
        pygame.draw.rect(window,(255,0,0),(self.hp_box[0]+self.hp*4,self.hp_box[1]-10,40-self.hp*4,8))

#player
class MyCharacter(Character):
    def __init__(self,left,top):
        super(MyCharacter, self).__init__(left,top)
        self.rect = self.image.get_rect()
        self.rect.center = (left, top)
        self.weapon_length = 50
        self.weapon_angle = 0
        self.mask = pygame.mask.from_surface(self.image)
        
    def myCharacter_moving(self):
        try:
            if self.direction =='R'or self.direction =='UR' or self.direction =='DR' and self.moving == True:
                if self.step<len(self.move_imageR):
                    self.image=self.move_imageR[self.step]
                    self.step+=1
                    Maingame.window.blit(self.image,self.rect)
                elif Maingame.my_Character.stop ==True :
                    Maingame.window.blit(self.image,self.rect)
                elif self.direction =='U' or self.direction =='D':
                    Maingame.window.blit(self.image.self.rect)

                else:
                
                    self.step=0
        
            if self.direction =='U' or self.direction =='D' or self.direction =='L'or self.direction =='UL' or self.direction =='DL' and self.moving == True:
                if self.step<len(self.move_imageL):
                    self.image=self.move_imageL[self.step]
                    self.step+=1
                    Maingame.window.blit(self.image,self.rect)
            
                elif Maingame.my_Character.stop == True :
                    Maingame.window.blit(self.image,self.rect)
                elif self.direction =='U' or self.direction =='D':
                    Maingame.window.blit(self.image.self.rect)
            
                else:
                    self.step = 0
        except:
            pass
        
    
    #检测我方与敌方发生碰撞
    def myCharacter_hit_enemy(self):
        #循环遍历敌方列表
        for monster in (Maingame.enemyList or Maingame.boommonsterlist):
            if pygame.sprite.collide_mask(self,monster):
                self.stay()
    

    def myCharacter_collision_room(self):
        for room in Maingame.roomlist:
            if pygame.sprite.collide_mask(self,room):
                Maingame.window.fill((0,0,0))
                Maingame.startgame()

#monster
class monster(Character):
    def __init__(self,left,top,speed,hp,dmg):
        #Calls the parent class's initialization method
        super(monster, self).__init__(left,top)
        pygame.sprite.Sprite.__init__(self)
        #Load the photo set
        self.images = {
            'U':pygame.image.load(Maingame.mimg_0),
            'D':pygame.image.load(Maingame.mimg_0),
            'L':pygame.image.load(Maingame.mimg_3),
            'R':pygame.image.load(Maingame.mimg_0),
            'DL':pygame.image.load(Maingame.mimg_3),
            'DR':pygame.image.load(Maingame.mimg_0),
            'UL':pygame.image.load(Maingame.mimg_3),
            'UR':pygame.image.load(Maingame.mimg_0),
        }  
        #Direction: Randomly generate enemy directions
        self.direction = self.randDirection()

        #Get the picture according to the direction
        self.image =self.images[self.direction]

        #area
        self.rect = self.image.get_rect()
        self.rect.center = (left,top)
        #Assign left and top
        self.rect.left = left
        self.rect.top = top

        #speed
        self.speed = speed

        #Moving switch
        self.flag = True 
        self.dmg = dmg
        self.hp = hp
        self.hp_box = (self.rect.left + 17, self.rect.top + 2, 31, 57)

        self.weapon_length = 50
        self.weapon_angle = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.stop = False
        self.gap = 60

        self.move_imageR = [
            pygame.image.load(Maingame.mimg_1),
            pygame.image.load(Maingame.mimg_2)
        ]
        self.move_imageL = [
            pygame.image.load(Maingame.mimg_4),
            pygame.image.load(Maingame.mimg_5)
        ]
        
    #敌方人物与我方人物是否发生碰撞
    def enemy_hit_myCharacter(self):
        if pygame.sprite.collide_mask(self,Maingame.my_Character):           
            self.stay()
            

    def boom_hit_myCharacter(self):
        if pygame.sprite.collide_mask(self,Maingame.my_Character):
            Maingame.my_Character.hp -= 1 
            self.live = False
            if Maingame.my_Character.hp <=0:
                Maingame.my_Character.live = False
             

    #Randomly generate enemy directions
    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'   
    #The way enemies move randomly
    def randMove(self):
        self.moving = True
        if self.gap <= 0:
            self.direction = self.randDirection()
            self.gap = 60
        else:
            self.move()
            self.gap -=1
        
        try:
            if self.direction =='R'or self.direction =='UR' or self.direction =='DR' and self.moving == True:
                    if self.step<len(self.move_imageR):
                        self.image=self.move_imageR[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image,self.rect)
                    elif self.stop ==True :
                        Maingame.window.blit(self.image,self.rect)
                    elif self.direction =='U' or self.direction =='D':
                        self.image=self.move_imageR[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image.self.rect)

                    else:
                
                        self.step=0
        
            if self.direction =='U' or self.direction =='D' or self.direction =='L'or self.direction =='UL' or self.direction =='DL' and self.moving == True:
                    if self.step<len(self.move_imageL):
                        self.image=self.move_imageL[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image,self.rect)
            
                    elif self.stop == True :
                        Maingame.window.blit(self.image,self.rect)
                    elif self.direction =='U' or self.direction =='D':
                        self.image=self.move_imageR[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image.self.rect)
            
                    else:
                        self.step = 0
           
        except:
            pass
        
    def track(self, MyCharacter):
        # 计算怪物和人物之间的距离
        self.stop = False
        try:
            distance = sqrt((MyCharacter.rect.left - self.rect.left) ** 2 + (MyCharacter.rect.top - self.rect.top) ** 2)
        
        # 如果距离小于一定范围，就朝向人物移动
            if distance < 300:                
            # 确定移动方向
                  
                dx = MyCharacter.rect.left - self.rect.left
                dy = MyCharacter.rect.top - self.rect.top
                
                    
                if dx >0 :
                    self.rect.left += self.speed
                    self.direction = 'R'
                elif dx <0 :
                    self.rect.left -= self.speed
                    self.direction = 'L'
                
                if dy > 0 :
                    self.rect.top += self.speed
                    self.direction = 'D'
                elif dy < 0 :
                    self.rect.top -= self.speed
                    self.direction = 'U'
                
                
            if self.direction =='R'or self.direction =='UR' or self.direction =='DR' and self.moving == True:
                    if self.step<len(self.move_imageR):
                        self.image=self.move_imageR[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image,self.rect)
                    elif self.stop ==True :
                        Maingame.window.blit(self.image,self.rect)
                    elif self.direction =='U' or self.direction =='D':
                        self.image=self.move_imageR[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image.self.rect)

                    else:
                
                        self.step=0
        
            if self.direction =='U' or self.direction =='D' or self.direction =='L'or self.direction =='UL' or self.direction =='DL' and self.moving == True:
                    if self.step<len(self.move_imageL):
                        self.image=self.move_imageL[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image,self.rect)
            
                    elif self.stop == True :
                        Maingame.window.blit(self.image,self.rect)
                    elif self.direction =='U' or self.direction =='D':
                        self.image=self.move_imageR[self.step]
                        self.step+=1
                        Maingame.window.blit(self.image.self.rect)
            
                    else:
                        self.step = 0

        except:
            pass         
    #rewrite shot()
    def shot(self):
        
        try:
            distance = sqrt((Maingame.my_Character.rect.left - self.rect.left) ** 2 + (Maingame.my_Character.rect.top - self.rect.top) ** 2)            
            if distance<=300 and (self.rect.left==Maingame.my_Character.rect.left or Maingame.my_Character.rect.top == self.rect.top) :                        
                    Maingame.imgbullet = 'img/enemymissile.gif'
                    Maingame.enemyBulletList.add(Bullet)
            else:
                Maingame.enemyBulletList.remove(Bullet)
                    
        except:
            pass
    def reset(self):
        if len(Maingame.enemyList) == 0:
            len(Maingame.enemyList)== 6
            self.x = random.randint(0,500)
            self.y = random.randint(0,500)
            self.live = True


class Skill():
    def __init__(self,Character):
        self.image = pygame.image.load('img/skill.png')
        self.direction = Character.direction
        self.rect = self.image.get_rect()

        if self.direction == 'U':
            self.rect.left = Character.rect.left + Character.rect.width / 2 - self.rect.width / 2
            self.rect.top = Character.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = Character.rect.left + Character.rect.width / 2 - self.rect.width / 2
            self.rect.top = Character.rect.top + Character.rect.height
        elif self.direction == 'L':
            self.rect.left = Character.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = Character.rect.top + Character.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = Character.rect.left + Character.rect.width
            self.rect.top = Character.rect.top + Character.rect.width / 2 - self.rect.width / 2

        self.speed = 5
        self.dmg = 3
        self.live = True
#Skill class
#Attribute of skill

    

    def displaySkill(self):
        Maingame.window.blit(self.image,self.rect)

    def mySkill_hit_enemy(self):
        for monster in (Maingame.enemyList or Maingame.boommonsterlist):
            if pygame.sprite.collide_rect(monster,self):
                #Changed the status of enemy and our bullets
                monster.live=False
                self.live=True
                #创建爆炸对象
                explode=Explode(monster)
                #将爆炸对象添加到爆炸列表中
                Maingame.explodeList.append(explode)
                

    def move(self):
        if self.direction == 'U':
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                #Modify status value
                self.live = False
        elif self.direction == 'R':
            if self.rect.left+self.rect.width<SCREEN_WIDTH:
                self.rect.left+=self.speed
            else:
                #Modify status value
                self.live = False
        elif self.direction =='D':
            if self.rect.top+self.rect.height<SCREEN_HEIGHT:
                self.rect.top+=self.speed
            else:
                #Modify status value
                self.live = False
        elif self.direction == 'L':
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                #Modify status value
                self.live = False

    def hitWall(self):
        for wall in Maingame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                self.live=False
                wall.hp-=1
                if wall.hp<=0:
                    wall.live=False
        
#Bullet class
class Bullet():   
    def __init__(self,Character,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        #Load picture
        self.image = pygame.image.load(Maingame.imgbullet)
        #The direction of the character determines the direction of the bullet
        self.direction = Character.direction
        #Acquisition region
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #bullet speed
        self.speed=6
        #To keep track of whether the bullet is alive
        self.live = True

        self.dmg =1
        self.angle = angle
        self.capacity = 10
        self.mask = pygame.mask.from_surface(self.image)
        

    #bullet move
    def move(self):
        self.rect.y -= self.speed * math.cos(self.angle/180*math.pi)
        self.rect.x -= self.speed * math.sin(self.angle/180*math.pi)
        self.off_screen()

    def off_screen(self):
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.live = False    
    
    #子弹是否碰撞墙壁
    def hitWall(self):
        #循环遍历墙壁列表
        for wall in Maingame.wallList:
            if pygame.sprite.collide_mask(self,wall):
                #修改子弹的生存状态，让子弹消失
                self.live=False
                #墙壁的生命值减小
                wall.hp-=1
                if wall.hp<=0:
                    #修改墙壁的生存状态
                    wall.live=False
                    

    #Show the bullet method
    def displayBullet(self):
        #Load the image surface into the window
        
            Maingame.window.blit(self.image,self.rect)

    #The collision of our bullets with the enemy
    def myBullet_hit_enemy(self):
        #Loop through the enemies list to determine if a collision has occurred
        for monster in Maingame.enemyList:
            if pygame.sprite.collide_mask(monster,self):
                if monster.hp - (self.dmg+Maingame.my_Character.dmg) <= 0:
                    monster.live=False
                    self.live=False    
                    explode=Explode(monster)
                    Maingame.explodeList.append(explode)
                else:
                    monster.hp -= (self.dmg+Maingame.my_Character.dmg)
                    monster.live = True
                    self.live = False
        for monster in Maingame.boommonsterlist:
            if pygame.sprite.collide_mask(monster,self):
                if monster.hp - (self.dmg+Maingame.my_Character.dmg) <= 0:
                    monster.live=False
                    self.live=False    
                    explode=Explode(monster)
                    Maingame.explodeList.append(explode)
                else:
                    monster.hp -= (self.dmg+Maingame.my_Character.dmg)
                    monster.live = True
                    self.live = False
    
    

    

    #敌方子弹与我方人物的碰撞    
    def enemyBullet_hit_myCharacter(self):
        if Maingame.my_Character and Maingame.my_Character.live:
            if pygame.sprite.collide_mask(Maingame.my_Character, self):
                if Maingame.my_Character.hp - (self.dmg +Maingame.dmg2) <= 0:
                    explode = Explode(Maingame.my_Character)
                    Maingame.explodeList.append(explode)
                    self.live = False
                    Maingame.my_Character.live = False
                else:
                    Maingame.my_Character.hp-= (self.dmg +Maingame.dmg2)
                    Maingame.my_Character.live = True
                    self.live = False
    
#Wall class
class Wall():
    def __init__(self,left,top):
        #加载墙壁图片
        self.image=pygame.image.load(Maingame.imgwall)
        self.image = pygame.transform.scale(self.image, (60, 60))
        #获取墙壁的区域
        self.rect=self.image.get_rect()
        #设置位置left、top
        self.rect.left=left
        self.rect.top=top
        #是否存活
        self.live=True
        #设置生命值
        self.hp=3
        self.dmg = 0
        self.speed = 0
    #展示墙壁的方法
    def displayWall(self):
        Maingame.window.blit(self.image,self.rect)
    
    # def displayShrine(self):
    #     Maingame.window.blit(self.image,self.rect)
        
#Attack effects class
class Explode():
    def __init__(self,character):
        #爆炸的位置由当前子弹打中的人物位置决定
        self.rect=character.rect
        self.images=[
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
        ]
        self.step=0
        self.image=self.images[self.step]
        #是否活着
        self.live=True

    #展示爆炸效果的方法
    def displayExplode(self):
        if self.step<len(self.images):
            #根据索引获取爆炸对象
            self.image=self.images[self.step]
            self.step+=1
            #添加到主窗口
            Maingame.window.blit(self.image,self.rect)
        else:
            self.live=False
            self.step=0

    #A way to show special effects    
    def displayexplode(self):
        pass


class Room(BaseItem):
    def __init__(self,pos):
        self.image = pygame.Surface((50,50))
        self.image.fill('black')
        self.rect = self.image.get_rect(center = pos)
        self.live = False
        if len(Maingame.enemyList) == 0:
            self.live = True

    def displayRoom(self):
            Maingame.window.blit(self.image,self.rect)
  
#music
class Music():
    def __init__(self,filename):
        self.filename = filename
        pygame.mixer.init()
        channel1 = pygame.mixer.Channel(0)
        channel2 = pygame.mixer.Channel(1)
        pygame.mixer.music.load(self.filename)

    #play music
    def play(self):
        pygame.mixer.music.play()

if __name__=='__main__':
    Maingame().startgame()
    

