"""
Platformer Game
"""
import timeit
import tkinter as tk

import arcade
from arcade.examples.camera_platform import TILE_SCALING
from arcade.examples.sprite_move_animation import CHARACTER_SCALING

from Mechanic import ModelMechanic
from Mechanic.ObserverPattern.Subscriber import Subscriber

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Constants
SCREEN_WIDTH = int(screen_width / 1.5)
SCREEN_HEIGHT = int(screen_height / 1.5)
SCREEN_TITLE = "Paul`s days"
PLAYER_MOVEMENT_SPEED = 5


class UIViewInfo:
    def __init__(self):
        self.timer_text_view = ""
        self.mood_text_view = ""
        self.current_state_text_view = ""


class ViewChanger(Subscriber):
    def __init__(self, ui_view_info: UIViewInfo):
        self.mech = ModelMechanic()
        self._ui_view_info = ui_view_info
        self.mech.attach(self)

    def start_changes(self):
        self.mech.start()

    def updateByNotify(self):
        self._ui_view_info.timer_text_view = self.mech.get_current_time_and_date()

    def stop(self):
        self.mech.stop()


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def close(self):
        super().close()
        self.view_changer.stop()


    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Separate variable that holds the player sprite
        self.player_sprite = None
        # Our Scene Object
        self.scene = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        self.ui_view_info = UIViewInfo()
        # Keep track of the time
        self.view_changer = ViewChanger(self.ui_view_info)

        # --- Variables for our statistics

        # Time for on_update
        self.processing_time = 0

        # Time for on_draw
        self.draw_time = 0

        # Variables used to calculate frames per second
        self.frame_count = 0

        self.fps_start_timer = None

        self.fps = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
        self.view_changer.start_changes()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            # arcade.play_sound(self.coin_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        # elif key == arcade.key.C:
        #     # Position the camera
        #     self.center_camera_to_player()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Start timing how long this takes
        start_time = timeit.default_timer()
        # Move the player with the physics engine
        self.physics_engine.update()

        self.center_camera_to_player()

        # Stop the draw timer, and calculate total on_draw time.
        self.processing_time = timeit.default_timer() - start_time

    def on_draw(self):
        """Render the screen."""

        # Start timing how long this takes
        start_time = timeit.default_timer()

        # --- Calculate FPS
        fps_calculation_freq = 60

        # Once every 60 frames, calculate our FPS
        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()
        # Add one to our frame count
        self.frame_count += 1
        self.clear()
        self.scene.draw()

        # Activate our Camera
        self.camera.use()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.ui_view_info.timer_text_view}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"

        arcade.draw_text(output, 20, SCREEN_HEIGHT - 25, arcade.color.BLACK, 18)

        output = f"Drawing time: {self.draw_time:.3f}"

        arcade.draw_text(output, 20, SCREEN_HEIGHT - 50, arcade.color.BLACK, 18)

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 75, arcade.color.BLACK, 18)

        # Stop the draw timer, and calculate total on_draw time.
        self.draw_time = timeit.default_timer() - start_time

        # Code to draw the screen goes here

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
