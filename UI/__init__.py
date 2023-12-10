"""
Platformer Game
"""
import tkinter as tk

import arcade
import pyglet.math

from Mechanic import ModelMechanic
from Mechanic.Mood import Mood
from Mechanic.ObserverPattern.Subscriber import Subscriber
from Mechanic.WeekTimer import TimerSpeedStates
from Mechanic.states.STATE_NAMES import STATES
from UI.Player import PlayerCharacter

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Constants
SCREEN_WIDTH = int(screen_width / 1.3)
SCREEN_HEIGHT = int(screen_height / 1.3)
SCREEN_TITLE = "Paul`s days"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5

SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

PLAYER_START_X = 360
PLAYER_START_Y = 150


class MechanicWithUiSharedData:
    def __init__(self):
        self.timer_text_view = ""
        self.mood_text_view = Mood.NORMAL
        self.current_state_text_view = STATES.SLEEP
        self.is_able_to_change_mood = False
        self.time_speed = TimerSpeedStates.NORMAL


class ViewChanger(Subscriber):
    def __init__(self, ui_view_info: MechanicWithUiSharedData):
        self.mech = ModelMechanic()
        self._ui_view_info = ui_view_info
        self.mech.attach(self)

    def set_new_time_speed(self, new_time_speed: TimerSpeedStates):
        self.mech.set_new_time_speed(new_time_speed)

    def set_new_mood(self, new_mood: Mood):
        self.mech.set_mood_fast(new_mood)

    def start_changes(self):
        self.mech.start()

    def updateByNotify(self):
        self._ui_view_info.timer_text_view = self.mech.get_current_time_and_date()
        self._ui_view_info.mood_text_view = self.mech.get_mood()
        self._ui_view_info.current_state_text_view, self._ui_view_info.is_able_to_change_mood = self.mech.get_state()
        self._ui_view_info.time_speed = self.mech.get_time_speed()

    def stop(self):
        self.mech.stop()

    def is_able_to_change_mood(self):
        return self._ui_view_info.is_able_to_change_mood

    def check_set_ability_to_change_mood(self, ability):
        self._ui_view_info.is_able_to_change_mood = ability


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
        self.center_window()
        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.destinations = {
            STATES.SLEEP: (472, 246),
            STATES.EAT: (464, 318),
            STATES.REST: (250, 172),
            STATES.UNIVERSITY: (986, 689),
            STATES.ROAD: (378, 575),
            STATES.PC: (482, 156),
            STATES.HOBBY: (275, 298),
            STATES.WALK: (776, 362),
        }

        # --- Related to paths
        # List of points that makes up a path between two points
        self.path = None
        # List of points we checked to see if there is a barrier there
        self.barrier_list = None

        # Our Scene Object
        self.scene = None

        # A Camera that can be used for scrolling the screen
        self.camera = None
        self.camera_center_x = 0
        self.camera_center_y = 0
        self.is_camera_follow_player = False

        self.mouse_pos_x = PLAYER_START_X
        self.mouse_pos_y = PLAYER_START_X

        self.current_camera_scale = 1  # 0.25

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Our TileMap Object
        self.tile_map = None

        # MECHANIC
        self.mech_ui_shared_data = MechanicWithUiSharedData()
        self.view_changer = ViewChanger(self.mech_ui_shared_data)
        # MECHANIC

        # self.destination_point = self.destinations[self.mech_ui_shared_data.current_state_text_view]
        self.destination_point = None
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
            },
            "GroundUnderRails": {
                "use_spatial_hash": True
            },
            "Decorations": {
                "use_spatial_hash": True
            },
            "UpperDecor": {
                "use_spatial_hash": True
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.

        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.set_new_player_speed_by_time_velocity(self.mech_ui_shared_data.time_speed)
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
        self.view_changer.start_changes()

        self.path = None
        # Grid size for calculations. The smaller the grid, the longer the time
        # for calculations. Make sure the grid aligns with the sprite wall grid,
        # or some openings might be missed.
        grid_size = 16

        # Calculate the playing field size. We can't generate paths outside of
        # this.
        playing_field_left_boundary = -SCREEN_WIDTH
        playing_field_right_boundary = SCREEN_WIDTH
        playing_field_top_boundary = SCREEN_HEIGHT
        playing_field_bottom_boundary = -SCREEN_HEIGHT

        # This calculates a list of barriers. By calculating it here in the
        # init, we are assuming this list does not change. In this example,
        # our walls don't move, so that is ok. If we want moving barriers (such as
        # moving platforms or enemies) we need to recalculate. This can be an
        # time-intensive process depending on the playing field size and grid
        # resolution.

        # Note: If the enemy sprites are the same size, we only need to calculate
        # one of these. We do NOT need a different one for each enemy. The sprite
        # is just used for a size calculation.
        self.barrier_list = arcade.AStarBarrierList(self.player_sprite,
                                                    self.scene.get_sprite_list("Walls"),
                                                    grid_size,
                                                    playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    playing_field_bottom_boundary,
                                                    playing_field_top_boundary)
        print("test")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = self.player_sprite.speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -self.player_sprite.speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -self.player_sprite.speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = self.player_sprite.speed
        elif key == arcade.key.C:
            self.is_camera_follow_player = True
        elif key == arcade.key.KEY_1:
            self.view_changer.set_new_time_speed(TimerSpeedStates.SLOW)
        elif key == arcade.key.KEY_2:
            self.view_changer.set_new_time_speed(TimerSpeedStates.NORMAL)
        elif key == arcade.key.KEY_3:
            self.view_changer.set_new_time_speed(TimerSpeedStates.SEMIFAST)
        elif key == arcade.key.KEY_4:
            self.view_changer.set_new_time_speed(TimerSpeedStates.FAST)
        elif key == arcade.key.KEY_0:
            self.destination_point = None
        elif key == arcade.key.H:
            self.view_changer.check_set_ability_to_change_mood(False)
        elif key == arcade.key.Y:
            self.view_changer.check_set_ability_to_change_mood(True)
        elif key == arcade.key.B:
            if self.view_changer.is_able_to_change_mood():
                self.view_changer.set_new_mood(Mood.BAD)
        elif key == arcade.key.N:
            if self.view_changer.is_able_to_change_mood():
                self.view_changer.set_new_mood(Mood.NORMAL)
        elif key == arcade.key.G:
            if self.view_changer.is_able_to_change_mood():
                self.view_changer.set_new_mood(Mood.GOOD)

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
        elif key == arcade.key.C:
            self.is_camera_follow_player = False

    def move_camera_if_need(self):
        is_need_to_change_pos = False
        camera_delta = 5

        if self.mouse_pos_y < float(SCREEN_HEIGHT) * 0.1:
            self.camera_center_y -= camera_delta
            is_need_to_change_pos = True

        if self.mouse_pos_y > float(SCREEN_HEIGHT) * 0.9:
            self.camera_center_y += camera_delta
            is_need_to_change_pos = True

        if self.mouse_pos_x < float(SCREEN_WIDTH) * 0.1:
            self.camera_center_x -= camera_delta
            is_need_to_change_pos = True

        if self.mouse_pos_x > float(SCREEN_WIDTH) * 0.9:
            self.camera_center_x += camera_delta
            is_need_to_change_pos = True

        if ((float(SCREEN_HEIGHT) * 0.1 < self.mouse_pos_y < float(SCREEN_HEIGHT) * 0.9)
                and (float(SCREEN_WIDTH) * 0.1 < self.mouse_pos_x < float(SCREEN_WIDTH) * 0.9)):
            is_need_to_change_pos = False

        if is_need_to_change_pos:
            self.camera.move_to(pyglet.math.Vec2(self.camera_center_x, self.camera_center_y), 0.4)

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()

        # Set to True if we can move diagonally. Note that diagonal movement
        # might cause the enemy to clip corners.
        if self.destination_point:
            self.path = arcade.astar_calculate_path((self.player_sprite.center_x, self.player_sprite.center_y),
                                                    self.destination_point,
                                                    self.barrier_list,
                                                    diagonal_movement=False)
        else:
            self.path = None

        if self.path and len(self.path) > 1:
            self.player_sprite.move_to_path(self.path[1])
        else:
            if self.destination_point:
                self.player_sprite.stop_player()

        # Update Animations
        self.scene.update_animation(
            delta_time, ["Player"]
        )

        self.destination_point = self.destinations[self.mech_ui_shared_data.current_state_text_view]
        self.player_sprite.set_new_player_speed_by_time_velocity(self.mech_ui_shared_data.time_speed)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Activate our Camera
        self.camera.use()
        if self.is_camera_follow_player:
            self.center_camera_to_player()

        self.scene.draw()
        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()
        # Draw our score on the screen, scrolling it with the viewport

        arcade.draw_text(
            f"Time: {self.mech_ui_shared_data.timer_text_view}",
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

        arcade.draw_text(
            f"Mood: {self.mech_ui_shared_data.mood_text_view.name}",
            400,
            10,
            arcade.csscolor.GREEN if (self.view_changer.is_able_to_change_mood()) else arcade.csscolor.RED,
            18,
        )

        arcade.draw_text(
            f"({self.player_sprite.center_x},{self.player_sprite.center_y})",
            600,
            10,
            arcade.csscolor.BLACK,
            18,
        )

        arcade.draw_text(
            f"State: {self.mech_ui_shared_data.current_state_text_view.name}",
            1000,
            10,
            arcade.csscolor.BLACK,
            18,
        )

        if self.path:
            self.move_path_by_camera()
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

        self.move_camera_if_need()
        self.camera.scale = self.current_camera_scale

    def move_path_by_camera(self):
        for i in range(len(self.path)):
            self.path[i] = (self.path[i][0] - self.camera_center_x,
                            self.path[i][1] - self.camera_center_y)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        print(f"Mouse ({x},{y})")

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )
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
