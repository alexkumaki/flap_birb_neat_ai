from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill('yellow')
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2))
        self.speed = 0
        self.jump_speed = -500
        self.gravity = 35
        self.max_speed = 500
        
        self.can_jump = True
        self.jump_time = 0
        self.jump_cooldown = 50

    def jump(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.can_jump:
            self.speed = self.jump_speed
            self.jump_time = pygame.time.get_ticks()

    def flap(self):
        if self.can_jump:
            self.speed = self.jump_speed
            self.jump_time = pygame.time.get_ticks()

    def move(self, dt):
        self.rect.centery += self.speed * dt

    def jump_timer(self):
        if not self.can_jump:
            current_time = pygame.time.get_ticks()
            if current_time - self.jump_time >= self.jump_cooldown:
                self.can_jump = True

    def update(self, dt):
        self.jump_timer()
        self.jump()
        self.speed = min(self.speed + self.gravity, self.max_speed)
        self.move(dt)
        if self.rect.centery < 0:
            self.rect.centery = 0
            self.speed = 0