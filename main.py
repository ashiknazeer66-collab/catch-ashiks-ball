import pygame
import copy
import sys
import random
from hand_tracker import get_finger_position

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Ashiks Balls")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
YELLOW = (255, 255, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)


# -----------------------------
# Tube Positions
# -----------------------------
tube_x = [200, 350, 500, 650]
# -----------------------------
# Random Puzzle Generator
# -----------------------------
def generate_puzzle():

    colors = [RED, GREEN, BLUE]

    # 4 balls of each color = 12 balls total
    all_balls = colors * 4

    random.shuffle(all_balls)

    # 3 tubes get 4 balls each, 1 tube stays empty
    new_tubes = [all_balls[0:4], all_balls[4:8], all_balls[8:12], []]

    return new_tubes


# -----------------------------
# Starting Puzzle
# -----------------------------
tubes = generate_puzzle()
initial_tubes = copy.deepcopy(tubes)

moves = 0
won = False

# -----------------------------
# Tube Colors
# -----------------------------
tube_colors = [WHITE, WHITE, WHITE, WHITE]

# -----------------------------
# Game Variables
# -----------------------------
picked_ball = None
picked_from = None
selected_tube = None

# -----------------------------
# Animation Variables
# -----------------------------
animating = False
anim_ball_color = None
anim_start = (0, 0)
anim_end = (0, 0)
anim_progress = 0.0
anim_speed = 0.08  # higher = faster animation
anim_target_tube = None

last_pinching = False
running = True


# -----------------------------
# Draw One Tube
# -----------------------------
def draw_tube(screen, tube, x, color):

    pygame.draw.rect(screen, color, (x, 150, 70, 220), 4)

    ball_y = 335

    for ball in tube:

        pygame.draw.circle(screen, ball, (x + 35, ball_y), 25)

        ball_y -= 50


# -----------------------------
# Find Which Tube Finger Is On
# -----------------------------
def get_selected_tube(game_x):

    for i in range(4):

        if abs(game_x - tube_x[i]) < 50:
            return i

    return None


# -----------------------------
# Get pixel position where a ball
# would land in a tube
# -----------------------------
def get_ball_landing_pos(tube_index, tube_len):

    x = tube_x[tube_index] + 35
    y = 335 - (tube_len * 50)

    return (x, y)


# -----------------------------
# Check Win Condition
# -----------------------------
def check_win(tubes):
    for tube in tubes:
        if len(tube) == 0:
            continue
        if len(tube) != 4:
            return False
        for ball in tube:
            if ball != tube[0]:
                return False
    return True


# -----------------------------
# Main Game Loop
# -----------------------------
while running:

    # -----------------------------
    # Check Window Events
    # -----------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # -----------------------------
        # Restart Game (R key)
        # -----------------------------
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                tubes = generate_puzzle()
                picked_ball = None
                picked_from = None
                moves = 0
                won = False

                print("🔄 New Puzzle Generated!")

    # -----------------------------
    # Clear Screen
    # -----------------------------
    screen.fill(BLACK)

    # Reset tube colors
    tube_colors = [WHITE, WHITE, WHITE, WHITE]

    # -----------------------------
    # Read Hand Tracker
    # -----------------------------
    position = get_finger_position()

    x = None
    y = None
    pinching = False

    if position is not None:

        x, y, pinching = position

    # -----------------------------
    # Finger Detection
    # -----------------------------
    if x is not None and y is not None:

        # Draw finger cursor
        pygame.draw.circle(screen, WHITE, (x, y), 15)

        # Detect selected tube
        selected_tube = get_selected_tube(x)

        if selected_tube is not None:

            tube_colors[selected_tube] = YELLOW

    else:

        selected_tube = None

    # -----------------------------
    # Draw picked ball
    # -----------------------------
    if picked_ball is not None:

        if x is not None and y is not None:

            pygame.draw.circle(screen, picked_ball, (x, y - 40), 25)

            # -----------------------------
    # Draw animating ball
    # -----------------------------
    if animating:

        pygame.draw.circle(
            screen, anim_ball_color, (int(current_x), int(current_y)), 25
        )

    # -----------------------------
    # Pick Ball
    # -----------------------------
    if pinching and not last_pinching:

        if picked_ball is None:

            if selected_tube is not None:

                if len(tubes[selected_tube]) > 0:

                    # Remember where the ball came from
                    picked_from = selected_tube

                    # Pick the top ball
                    picked_ball = tubes[selected_tube].pop()

                    print("Picked!")

    # -----------------------------
    # Drop Ball
    # -----------------------------
    if (not pinching) and last_pinching:

        if picked_ball is not None and not animating:
            can_drop = False
            if selected_tube is not None:

                # Rule 1: Always allow returning
                # to the original tube
                if selected_tube == picked_from:

                    can_drop = True

                # Rule 2: Tube must have space
                elif len(tubes[selected_tube]) < 4:

                    if len(tubes[selected_tube]) == 0:
                        can_drop = True
                    elif tubes[selected_tube][-1] == picked_ball:
                        can_drop = True
                    else:
                        can_drop = False
                        print("Wrong Color!")

                else:
                    can_drop = False
                    print("Tube Full!")

                # -----------------------------
                # Start the drop animation
                # -----------------------------
                if can_drop:

                    animating = True
                    anim_ball_color = picked_ball
                    anim_target_tube = selected_tube
                    anim_progress = 0.0

                    anim_start = (x, y - 40)
                    anim_end = get_ball_landing_pos(
                        selected_tube, len(tubes[selected_tube])
                    )

                    picked_ball = None
                    picked_from = None
    # Save pinch state
    last_pinching = pinching

    # -----------------------------
    # Update Ball Animation
    # -----------------------------
    if animating:

        anim_progress += anim_speed

        if anim_progress >= 1.0:

            anim_progress = 1.0

            # Animation finished — actually add ball to tube
            tubes[anim_target_tube].append(anim_ball_color)

            moves += 1
            print("Dropped!")

            animating = False

        # Calculate current position (linear interpolation)
        current_x = anim_start[0] + (anim_end[0] - anim_start[0]) * anim_progress
        current_y = anim_start[1] + (anim_end[1] - anim_start[1]) * anim_progress

    # -----------------------------
    # Check Win
    # -----------------------------
    if not won:

        if check_win(tubes):

            won = True
            print("🎉 You Win!")

    # -----------------------------
    # Draw All Tubes
    # -----------------------------
    for i in range(4):

        draw_tube(screen, tubes[i], tube_x[i], tube_colors[i])

    # -----------------------------
    # Show PINCH text
    # -----------------------------
    if pinching:

        font = pygame.font.SysFont(None, 36)

        text = font.render("PINCH!", True, YELLOW)

        screen.blit(text, (20, 20))

    # -----------------------------
    # Show Moves
    # -----------------------------
    font_small = pygame.font.SysFont(None, 30)
    moves_text = font_small.render(f"Moves: {moves}", True, WHITE)
    screen.blit(moves_text, (20, 60))

    # -----------------------------
    # Show Win Message
    # -----------------------------
    if won:

        font_big = pygame.font.SysFont(None, 60)
        win_text = font_big.render("YOU WIN! Press R to restart", True, YELLOW)
        screen.blit(win_text, (60, 250))

    # -----------------------------
    # Update Screen
    # -----------------------------
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)


# -----------------------------
# Close Game
# -----------------------------
pygame.quit()
sys.exit()
