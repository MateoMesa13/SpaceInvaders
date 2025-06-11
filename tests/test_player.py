import os
import pygame
import pytest

import PlayerClass
import EnemyClass
import BulletClass


def _rect_collision(self, obj):
    bullet_rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
    enemy_rect = pygame.Rect(obj.x, obj.y, obj.ship_img.get_width(), obj.ship_img.get_height())
    return bullet_rect.colliderect(enemy_rect)


@pytest.fixture(autouse=True)
def pygame_env():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def setup_game(monkeypatch):
    player_surface = pygame.Surface((40, 40))
    bullet_surface = pygame.Surface((10, 10))
    enemy_surface = pygame.Surface((40, 40))

    monkeypatch.setattr(PlayerClass, "PLAYER_IMAGE", player_surface, raising=False)
    monkeypatch.setattr(PlayerClass, "BULLET_IMAGE", bullet_surface, raising=False)
    monkeypatch.setattr(EnemyClass, "ENEMY_BLUE_IMAGE", enemy_surface, raising=False)
    EnemyClass.COLOR["BLUE"] = (enemy_surface, bullet_surface)
    monkeypatch.setattr(BulletClass.Bullet, "collision", _rect_collision, raising=False)
    return player_surface, bullet_surface, enemy_surface


def test_hit_detects_collision(setup_game):
    player = PlayerClass.Player(50, 50, 0, 0)
    enemy = EnemyClass.Enemy(0, x=50, y=50, color="BLUE")
    bullet = BulletClass.Bullet(50, 50, player.bullet_img)
    player.fired_bullets.append(bullet)
    assert player.hit(enemy)


def test_hit_no_collision(setup_game):
    player = PlayerClass.Player(50, 50, 0, 0)
    enemy = EnemyClass.Enemy(0, x=200, y=200, color="BLUE")
    bullet = BulletClass.Bullet(50, 50, player.bullet_img)
    player.fired_bullets.append(bullet)
    assert not player.hit(enemy)
