import pygame
import sys

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("My First Game")

white = (255, 255, 255)
black = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 50)
big_font = pygame.font.SysFont("Arial", 70)

winningScore = 5


class Player:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.score = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

    def move(self, up_key, down_key, keys, screen_height):
        if keys[up_key] and self.y > 0:
            self.y -= self.speed
        if keys[down_key] and self.y < screen_height - self.height:
            self.y += self.speed


class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def reset(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed_x = 5 * direction
        self.speed_y = 5

def check_wall_collision(ball, screen_height):
    if ball.y - ball.radius <= 0 or ball.y + ball.radius > screen_height:
        ball.speed_y *= -1

def check_paddle_collision(ball, player):
    if (player.x < ball.x < player.x + player.width and player.y < ball.y < player.y + player.height):
        ball.speed_x *= -1
        ball.speed_x *= 1.1
        ball.speed_y *= 1.05


player1 = Player(30, height // 2 - 50, 20, 100, white, speed=7)
player2 = Player(width - 50, height // 2 - 50, 20, 100, white, speed=7)
ball = Ball(width // 2, height // 2, 10, white, speed_x=5, speed_y=5)


def draw_window(winner=None):
    screen.fill(black)

    pygame.draw.aaline(screen, white, (width // 2, 0), (width // 2, height))

    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    score_text = font.render(f"{player1.score} {player2.score}", True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

    if winner:
        win_text = big_font.render(winner, True, white)
        screen.blit(
            win_text,
            (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2)
        )
    pygame.display.flip()


def main():
    running = True
    winner = None

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if winner is None:
            keys = pygame.key.get_pressed()
            player1.move(pygame.K_w, pygame.K_s, keys, height)
            player2.move(pygame.K_UP, pygame.K_DOWN, keys, height)

            ball.move()
            check_wall_collision(ball, height)
            check_paddle_collision(ball, player1)
            check_paddle_collision(ball, player2)

            if ball.x - ball.radius <= 0:
                player2.score += 1
                ball.reset(width // 2, height // 2, direction=1)

            if ball.x + ball.radius >= width:
                player1.score += 1
                ball.reset(width // 2, height // 2, direction=-1)

            if player1.score >= winningScore:
                winner = "Player 1 wins"
            elif player2.score >= winningScore:
                winner = "Player 2 wins"

        draw_window(winner)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

