import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)  # Change the background colour to light blue
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)  # Add GREY colour definition
LIGHT_GREY = (108, 108, 108)
# Fonts
FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)

# Card dimensions
CARD_WIDTH, CARD_HEIGHT = 100, 150

# Card classes
class Ship:
    def __init__(self, name, color, rank):
        self.name = name
        self.color = color
        self.rank = rank
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)

    @property
    def sign(self):
        if self.rank == 0:
            return "A"
        if 1 <= self.rank <= 10:
            return str(self.rank)
        if self.rank == 11:
            return "J"
        if self.rank == 12:
            return "Q"
        if self.rank == 13:
            return "K"

def create_deck():
    deck = []
    colors = [RED, BLUE, GREEN, YELLOW]
    ship_names = ["Carrier Naval Bomber", "Carrier Fighter", "Submarine", "Destroyer", "Light Cruiser", "Heavy Cruiser", "BattleCruiser", "Carrier", "Battleship", "Super Heavy Battleship", "Ace"]
    ranks = [1, 3, 4, 5, 8, 10, 11, 12, 13, 0, 14]

    for color in colors:
        for name, rank in zip(ship_names, ranks):
            deck.append(Ship(name, color, rank))

    random.shuffle(deck)
    return deck[:6]

# Create decks
player_deck = create_deck()
opponent_deck = create_deck()
player_health = sum(card.rank for card in player_deck)
max_player_health = player_health

# Initialize player and AI health
player_health = sum(card.rank for card in player_deck)
max_player_health = player_health
ai_health = sum(card.rank for card in opponent_deck)
max_ai_health = ai_health

opponent_health = sum(card.rank for card in opponent_deck)
max_opponent_health = opponent_health

# Initialize selected_card and hovered_card
selected_card = None
hovered_card = None

# Initialize attack zones
attack_zone = []
opponent_attack_zone = []

# Initialize turn count
turn_count = 1

# Button class
class Button:
    def __init__(self, x, y, width, height, text, font, colors, text_colors=(WHITE, WHITE)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.colors = colors
        self.text_colors = text_colors

    def draw(self, surface):
        color = self.colors[0] if self.is_hovered(pygame.mouse.get_pos()) else self.colors[1]
        text_color = self.text_colors[0] if self.is_hovered(pygame.mouse.get_pos()) else self.text_colors[1]
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
def draw_zone_outline(surface, x, y, width, height, color):
    outline_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, outline_rect, 3)
    
def draw_health_bar(surface, x, y, width, height, value, max_value, bar_color, bg_color):
    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, bg_color, bg_rect)

    bar_width = int(value / max_value * width)
    bar_rect = pygame.Rect(x, y, bar_width, height)
    pygame.draw.rect(surface, bar_color, bar_rect)


# Move buttons to the sidebar
attack_button = Button(WIDTH - 270, HEIGHT // 2 - 60, 120, 40, "Attack", FONT_SMALL, (GREEN, GREY))
end_turn_button = Button(WIDTH - 270, HEIGHT // 2 - 10, 120, 40, "End Turn", FONT_SMALL, (ORANGE, GREY))
# Main game loop
running = True
while running:
    screen.fill(LIGHT_BLUE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for i, card in enumerate(player_deck):
                    card.rect.topleft = (i * (CARD_WIDTH + 20) + 20, HEIGHT - CARD_HEIGHT - 20)
                    if card.rect.collidepoint(event.pos):
                        selected_card = card
                        attack_zone.append(selected_card)
                        player_deck.remove(selected_card)
            elif event.button == 3:  # Right mouse button
                for card in attack_zone:
                    if card.rect.collidepoint(event.pos):
                        player_deck.append(card)
                        attack_zone.remove(card)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                selected_card = None
                if attack_button.rect.collidepoint(event.pos):
                    if len(attack_zone) == 1 and len(opponent_attack_zone) == 1:
                        player_card = attack_zone[0]
                        ai_card = opponent_attack_zone[0]
                        if player_card.rank > ai_card.rank:
                            ai_health -= (player_card.rank - ai_card.rank)
                            opponent_attack_zone.remove(ai_card)
                            opponent_deck.append(ai_card)
                            print("Player attacked and dealt", player_card.rank - ai_card.rank, "damage.")
                        elif player_card.rank < ai_card.rank:
                            player_health -= (ai_card.rank - player_card.rank)
                            attack_zone.remove(player_card)
                            player_deck.append(player_card)
                            print("AI attacked and dealt", ai_card.rank - player_card.rank, "damage.")
                        else:
                            print("The attack was a draw.")
                elif end_turn_button.rect.collidepoint(event.pos):
                    # AI Logic: deploy a random card and attack
                    if opponent_deck:
                        chosen_card = random.choice(opponent_deck)
                        opponent_attack_zone.append(chosen_card)
                        opponent_deck.remove(chosen_card)
                        print("AI deployed", chosen_card.name)

                    # End turn
                    turn_count += 1




    # Draw buttons
    attack_button.draw(screen)
    end_turn_button.draw(screen)



    # Draw cards
    for i, card in enumerate(player_deck):
        card.rect.topleft = (i * (CARD_WIDTH + 20) + 20, HEIGHT - CARD_HEIGHT - 20)
        pygame.draw.rect(screen, card.color, card.rect)
        sign_surface = FONT_SMALL.render(card.sign, True, BLACK)
        screen.blit(sign_surface, card.rect.topleft)
        name_surface = FONT_SMALL.render(card.name, True, BLACK)
        screen.blit(name_surface, (card.rect.x, card.rect.y + 60))

    for i, card in enumerate(opponent_deck):
        card.rect.topleft = (i * (CARD_WIDTH + 20) + 20, 20)
        pygame.draw.rect(screen, card.color, card.rect)
        sign_surface = FONT_SMALL.render(card.sign, True, BLACK)
        screen.blit(sign_surface, card.rect.topleft)
        name_surface = FONT_SMALL.render(card.name, True, BLACK)
        screen.blit(name_surface, (card.rect.x, card.rect.y + 60))

    # Draw stat panel
    pygame.draw.rect(screen, LIGHT_GREY, (WIDTH - 350, 20, 330, HEIGHT - 40))
    draw_zone_outline(screen, WIDTH - 350, 20, 330, HEIGHT - 40, BLACK)
    draw_zone_outline(screen, 20, HEIGHT // 2 - CARD_HEIGHT // 2 - 100, 6 * (CARD_WIDTH + 20), CARD_HEIGHT, BLACK)
    draw_zone_outline(screen, 20, HEIGHT // 2 - CARD_HEIGHT // 2 + 100, 6 * (CARD_WIDTH + 20), CARD_HEIGHT, BLACK)



    # Draw attack zones
    draw_zone_outline(screen, 20, HEIGHT // 2 - CARD_HEIGHT // 2 - 100, CARD_WIDTH + 20, CARD_HEIGHT, BLACK)
    draw_zone_outline(screen, 20, HEIGHT // 2 - CARD_HEIGHT // 2 + 100, CARD_WIDTH + 20, CARD_HEIGHT, BLACK)

    # Draw stat panel
    draw_zone_outline(screen, WIDTH - 350, 20, 330, HEIGHT - 40, BLACK)

    # Draw buttons
    attack_button.draw(screen)
    end_turn_button.draw(screen)

    # Draw health bars
    draw_health_bar(screen, WIDTH - 270, 100, 200, 20, player_health, max_player_health, GREEN, GREY)
    draw_health_bar(screen, WIDTH - 270, 150, 200, 20, ai_health, max_ai_health, RED, GREY)

    # Draw text labels for player and AI fleet health
    health_label_player = FONT_SMALL.render("Player Fleet Health", True, WHITE)
    health_label_ai = FONT_SMALL.render("AI Fleet Health", True, WHITE)
    screen.blit(health_label_player, (WIDTH - 270, 70))
    screen.blit(health_label_ai, (WIDTH - 270, 120))


    # Draw turn counter and player's turn
    turn_text = FONT.render(f"Turn {turn_count}", True, BLACK)
    screen.blit(turn_text, (WIDTH - 270, 200))
    player_turn_text = FONT.render("Player's Turn" if turn_count % 2 == 1 else "AI's Turn", True, BLACK)
    screen.blit(player_turn_text, (WIDTH - 270, 240))

    # Draw AI actions/thoughts
    ai_thoughts = FONT.render("AI is thinking...", True, BLACK)
    screen.blit(ai_thoughts, (WIDTH - 270, 300))

    # Update screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()


