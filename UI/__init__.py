"""
Platformer Game
"""
import tkinter as tk

import arcade
import pyglet.math

from Mechanic import ModelMechanic
from Mechanic.ObserverPattern.Subscriber import Subscriber
from UI.Player import PlayerCharacter

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Constants
SCREEN_WIDTH = int(screen_width / 1.5)
SCREEN_HEIGHT = int(screen_height / 1.5)
SCREEN_TITLE = "Paul`s days"
PLAYER_MOVEMENT_SPEED = 2

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
VIEWPORT_MARGIN = 100

PLAYER_START_X = 64
PLAYER_START_Y = 128


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
        self.camera_center_x = 0
        self.camera_center_y = 0

        self.mouse_pos_x = PLAYER_START_X
        self.mouse_pos_y = PLAYER_START_X

        self.current_camera_scale = 0.4

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Our TileMap Object
        self.tile_map = None

        self.ui_view_info = UIViewInfo()
        # Keep track of the time
        self.view_changer = ViewChanger(self.ui_view_info)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        super().on_mouse_motion(x, y, dx, dy)
        self.mouse_pos_x = x
        self.mouse_pos_y = y

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)


        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        map_name = 'UI/map.tmx'
        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            },
            "Road": {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.

        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)


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
        elif key == arcade.key.C:
            self.center_camera_to_player()

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

    def move_camera_if_need(self):
        is_need_to_change_pos = False

        if self.mouse_pos_y < float(SCREEN_HEIGHT) * 0.1:
            self.camera_center_y -= 3
            is_need_to_change_pos = True

        if self.mouse_pos_y > float(SCREEN_HEIGHT) * 0.9:
            self.camera_center_y += 3
            is_need_to_change_pos = True

        if self.mouse_pos_x < float(SCREEN_WIDTH) * 0.1:
            self.camera_center_x -= 3
            is_need_to_change_pos = True

        if self.mouse_pos_x > float(SCREEN_WIDTH) * 0.9:
            self.camera_center_x += 3
            is_need_to_change_pos = True

        if ((float(SCREEN_HEIGHT) * 0.1 < self.mouse_pos_y < float(SCREEN_HEIGHT) * 0.9)
                and (float(SCREEN_WIDTH) * 0.1 < self.mouse_pos_x < float(SCREEN_WIDTH) * 0.9)):
            is_need_to_change_pos = False

        if is_need_to_change_pos:
            self.camera.move_to(pyglet.math.Vec2(self.camera_center_x, self.camera_center_y), 0.3)

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()

        # Update Animations
        self.scene.update_animation(
            delta_time, ["Player"]
        )

        self.move_camera_if_need()

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Activate our Camera
        self.camera.use()
        self.camera.scale = self.current_camera_scale

        self.scene.draw()
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

        arcade.draw_text(
            f"({self.player_sprite.center_x},{self.player_sprite.center_y})",
            500,
            10,
            arcade.csscolor.BLACK,
            18,
        )

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        print(f"Mouse ({x},{y})")

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        # if screen_center_x < 0:
        #     screen_center_x = 0
        # if screen_center_y < 0:
        #     screen_center_y = 0
        self.camera_center_x, self.camera_center_y = screen_center_x, screen_center_y
        self.camera.move_to((self.camera_center_x, self.camera_center_y))

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        super().on_mouse_scroll(x, y, scroll_x, scroll_y)
        if scroll_y > 0:
            self.current_camera_scale = 0.1 if (self.current_camera_scale <= 0.15) else self.current_camera_scale - 0.1
        elif scroll_y < 0:
            self.current_camera_scale += 0.1


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
