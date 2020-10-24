import arcade
import time
import random
import os

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Test-Game"

CHARACTER_SCALING = 0.8
ENEMY_SCALING = 0.3
TILE_SCALING = 0.5
DOOR_SCALING = 1.3
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1.1
PLAYER_JUMP_SPEED = 20

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH/2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH/2
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

MUSIC_VOLUME = 0.5

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
        self.doorTop_list = None
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

        # init level trigger
        self.trigger_list = None

        # init score for keeping track of hits
        self.score = 0

        self.isInteractive = False

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.LIGHT_CYAN)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.doorMid_list = arcade.SpriteList()
        self.doorTop_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.cloud_list = arcade.SpriteList(use_spatial_hash=True)
        self.quote_list = arcade.SpriteList(use_spatial_hash=True)
        self.trigger_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", CHARACTER_SCALING) # example: :resources:images/enemies/slimeBlock.png
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 140
        self.player_list.append(self.player_sprite)

        # List of music
        self.music_list = ["assets\\sounds\\Mellow_Thoughts.mp3", "assets\\sounds\\Lofi.mp3", "assets\\sounds\\Homework.mp3"]
        self.current_song = 0
        self.play_song()

        # Create the ground
        for x in range(0, 1400, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Creates doors to different levels
        for x in range(700, 1250, 250):
            doorMid = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", DOOR_SCALING)
            doorMid.center_x = x
            doorMid.center_y = 147.5
            self.doorMid_list.append(doorMid)

            doorTop = arcade.Sprite(":resources:images/tiles/doorClosed_top.png", DOOR_SCALING)
            doorTop.center_x = x
            doorTop.center_y = 305
            self.doorTop_list.append(doorTop)

        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 1)

        # Spawn a new cloud every 0.75 seconds
        arcade.schedule(self.add_cloud, 0.75)

        # Adding + removing quotes with a viewing interval of 10 seconds
        arcade.schedule(self.add_quote, 15)
        arcade.schedule(self.remove_quote, 20)
        arcade.schedule(self.remove_triggers, 0.02)

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

        # Draw sprites
        self.wall_list.draw()
        self.player_list.draw()
        self.doorMid_list.draw()
        self.doorTop_list.draw()
        self.enemy_list.draw()
        self.cloud_list.draw()
        self.quote_list.draw()
        self.trigger_list.draw()

        start_x = 70
        start_y = 400
        arcade.draw_text("Soothe Yourself", start_x, start_y, arcade.color.BLACK, 60, font_name='GARA')

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 620 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)
                         
    def on_update(self, delta_time):

        self.enemy_list.update()
        self.cloud_list.update()
        self.physics_engine.update()

        if self.player_sprite.center_y <= 100:
            self.player_sprite.center_y = 115
            self.player_sprite.center_x = 64

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
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.music.stop()
            self.window.show_view(pause)

        if self.isInteractive:
            if key == arcade.key.ENTER:
                arcade.load_textures("assets\\images\\loading.png")

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

        cloud = arcade.Sprite("assets\\sprites\\cloud.png", ENEMY_SCALING)
        cloud.center_x = random.randint(0,2400)
        cloud.center_y = 650
        self.cloud_list.append(cloud)
        cloud.velocity = (-2,0)

    def add_enemy(self, delta_time: float):

        enemy = arcade.Sprite(":resources:images/enemies/ladybug.png", ENEMY_SCALING)
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
        trigger.center_y = door_sprite.center_y + 200
        self.trigger_list.append(trigger)

    def remove_triggers(self, delta_time: float):
        for trigger in self.trigger_list:
            trigger.remove_from_sprite_lists()
         
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)
        
    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.ORANGE + (80,))

        # Show PAUSED text and hints on return and exit
        arcade.draw_text("PAUSED", 
                         player_sprite.left+50,
                         SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, 
                         font_size=50, anchor_x="center")

        
        arcade.draw_text("Press Esc. to return",
                         player_sprite.left+50,
                         SCREEN_HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

        arcade.draw_text("Press Enter to go back to main menu",
                         player_sprite.left+50,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # go to main menu
            menu_view = MenuView()
            self.window.show_view(menu_view)

def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Soothe")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()