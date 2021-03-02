# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import sys
import random
import pygame


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(300, random_pipe_pos - 150))
    bottom_pipe = pipe_surface.get_rect(midtop=(300, random_pipe_pos))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotate(bird, -bird_movement * 3)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index % 3]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def display_score(game_on):
    if game_on:
        score_surface = game_font.render(str(int(score)), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    
    else: 
        score_surface = game_font.render(f'Score: {str(int(score))}', False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {str(int(high_score))}', False, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 420))
        screen.blit(high_score_surface, high_score_rect)


pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 25)

# Game Variables
GRAVITY = 0.125
bird_movement = 0
game_active = False
score = 0
high_score = 0

# Surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert()
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 236))

# Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

score_sound_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5

            if game_active:
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                pipe_list.clear()
                bird_rect.center = (50, 256)
                game_active = True
                bird_movement = 0
                score = 0
                score_sound_counter = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
            if len(pipe_list) >= 6:
                pipe_list.pop(0)
                pipe_list.pop(0)

        if event.type == BIRDFLAP:
            bird_index += 1

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        game_active = check_collision(pipe_list)

        # Pipes
        draw_pipes(pipe_list)
        pipe_list = move_pipes(pipe_list)

        # Score
        score += 0.0075
        if int(score) - score_sound_counter != 0:
            score_sound.play()
            score_sound_counter += 1
        
    else:
        screen.blit(game_over_surface, game_over_rect)

    # Score
    if score > high_score:
        high_score = score

    display_score(game_active)

    # Floor
    draw_floor()
    floor_x_pos -= 1
    if floor_x_pos <= -288:
        floor_x_pos += 288

    pygame.display.update()
    clock.tick(120)
