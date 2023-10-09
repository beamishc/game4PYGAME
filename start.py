import pygame
import pytmx
import pyscroll
import os
from gameobject_class import GameObject
from playercharacter_class import PC
from nonplayercharacter_class import NPC

# print(pygame.font.get_fonts())

# size of the game screen
SCREEN_TITLE = 'Ghost Town'
SCREEN_WIDTH = 816
SCREEN_HEIGHT = 816
PRE_PLAYER = 'assets/Tiles/tile_0121.png'
PLAYER = 'assets/Tiles/tile_0119.png'
GHOSTS = 'assets/Tiles/tile_0125.png'
SWORD = 'assets/Tiles/tile_0126.png'
TREASURE = 'assets/Tiles/tile_0134.png'
HALFLIFE = 'assets/Tiles/tile_0128.png'
HEARTLESS = 'assets/Tiles/tile_0127.png'
BACKGROUND = '/Users/cbeams/code/game-builds/monochrome_1.tmx'

# RGB color codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# define the clock
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('baskerville', 96, bold=True)

class Game:
    # Typical rate of 60 , equivalent to FPS
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height, player_image, enemy_image, treasure_image, sword_image, pre_player_image):
        self.title = title
        self.image = BACKGROUND
        self.width = width
        self.height = height
        self.player_image = player_image
        self.enemy_image = enemy_image
        self.sword_image = sword_image
        self.treasure_image = treasure_image
        self.pre_player_image = pre_player_image
        self.sign = 'assets/Tiles/tile_0067.png'
        self.heart = 'assets/Tiles/tile_0129.png'
        self.halflife = 'assets/Tiles/tile_0128.png'
        self.heartless = 'assets/Tiles/tile_0127.png'
        self.health = 6
        self.damage_taken = False

        # create the game screen
        self.game_screen = pygame.display.set_mode((width, height))

        # set the game screen to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        # background_image = pygame.image.load(image_path)
        # self.image = pygame.transform.scale(background_image, (width, height))

        # tmxdata = pytmx.TiledMap(BACKGROUND)
        self.gameMap = pytmx.load_pygame(self.image)

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0
        px_h = 48
        px_w = 48

        # 'source_files/project_files/player.png'
        player_character = PC(self.pre_player_image, 384, 720, px_h, px_w)
        if level_speed >= 1:
            player_character = PC(self.player_image, 384, 720, px_h, px_w)

        # 'source_files/project_files/enemy.png'
        enemy_0 = NPC(self.enemy_image, 24, 624, px_h, px_w)
        enemy_0.SPEED *= level_speed

        enemy_1 = NPC(self.enemy_image, self.width - 48, 384, px_h, px_w)
        enemy_1.SPEED *= level_speed

        enemy_2 = NPC(self.enemy_image, 24, 192, px_h, px_w)
        enemy_2.SPEED *= level_speed

        # 'source_files/project_files/treasure.png'
        treasure = GameObject(self.treasure_image, 384, 48, px_h, px_w)
        sword = GameObject(self.sword_image, 384, 48, px_h, px_w)

        signage = GameObject(self.sign, 336, 672, px_h, px_w)

        heart1_x = self.width - 144
        heart2_x = self.width - 96
        heart3_x = self.width - 48
        heart_y = 0

        heart1 = GameObject(self.heart, heart1_x, heart_y, px_h, px_w)
        heart2 = GameObject(self.heart, heart2_x, heart_y, px_h, px_w)
        heart3 = GameObject(self.heart, heart3_x, heart_y, px_h, px_w)

        # Main loop of game - runs until is_game_over == True
        while not is_game_over:

            # checks all events that occur
            for event in pygame.event.get():

                # quit event closes game
                if event.type == pygame.QUIT:
                    is_game_over = True

                # detect when key pressed
                elif event.type == pygame.KEYDOWN:

                    # move forward if key up pressed
                    if event.key ==pygame.K_UP:
                        direction = 1

                    # move back if key up pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1

                # detect when key lifted
                elif event.type == pygame.KEYUP:

                    # stop moving when key lifted
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

                # print(event)

            # Clear screen
            self.game_screen.fill(WHITE_COLOR)
            for layer in self.gameMap.visible_layers:
                for x, y, gid, in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if(tile != None):
                        self.game_screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

            if level_speed == 1:
                sword.draw(self.game_screen)
            else:
                treasure.draw(self.game_screen)

            signage.draw(self.game_screen)

            heart1.draw(self.game_screen)
            heart2.draw(self.game_screen)
            heart3.draw(self.game_screen)

            # Update player position
            player_character.move(direction, self.height)

            # Display player at new position
            player_character.draw(self.game_screen)

            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)

            if level_speed > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            collision = sum([player_character.detect_collision(enemy_0)
                             , player_character.detect_collision(enemy_1)
                             , player_character.detect_collision(enemy_2)])

            if collision > 0 and self.damage_taken == False:
                self.game_screen.fill((255,0,0))
                self.health -= 1

            if self.health == 5:
                self.damage_taken = True
                heart3 = GameObject(self.halflife, heart3_x, heart_y, px_h, px_w)

            if self.health == 4:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w)

            if self.health == 3:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w)
                heart2 = GameObject(self.halflife, heart2_x, heart_y, px_h, px_w)

            if self.health == 2:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w)
                heart2 = GameObject(self.heartless, heart2_x, heart_y, px_h, px_w)

            if self.health == 1:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w)
                heart2 = GameObject(self.heartless, heart2_x, heart_y, px_h, px_w)
                heart1 = GameObject(self.halflife, heart1_x, heart_y, px_h, px_w)

            if collision == 0:
                self.damage_taken = False

            if self.health == 0:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w)
                heart2 = GameObject(self.heartless, heart2_x, heart_y, px_h, px_w)
                heart1 = GameObject(self.heartless, heart1_x, heart_y, px_h, px_w)
                is_game_over = True
                did_win = False
                text = font.render('YOU LOSE!', True, BLACK_COLOR)
                self.game_screen.blit(text, (200, 350))
                pygame.display.update()
                clock.tick(1)
                break

            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('YOU WIN!', True, BLACK_COLOR)
                self.game_screen.blit(text, (200, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # updates all game graphics
            pygame.display.update()
            # tick the clock to update everything in the game
            clock.tick(self.TICK_RATE)

        if did_win:
            self.player_image = 'assets/Tiles/tile_0119.png'
            self.run_game_loop(level_speed + 0.5)
        else:
            return


# initialise game
pygame.init()


new_game = Game('source_files/project_files/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, PRE_PLAYER, GHOSTS, TREASURE, SWORD, PRE_PLAYER)
new_game.run_game_loop(1)
# new_game2 = Game('source_files/project_files/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, 'assets/player.png', 'assets/dragon.png', 'assets/treasure.png')
# new_game2.run_game_loop(1)


# end game
pygame.quit()
quit()
