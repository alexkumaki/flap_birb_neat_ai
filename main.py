from settings import *
from player import Player
from objects import *
from random import randint
import neat
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flap Birb')
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.top_pipe_sprites = pygame.sprite.Group()
        self.bottom_pipe_sprites = pygame.sprite.Group()
        self.all_pipe_sprites = pygame.sprite.Group()
        self.score_sprites = pygame.sprite.Group()
        self.ground_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)
        self.ground = Ground(True, (self.all_sprites, self.ground_sprites))
        self.roof = Ground(False, (self.all_sprites, self.ground_sprites))
        self.start_time = pygame.time.get_ticks()
        self.pipe_timer = pygame.time.get_ticks()
        self.pipe_delay = 1200

        self.score = 0
        pygame.font.init()
        self.font = pygame.font.Font(None, 30)

        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.start_time = pygame.time.get_ticks()

        self.all_sprites.empty()
        self.top_pipe_sprites.empty()
        self.bottom_pipe_sprites.empty()
        self.score_sprites.empty()

        self.player = Player(self.all_sprites)
        self.ground = Ground(True, (self.all_sprites, self.ground_sprites))
        self.roof = Ground(False, (self.all_sprites, self.ground_sprites))

    def create_pipe(self, height):
        TopPipe(height, (self.all_sprites, self.top_pipe_sprites, self.all_pipe_sprites))
        BottomPipe(height, (self.all_sprites, self.bottom_pipe_sprites, self.all_pipe_sprites))
        PipeGap(height, (self.all_sprites, self.score_sprites))

    def collision(self):
        collision_sprites = pygame.sprite.spritecollide(self.player, self.all_pipe_sprites, False, pygame.sprite.collide_mask)
        if collision_sprites:
            pygame.time.delay(500)
            self.reset_game()
        score_collision = pygame.sprite.spritecollide(self.player, self.score_sprites, True, pygame.sprite.collide_mask)
        if score_collision:
            self.score += 1
        if self.player.rect.centery >= WINDOW_HEIGHT:
            pygame.time.delay(500)
            self.reset_game()

    def display_score(self):
        text_surf = self.font.render(f"Score: {self.score}", True, ('red'))
        text_rect = text_surf.get_frect(topleft = (10, 10))
        self.display_surface.blit(text_surf, text_rect)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            if (pygame.time.get_ticks() - self.start_time) % 1000 == 0:
                self.create_pipe(randint(250, 600))
            self.all_sprites.update(dt)
            self.collision()

            self.display_surface.fill('blue')
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            pygame.display.update()

    def run_single_game(self, genomes, config):
        players = []
        nets = []
        ge = []

        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            players.append(Player(self.all_sprites))
            ge.append(genome)

        self.create_pipe(randint(300,600))
        self.pipe_timer = pygame.time.get_ticks()

        while True:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
            
            if ((pygame.time.get_ticks() - self.pipe_timer) >= self.pipe_delay):
                self.score += 1
                self.create_pipe(randint(300, 600))
                self.pipe_timer = pygame.time.get_ticks()

            self.all_sprites.update(dt)
            # alive_players = len(players)

            for i, player in enumerate(players):
                pipe = self.get_next_pipe(player)
                if pipe is not None:
                    inputs = (
                        player.rect.centery,
                        pipe.rect.x + 50 - player.rect.x,
                        pipe.rect.bottom - player.rect.centery
                    )

                    output = nets[i].activate(inputs)

                    if output[0] > 0.5 and player.can_jump:
                        player.flap()

                    ge[i].fitness += 0.1

                    if pygame.sprite.spritecollide(player, self.all_pipe_sprites, False, pygame.sprite.collide_mask):
                        player.image.set_alpha(0)
                        players.pop(i)
                        nets.pop(i)
                        ge.pop(i)
                    elif pygame.sprite.spritecollide(player, self.ground_sprites, False, pygame.sprite.collide_mask):
                        player.image.set_alpha(0)
                        # print(f'Player {i} was killed')
                        players.pop(i)
                        nets.pop(i)
                        ge.pop(i)
                    # if player.rect.centery < 0:
                    #     players.pop(i)
                    #     nets.pop(i)
                    #     ge.pop(i)
                else:
                    inputs = (
                        player.rect.centery,
                        0,
                        0
                    )

                    output = nets[i].activate(inputs)

                    if output[0] > 0.5:
                        player.flap()

                    ge[i].fitness += 0.1

                    if pygame.sprite.spritecollide(player, self.ground_sprites, False, pygame.sprite.collide_mask):
                        player.image.set_alpha(0)
                        players.pop(i)
                        nets.pop(i)
                        ge.pop(i)

            
            if len(players) == 0:
                break
            
            self.display_surface.fill('blue')
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            pygame.display.update()

    def get_next_pipe(self, player):
        for pipe in self.top_pipe_sprites:
            if pipe.rect.right > player.rect.left:
                return pipe
        return None

def eval_genomes(genomes, config):
    game = Game()
    game.run_single_game(genomes, config)

if __name__ == '__main__':

    config_path = join('config-feedforward.txt')
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    population.run(eval_genomes, 50)

