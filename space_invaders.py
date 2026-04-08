import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simple Space Invaders (Arcade 3.x Compatible)"

PLAYER_SPEED = 5
BULLET_SPEED = 7


class SpaceGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set a background color (this satisfies "background" requirement)
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.player = None

    def setup(self):
        # Player (movable)
        self.player = arcade.SpriteSolidColor(40, 20, arcade.color.WHITE)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 50
        self.player_list.append(self.player)

        # Unmovable object (wall)
        wall = arcade.SpriteSolidColor(200, 20, arcade.color.GRAY)
        wall.center_x = SCREEN_WIDTH // 2
        wall.center_y = 200
        self.wall_list.append(wall)

        # Enemy (moves left/right)
        enemy = arcade.SpriteSolidColor(40, 20, arcade.color.RED)
        enemy.center_x = SCREEN_WIDTH // 2
        enemy.center_y = 500
        enemy.change_x = 2
        self.enemy_list.append(enemy)

    def on_draw(self):
        # Clears the screen using the background color
        self.clear()

        # Draw sprites
        self.player_list.draw()
        self.bullet_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.bullet_list.update()
        self.enemy_list.update()

        # Enemy bouncing movement
        for enemy in self.enemy_list:
            if enemy.left < 0 or enemy.right > SCREEN_WIDTH:
                enemy.change_x *= -1

        # Bullet-wall collision
        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.wall_list):
                bullet.remove_from_sprite_lists()

        # Bullet-enemy collision
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

        # Remove bullets off-screen
        for bullet in self.bullet_list:
            if bullet.top > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        # Keyboard input
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.SPACE:
            # Fire bullet
            bullet = arcade.SpriteSolidColor(4, 12, arcade.color.YELLOW)
            bullet.center_x = self.player.center_x
            bullet.bottom = self.player.top
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


def main():
    game = SpaceGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
