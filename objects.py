from settings import *
from random import randint


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, height, groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 500))
        self.image.fill('darkgreen')
        self.rect = self.image.get_frect(bottomleft = (600, height - 200))

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 5000
        self.speed = 400

    def update(self, dt):
        self.rect.centerx -= self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class BottomPipe(pygame.sprite.Sprite):
    def __init__(self, height, groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 500))
        self.image.fill('darkgreen')
        self.rect = self.image.get_frect(topleft = (600, height))

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 5000
        self.speed = 400

    def update(self, dt):
        self.rect.centerx -= self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class PipeGap(pygame.sprite.Sprite):
    def __init__(self, height, groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 150))
        self.image.set_alpha(0)
        self.rect = self.image.get_frect(bottomleft = (650, height))

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 5000
        self.speed = 400

    def update(self, dt):
        self.rect.centerx -= self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self, ground, groups):
        super().__init__(groups)
        self.image = pygame.Surface((WINDOW_WIDTH, 50))
        if ground:
            self.rect = self.image.get_frect(bottomleft = (0, WINDOW_HEIGHT))
        else:
            self.rect = self.image.get_frect(topleft = (0, 0))