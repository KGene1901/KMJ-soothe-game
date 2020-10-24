import arcade
import random
import time

# Constants
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
PLAYER_MOVEMENT_SPEED = 13
GRAVITY = 1.3
PLAYER_JUMP_SPEED = 20

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

MUSIC_VOLUME = 0.5


class SootheGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.music_list = []
        self.current_song = 0
        self.music = None

        # sprit lists
        self.wall_list = None
        self.player_list = None
        self.doorMid_list = None
        self.doorTop_list = None
        self.enemy_list = None
        self.cloud_list = None

        self.physics_engine = None

        self.player_sprite = None

        self.view_bottom = 0
        self.view_left = 0

        self.hit_enemy_sound = arcade.load_sound("test-game-KG/sounds/Bubble-wrap-popping.mp3")
        # self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.LIGHT_CYAN)

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

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.doorMid_list = arcade.SpriteList()
        self.doorTop_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.cloud_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", CHARACTER_SCALING) # example: :resources:images/enemies/slimeBlock.png
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 115
        self.player_list.append(self.player_sprite)

        # List of music
        self.music_list = ["test-game-KG/sounds/2020-09-14_-_Mellow_Thoughts_-_www.FesliyanStudios.com_David_Renda.mp3", "test-game-KG/sounds/relaxing lofi for late nights...😴 (128 kbps).mp3", "test-game-KG/sounds/2019-06-12_-_Homework_-_David_Fesliyan.mp3"]
        self.current_song = 0
        self.play_song()

        # Create the ground
        for x in range(0, 2000, 64):
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
        arcade.schedule(self.add_enemy, 1.2)

        # Spawn a new cloud every 0.75 seconds
        arcade.schedule(self.add_cloud, 0.75)

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

    def add_enemy(self, delta_time: float):

        enemy = arcade.Sprite(":resources:images/enemies/ladybug.png", ENEMY_SCALING)
        enemy.center_x = random.randint(100,2000)
        enemy.center_y = 70
        self.enemy_list.append(enemy)
        enemy.velocity = (random.randint(-20, -5), 0)


    def add_cloud(self, delta_time: float):

        cloud = arcade.Sprite("test-game-KG/sprites/198daeda14097d45e417e62ff283f10e.png", ENEMY_SCALING)
        cloud.center_x = random.randint(0,2400)
        cloud.center_y = 650
        self.cloud_list.append(cloud)
        cloud.velocity = (-2,0)

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

        start_x = 70
        start_y = 400
        arcade.draw_text("Soothe Yourself", start_x, start_y, arcade.color.BLACK, 60, font_name='GARA')

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                # arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
    
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



def main():
    window = SootheGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()