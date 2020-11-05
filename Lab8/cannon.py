import pygame as pg
import pygame.draw as draw
from Lab8.common import GameObject, Vector, Colors


class Cannon(GameObject):
    """
    Represents a stationary cannon that can shoot projectiles
    """
    max_shooting_power = 1.0
    shooting_power_per_second = 0.35
    projectile_max_velocity = 500
    projectile_min_velocity = 50
    line_width = 20
    line_length = 150
    y_pos = 100

    def __init__(self, game):
        height = game.resolution[1]
        super().__init__(Vector(Cannon.y_pos, height / 2), game)

        game.subscribe_to_event(pg.MOUSEBUTTONDOWN, self._mousebuttondown_listener)
        game.subscribe_to_event(pg.MOUSEBUTTONUP, self._mousebuttonup_listener)

        self.shooting_power = 0
        self.direction = Vector(1, 0)
        self.is_mouse_down = False
        self._shells = []

    def update(self):
        x, y = pg.mouse.get_pos()
        self.direction = (Vector(x, y) - self.pos).normalize()

        if self.is_mouse_down:
            print("Adding shooting power")
            self.shooting_power = min(self.shooting_power + Cannon.shooting_power_per_second * self.game.dt,
                                      Cannon.max_shooting_power)

    def draw(self, surface):
        start_pos = tuple(self.pos)
        end_pos = tuple(self.pos + self.direction * Cannon.line_length)

        draw.line(surface, Colors.red, start_pos, end_pos, Cannon.line_width)

        if self.is_mouse_down:
            end_pos = tuple(self.pos + self.direction * Cannon.line_length * max(self.shooting_power, 0.03))
            # line is drawn incorrectly when it's length is 0 so an indent of 0.03 added

            draw.line(surface, Colors.white, start_pos, end_pos, Cannon.line_width)

    def on_destroyed(self):
        pass

    def _mousebuttondown_listener(self, event: pg.event.Event):
        """
        MOUSEBUTTONDOWN event listener
        :param event: an event object
        """
        self.is_mouse_down = True
        self.shooting_power = 0

    def _mousebuttonup_listener(self, event: pg.event.Event):
        """
        MOUSEBUTTONUP event listener
        :param event: an event object
        """
        self.is_mouse_down = False
        self.shoot()
        self.shooting_power = 0

    def shoot(self):
        """
        Shoots a projectile
        """
        projectile_pos = self.pos + self.direction * Cannon.line_length
        projectile_velocity = self.direction * (Cannon.projectile_min_velocity + (Cannon.projectile_max_velocity - Cannon.projectile_min_velocity) * self.shooting_power)
        self._shells.append(Projectile(projectile_pos, projectile_velocity, self.game, self))


class Projectile(GameObject):
    gravitational_acceleration = Vector(0, 20)
    air_resistance_coefficient = 0.02
    max_radius = 40

    def __init__(self, pos, velocity, game, cannon):
        super().__init__(pos, game)

        self.cannon = cannon

        self.velocity = velocity

    def update(self):
        dt = self.game.dt

        self.pos += self.velocity * dt
        self.velocity += (Projectile.gravitational_acceleration
                          - self.velocity * Projectile.air_resistance_coefficient) * dt

    def draw(self, surface):
        draw.circle(surface, Colors.white, self.pos.int_tuple(), Projectile.max_radius)

    def on_destroyed(self):
        pass