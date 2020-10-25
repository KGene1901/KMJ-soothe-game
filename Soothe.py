import arcade
import time
import random
import os

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Test-Game"

CHARACTER_SCALING = 2.5
ENEMY_SCALING = 3
CLOUD_SCALING = 0.3
TILE_SCALING = 0.5
DOOR_SCALING = 0.42
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player
PLAYER_MOVEMENT_SPEED = 7
SPECIAL_SPEED = 1
GRAVITY = 1.7
PLAYER_JUMP_SPEED = 20

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH/2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH/2
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 300
MUSIC_VOLUME = 0.1

class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self):
        super().__init__()

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.LIGHT_CYAN)
        arcade.set_viewport(0,SCREEN_WIDTH,0,SCREEN_HEIGHT)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text("Soothe", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,arcade.color.PINK, font_size=50, anchor_x="center")
        arcade.draw_text("Press any key to advance.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """ Use a key press to advance to the 'game' view. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameView(arcade.View):
    """ Manage the 'game' view for our program. """
    def __init__(self):

        super().__init__()

        # music
        self.music_list = []
        self.current_song = 0
        self.music = None

        # sprite lists
        self.wall_list = None
        self.player_list = None
        self.doorMid_list = None
        self.endDoor_list = None
        self.drawer_list = None
        self.bottomWall_list = None
        self.window_list = None
        self.enemy_list = None
        self.cloud_list = None

        # initiating physics engine
        self.physics_engine = None

        # init player sprite
        self.player_sprite = None

        # init viewports
        self.view_bottom = 0
        self.view_left = 0

        self.hit_enemy_sound = arcade.load_sound("assets\\sounds\\Bubble-wrap-popping.mp3")
        # self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # init quotes sprite
        self.quote_list = None
        self.quotes = []
        self.current_quote = 0 

        # init dialogue
        self.dialogue_list = None

        # init level trigger
        self.trigger_list = None

        # init score for keeping track of hits
        self.score = 0

        # init interactive settings
        self.isInteractive = False

        # init personalized bg
        self.background = None
        self.background2 = None

        # init level selector
        self.levelSelector = 0

        self.slowDown = False

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color((153, 178, 188))

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.background = arcade.load_texture("assets\\images\\Background\\stress_background_png.png")
        self.background2 = arcade.load_texture("assets\\images\\Background\\computer_breaker_nodithering.png")
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedWalkingSprite()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.doorMid_list = arcade.SpriteList()
        self.endDoor_list= arcade.SpriteList()
        self.bottomWall_list = arcade.SpriteList(use_spatial_hash=True)
        self.window_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list = arcade.SpriteList()
        self.cloud_list = arcade.SpriteList(use_spatial_hash=True)
        self.quote_list = arcade.SpriteList(use_spatial_hash=True)
        self.trigger_list = arcade.SpriteList(use_spatial_hash=True)
        self.drawer_list = arcade.SpriteList(use_spatial_hash=True)
        self.dialogue_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player
        # self.player_sprite = arcade.Sprite("assets\\sprites\\player_sprite\\idle1.png", CHARACTER_SCALING) # example: :resources:images/enemies/slimeBlock.png
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 3400
        self.player_sprite.scale = CHARACTER_SCALING
        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\right_idle1.png"))
        self.player_sprite.stand_right_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\right_idle2.png"))
        self.player_sprite.stand_left_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\right_idle1.png", mirrored=True))
        self.player_sprite.stand_left_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\right_idle2.png", mirrored=True))

        self.player_sprite.walk_right_textures = []
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right1.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right2.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right3.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right4.png"))

        self.player_sprite.walk_left_textures = []
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right1.png", mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right2.png", mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right3.png", mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets\\sprites\\player_sprite\\walk-right4.png", mirrored=True))

        self.player_list.append(self.player_sprite)

        # List of music
        self.music_list = ["assets\\sounds\\Mellow_Thoughts.mp3", "assets\\sounds\\Lofi.mp3", "assets\\sounds\\Homework.mp3"]
        self.current_song = 0
        self.play_song()

        # Create the ground
        for x in range(0, 2000, 64):
            wall= arcade.Sprite("assets\\sprites\\lobby_floor.png", 0.15)
            wall.center_x = x
            wall.center_y = 3000
            self.wall_list.append(wall)

            wall = arcade.Sprite("assets\\sprites\\grass_tile.png", 2)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        for x in range(0, 18000, 64):
            wall= arcade.Sprite("assets\\sprites\\white_tile.png", 4)
            wall.center_x = x
            wall.center_y = -3000
            self.wall_list.append(wall)
        
        # Creates doors to different levels
        for x in range(700, 1250, 250):
            doorMid = arcade.Sprite("assets\\sprites\\door.png", DOOR_SCALING)
            doorMid.center_x = x
            doorMid.center_y = 3110
            self.doorMid_list.append(doorMid)

        endDoor = arcade.Sprite("assets\\sprites\\door.png", DOOR_SCALING)
        endDoor.center_x = 1900
        endDoor.center_y = 130
        self.endDoor_list.append(endDoor)

        endDoor = arcade.Sprite("assets\\sprites\\door.png", DOOR_SCALING)
        endDoor.center_x = 17412
        endDoor.center_y = -2900
        self.endDoor_list.append(endDoor)

        # Creates drawers
        for x in range(825, 1300, 250):
            drawer = arcade.Sprite("assets\\sprites\\drawer.png", DOOR_SCALING-0.1)
            drawer.center_x = x
            drawer.center_y = 3080
            self.drawer_list.append(drawer)

        # Creates bottom lining of wall
        for x in range(44, 1954, 10):
            lining = arcade.Sprite("assets\\sprites\\bottom-wall.png", DOOR_SCALING-0.1)
            lining.center_x = x
            lining.center_y = 3046.5
            self.bottomWall_list.append(lining)


        # creating windows
        window = arcade.Sprite("assets\\sprites\\lobby_window.png", DOOR_SCALING-0.1)
        window.center_x = 100
        window.center_y = 3121
        self.window_list.append(window)

        window = arcade.Sprite("assets\\sprites\\lobby_window.png", DOOR_SCALING-0.1)
        window.center_x = 400
        window.center_y = 3121
        self.window_list.append(window)
        
        window = arcade.Sprite("assets\\sprites\\lobby_window.png", DOOR_SCALING-0.1)
        window.center_x = 1500
        window.center_y = 3121
        self.window_list.append(window)

        window = arcade.Sprite("assets\\sprites\\lobby_window.png", DOOR_SCALING-0.1)
        window.center_x = 1800
        window.center_y = 3121
        self.window_list.append(window)


        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 1)

        # Spawn a new cloud every 0.75 seconds
        arcade.schedule(self.add_cloud, 0.75)

        # Adding + removing quotes with a viewing interval of 10 seconds
        arcade.schedule(self.add_quote, 15)
        arcade.schedule(self.remove_quote, 10)
        arcade.schedule(self.remove_triggers, 0.02)
        # arcade.schedule(self.reset_level_selector, 2)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        # coordinate_list = [[256, 96],
        #                    [512, 96],
        #                    [768, 96]]

        # for coordinate in coordinate_list:
        #     # Add a crate on the ground
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
        #     wall.position = coordinate
        #     self.wall_list.append(wall)

        pass

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(-500, 0,
                                            SCREEN_WIDTH+2000, SCREEN_HEIGHT+200,
                                            self.background)
        arcade.draw_lrwh_rectangle_textured(-500, -3100,
                                            SCREEN_WIDTH+18000, SCREEN_HEIGHT+300,
                                            self.background2)

        # Draw sprites
        self.bottomWall_list.draw()
        self.doorMid_list.draw()
        self.endDoor_list.draw()
        self.drawer_list.draw()
        self.window_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.cloud_list.draw()
        self.quote_list.draw()
        self.trigger_list.draw()
        self.dialogue_list.draw()

        arcade.draw_text("Soothe", 70, 3400, arcade.color.BLACK, 60, font_name='GARA')
        arcade.draw_text("Stress Reliever", 70, 400, arcade.color.BLACK, 60, font_name='GARA')
        arcade.draw_text("Enlighten", 70, -2650, arcade.color.WHITE, 60, font_name='GARA')

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 634,
                         arcade.csscolor.BLACK, 18)
                         
    def on_update(self, delta_time):

        self.player_list.update()
        self.player_list.update_animation()
        self.enemy_list.update()
        self.cloud_list.update()
        self.physics_engine.update()

        if self.levelSelector != 2:
            if self.player_sprite.center_x < -20 or self.player_sprite.center_x > 2000:
                if self.levelSelector == 0:
                        self.player_sprite.center_x = 64
                        self.player_sprite.center_y = 3400
                elif self.levelSelector == 1:
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = 92
        else:
            if self.player_sprite.center_x < -20 or self.player_sprite.center_x > 18000:
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = -2900

        for enemy in self.enemy_list:
            if enemy.center_x < 40:
                enemy.remove_from_sprite_lists()

        position = self.music.get_stream_position()
        if position == 0.0:
            self.advance_song()
            self.play_song()

        # See if we hit any enemy
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.enemy_list)

        # Loop through each coin we hit (if any) and remove it
        for enemy in enemy_hit_list:
            # Remove the coin
            enemy.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.hit_enemy_sound)
            self.score += 1

        door_collision_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.doorMid_list)

        for hit in door_collision_list:
            self.add_triggers(hit)
            self.isInteractive = True
            if hit.center_x == 700:
                self.levelSelector = 1
            elif hit.center_x == 950:
                self.levelSelector = 2
                self.slowDown = True

        endDoor_collision_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.endDoor_list)

        for hit in endDoor_collision_list:
            self.add_return_trigger(hit)
            self.isInteractive = True
            self.levelSelector = 0

        # create user-location based dialogue for level 2 
        if self.player_sprite.center_y <= -2000:
            if self.player_sprite.center_x == 100:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase1.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 200
                self.dialogue_list.append(dialog)

            elif self.player_sprite.center_x == 852:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase2.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x - 200
                dialog.center_y = self.player_sprite.center_y + 350
                self.dialogue_list.append(dialog) 

                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase3.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x - 100
                dialog.center_y = self.player_sprite.center_y + 200
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 900:
                dialog = arcade.Sprite("assets\\sprites\\stressed_out_drawing.png", 1.5)
                dialog.center_x = self.player_sprite.center_x + 300
                dialog.center_y = self.player_sprite.center_y + 200
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 1504:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase4.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 300
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 1800:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase5.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 200
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 2356:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase6.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 400
                self.dialogue_list.append(dialog)
                
                world_burning = arcade.Sprite("assets\\sprites\\earth_burning.png", 1)
                world_burning.center_x = self.player_sprite.center_x
                world_burning.center_y = self.player_sprite.center_y + 200
                self.dialogue_list.append(world_burning)

            elif self.player_sprite.center_x == 3140:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase7.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 500
                self.dialogue_list.append(dialog) 

                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase8.png", TILE_SCALING)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog)

            elif self.player_sprite.center_x == 4040:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase9.png", 1.3)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 300
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 5000:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase10.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 300
                self.dialogue_list.append(dialog) 

                ## spawns in friend here ##
            elif self.player_sprite.center_x == 5800:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase11.png", 0.7)
                dialog.center_x = self.player_sprite.center_x + 200
                dialog.center_y = self.player_sprite.center_y + 300
                self.dialogue_list.append(dialog) 

                 ## spawns in friend here ##
            elif self.player_sprite.center_x == 6900:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase12.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 400
                self.dialogue_list.append(dialog) 

                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase13.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 300
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 8032:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase14.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 400
                self.dialogue_list.append(dialog) 

                self_love = arcade.Sprite("assets\\sprites\\self_love.png", 1)
                self_love.center_x = self.player_sprite.center_x
                self_love.center_y = self.player_sprite.center_y + 190
                self.dialogue_list.append(self_love) 
            
            elif self.player_sprite.center_x == 9004:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase15.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 250
                self.dialogue_list.append(dialog) 
            
            elif self.player_sprite.center_x == 9460:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase16.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 10684:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase17.png", 0.8)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 
            
            elif self.player_sprite.center_x == 11624:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase18.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 12812:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase19.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 420
                self.dialogue_list.append(dialog)

                hope = arcade.Sprite("assets\\sprites\\hope.png", 1)
                hope.center_x = self.player_sprite.center_x
                hope.center_y = self.player_sprite.center_y + 260
                self.dialogue_list.append(hope)  

                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase20.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 100
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 13536:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase21.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 
            
            elif self.player_sprite.center_x == 14520:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase22.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 

            elif self.player_sprite.center_x == 15064:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase23.png", 0.7)
                dialog.center_x = self.player_sprite.center_x
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 
            
            elif self.player_sprite.center_x == 16728:
                self.reset_array(self.dialogue_list)
                dialog = arcade.Sprite("assets\\sprites\\level-2-phrases\\phrase24.png", 0.5)
                dialog.center_x = self.player_sprite.center_x + 110
                dialog.center_y = self.player_sprite.center_y + 150
                self.dialogue_list.append(dialog) 


            
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
    
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                # arcade.play_sound(self.jump_sound)

        elif key == arcade.key.LEFT or key == arcade.key.A:
            if not self.slowDown:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            else:
                if self.player_sprite.center_y <= -2000:
                    self.player_sprite.change_x = -SPECIAL_SPEED
                else:
                    self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if not self.slowDown:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            else:
                if self.player_sprite.center_y <= -2000:
                    self.player_sprite.change_x = SPECIAL_SPEED
                else:
                    self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.music.stop()
            self.window.show_view(pause)

        if self.isInteractive:
            if key == arcade.key.ENTER:
                if self.levelSelector == 0:
                    self.score = 0
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = 3400
                elif self.levelSelector == 1:
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = 92
                elif self.levelSelector == 2:
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = -2900

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.ENTER:
            self.isInteractive = False

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        self.current_song += 1
        if self.current_song >= len(self.music_list):
            self.current_song = 0
        print(f"Advancing song to {self.current_song}.")

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        print(f"Playing {self.music_list[self.current_song]}")
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(MUSIC_VOLUME)
        time.sleep(0.03)

    def add_cloud(self, delta_time: float):

        cloud = arcade.Sprite("assets\\sprites\\cloud.png", CLOUD_SCALING)
        cloud.center_x = random.randint(0,2400)
        cloud.center_y = random.randint(600,650)
        self.cloud_list.append(cloud)
        cloud.velocity = (-2,0)

    def add_enemy(self, delta_time: float):

        enemy = arcade.Sprite("assets\\sprites\\squish.png", ENEMY_SCALING)
        enemy.center_x = random.randint(100,2000)
        enemy.center_y = 70
        self.enemy_list.append(enemy)
        enemy.velocity = (random.randint(-15, -2), 0)

    def add_quote(self, delta_time: float):

        self.quotes = ["assets\\quotes\\9ff607bc2e850fef7bc06478dba885e9.png", "assets\\quotes\\d6360d549c2b85fd4ec30cc44b0af930.png", "assets\\quotes\\3540c344e617725d1a26fe3b4332048c.png", "assets\\quotes\\9ff607bc2e850fef7bc06478dba885e9.png"]
        self.current_quote = random.randint(0, len(self.quotes)-1)
        quote = arcade.Sprite(self.quotes[self.current_quote], TILE_SCALING)
        player_pos = self.player_sprite.center_x
        quote.center_x = 1000
        quote.center_y = 30
        self.quote_list.append(quote)

    def remove_quote(self, delta_time: float):
        for quote in self.quote_list:
            quote.remove_from_sprite_lists()

    def add_triggers(self, door_sprite):
        trigger = arcade.Sprite("assets\\sprites\\level-trigger.png", TILE_SCALING)
        trigger.center_x = door_sprite.center_x
        trigger.center_y = door_sprite.center_y + 120
        self.trigger_list.append(trigger)

    def remove_triggers(self, delta_time: float):
        for trigger in self.trigger_list:
            trigger.remove_from_sprite_lists()
         
    def add_return_trigger(self, door_sprite):
        trigger = arcade.Sprite("assets\\sprites\\return_trigger.png", TILE_SCALING)
        trigger.center_x = door_sprite.center_x
        trigger.center_y = door_sprite.center_y + 120
        self.trigger_list.append(trigger)

    def reset_level_selector(self, delta_time: float):
        self.levelSelector = 0

    def reset_array(self, sprite_array):
        for item in sprite_array:
            item.remove_from_sprite_lists()

class PauseView(arcade.View):
    def __init__(self, game_view):

        super().__init__()
        self.game_view = game_view
    
    # Called when switching to this view
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)
    
    # Render the screen
    def on_draw(self):
        arcade.start_render()

        # Draw player on pause screen
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # Draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.ORANGE + (80,))

        # Show PAUSED text and hints on return and exit
        arcade.draw_text("PAUSED", 
                         player_sprite.center_x,
                         player_sprite.center_y+130,
                         arcade.color.BLACK, 
                         font_size=50, anchor_x="center")

        
        arcade.draw_text("Press Esc. to return",
                         player_sprite.center_x,
                         player_sprite.center_y+100,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        
        arcade.draw_text("Press Enter to go back to main menu",
                         player_sprite.center_x,
                         player_sprite.center_y+80,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    # Detect individual key presses
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # go to main menu
            menu_view = MenuView()
            self.score = 0
            self.window.show_view(menu_view)

def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Soothe")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()