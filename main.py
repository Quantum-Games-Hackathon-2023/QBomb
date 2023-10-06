import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, RLEACCEL
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import os
import numpy as np


pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.RESIZABLE)
pygame.display.set_caption('Gra')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75,25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()

        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)


        if self.rect.left < 0:
              self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
              self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
              self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
              self.rect.bottom = SCREEN_HEIGHT


def update_image(coords):
    plot_bloch_vector([1]+coords, coord_type='spherical', figsize=(2,2))
    plt.savefig('bloch.png')
    plt.close()


class Qubit(pygame.sprite.Sprite):
    def __init__(self):
        super(Qubit, self).__init__()
        self.coords = [0,0]
        self.last_update = 0
        self.surf = None
        self.rect = None
        self.reLoadImage()

    def reLoadImage(self):
        file_time = os.path.getmtime('bloch.png')
        if file_time > self.last_update:
            self.surf = pygame.image.load("bloch.png").convert()
            self.rect = self.surf.get_rect(center=(500,500))


class Gate(pygame.sprite.Sprite):
    def __init__(self, gate_type, center):
        super(Gate, self).__init__()
        self.gate_type = gate_type
        self.surf = pygame.Surface((75,75))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect(center=center)

    

player = Player()
update_image([0,0])
qubit = Qubit()
H = Gate('H', (200,200))
X = Gate('X',(350,200))

all_sprites = pygame.sprite.Group()
gates = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(qubit)
all_sprites.add(H)
all_sprites.add(X)
gates.add(H)
gates.add(X)

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    qubit.reLoadImage()

    screen.fill((0,0,0))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    gate_pass = pygame.sprite.spritecollideany(player, gates)
    if gate_pass:
        if gate_pass.gate_type == 'H':
            qubit.coords[0]+=np.pi/2
            qubit.coords[1]+=0
            coords = qubit.coords
        if gate_pass.gate_type == 'X':
            qubit.coords[0]+=np.pi
            qubit.coords[1]+=np.pi
            coords = qubit.coords
        
        update_image(coords)
        gate_pass.kill()


    pygame.display.flip()

    clock.tick(50)
    

pygame.quit()