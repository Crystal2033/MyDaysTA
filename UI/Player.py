"""
Platformer Game

python -m arcade.examples.platform_tutorial.11_animate_character
"""
import math

import arcade

from Mechanic.WeekTimer import TimerSpeedStates

# Constants used to scale our sprites from their original size

CHARACTER_SCALING = 5 / 30

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


SLOW_SPEED = 2
NORMAL_SPEED = 4
SEMIFAST_SPEED = 8
FAST_SPEED = 16

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        self.speed = NORMAL_SPEED

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]

    def set_new_player_speed_by_time_velocity(self, time_speed: TimerSpeedStates):
        if time_speed == TimerSpeedStates.SLOW:
            self.speed = SLOW_SPEED
        elif time_speed == TimerSpeedStates.NORMAL:
            self.speed = NORMAL_SPEED
        elif time_speed == TimerSpeedStates.SEMIFAST:
            self.speed = SEMIFAST_SPEED
        elif time_speed == TimerSpeedStates.FAST:
            self.speed = FAST_SPEED


    def stop_player(self):
        self.change_x = 0
        self.change_y = 0

    def move_to_path(self, next_point):
        start_x = self.center_x
        start_y = self.center_y

        if not next_point:
            return

        # Where are we going
        dest_x = next_point[0]
        dest_y = next_point[1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        # # Update our location
        # self.center_x += change_x
        # self.center_y += change_y
