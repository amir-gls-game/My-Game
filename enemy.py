import pygame
import random
import math


class Enemy:

    def __init__(self, x, y):

        self.width = 60
        self.height = 60

        self.x = x
        self.y = y

        self.color = (200, 40, 40)
        self.direction_color = (235, 75, 75)

        self.direction = "down"

        # Health
        self.max_health = 105
        self.health = 105

        self.hit_timer = 0
        self.recent_hit_timer = 0

        # Movement
        self.speed = 3.0
        self.preferred_distance = 105

        # Attack
        self.attack_distance = 88
        self.attack_damage = 15
        self.attack_cooldown = 45
        self.attack_timer = 0

        # Attack animation
        self.attack_animation_active = False
        self.attack_animation_timer = 0
        self.attack_animation_duration = 14
        self.attack_has_hit = False

        # AI
        self.current_action = "approach"

        self.decision_timer = random.randint(10, 22)
        self.action_timer = random.randint(15, 30)

        self.strafe_direction = random.choice([-1, 1])

        self.personality = random.uniform(0.9, 1.1)

        # Short memory
        self.last_player_attack_direction = None
        self.player_attack_count = 0
        self.attack_memory_timer = 0
        self.counter_window = 0

        # Dodge
        self.dodge_timer = 0

    # =================================================
    # RECT
    # =================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    # =================================================
    # DISTANCE
    # =================================================

    def get_distance_to_player(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = b.centerx - a.centerx
        dy = b.centery - a.centery

        return math.sqrt(dx * dx + dy * dy)

    # =================================================
    # DIRECTION
    # =================================================

    def update_direction_towards_player(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = b.centerx - a.centerx
        dy = b.centery - a.centery

        if abs(dx) > abs(dy):

            if dx > 0:
                self.direction = "right"
            else:
                self.direction = "left"

        else:

            if dy > 0:
                self.direction = "down"
            else:
                self.direction = "up"

    # =================================================
    # PLAYER ATTACK MEMORY
    # =================================================

    def notice_player_attack(self, player):

        self.last_player_attack_direction = player.direction

        self.player_attack_count += 1

        self.attack_memory_timer = 80
        self.counter_window = 15

        self.decision_timer = 0

    # =================================================
    # UTILITY AI
    # =================================================

    def calculate_utilities(self, player):

        distance = self.get_distance_to_player(player)

        health_ratio = self.health / self.max_health
        player_health_ratio = player.health / player.max_health

        utilities = {}

        # =================================================
        # APPROACH
        # =================================================

        approach = 0

        if distance > 140:

            approach += min(
                distance * 0.55,
                80
            )

        elif distance > 115:

            approach += 35

        else:

            approach -= 25

        if player_health_ratio < 0.4:

            approach += 18

        utilities["approach"] = (
            approach * self.personality
        )

        # =================================================
        # ATTACK
        # =================================================

        attack = 0

        if distance <= self.attack_distance:

            attack += 70

            if self.attack_timer <= 0:

                attack += 50

            else:

                attack -= 40

            if self.counter_window > 0:

                attack += 35

            if player_health_ratio < 0.35:

                attack += 30

        else:

            attack -= (
                distance - self.attack_distance
            ) * 0.7

        utilities["attack"] = (
            attack * self.personality
        )

        # =================================================
        # STRAFE
        # =================================================

        strafe = 0

        if 65 <= distance <= 145:

            strafe += 50

        elif distance < 65:

            strafe += 25

        else:

            strafe -= 20

        if self.player_attack_count >= 2:

            strafe += 25

        utilities["strafe"] = strafe

        # =================================================
        # RETREAT
        # =================================================

        retreat = 5

        if distance < 60:

            retreat += 35

        if health_ratio < 0.30:

            retreat += 55

        elif health_ratio < 0.50:

            retreat += 25

        if self.recent_hit_timer > 0:

            retreat += 30

        if player_health_ratio < 0.30:

            retreat -= 50

        utilities["retreat"] = retreat

        # =================================================
        # DODGE
        # =================================================

        dodge = 0

        if self.attack_memory_timer > 0:

            dodge += 15

        if self.player_attack_count >= 2:

            dodge += 35

        if distance < 120:

            dodge += 20

        if self.dodge_timer > 0:

            dodge -= 80

        utilities["dodge"] = dodge

        # =================================================
        # REPOSITION
        # =================================================

        reposition = 15

        if (
            self.preferred_distance - 25
            <= distance
            <= self.preferred_distance + 40
        ):

            reposition += 25

        utilities["reposition"] = reposition

        # =================================================
        # CONTROLLED RANDOMNESS
        # =================================================

        for action in utilities:

            utilities[action] += random.uniform(
                -7,
                7
            )

        return utilities

    # =================================================
    # CHOOSE ACTION
    # =================================================

    def choose_action(self, player):

        utilities = self.calculate_utilities(
            player
        )

        sorted_actions = sorted(
            utilities.items(),
            key=lambda item: item[1],
            reverse=True
        )

        best_action = sorted_actions[0][0]
        best_score = sorted_actions[0][1]

        if len(sorted_actions) > 1:

            second_action = sorted_actions[1][0]
            second_score = sorted_actions[1][1]

            if (
                second_score >= best_score * 0.80
                and random.random() < 0.25
            ):

                best_action = second_action

        self.current_action = best_action

        self.action_timer = random.randint(
            12,
            28
        )

        if random.random() < 0.35:

            self.strafe_direction *= -1

    # =================================================
    # APPROACH
    # =================================================

    def approach_player(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = b.centerx - a.centerx
        dy = b.centery - a.centery

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:
            return

        self.update_direction_towards_player(
            player
        )

        if distance > self.preferred_distance:

            self.x += (
                dx / distance
            ) * self.speed

            self.y += (
                dy / distance
            ) * self.speed

        elif distance > 82:

            self.x += (
                dx / distance
            ) * self.speed * 0.35

            self.y += (
                dy / distance
            ) * self.speed * 0.35

    # =================================================
    # RETREAT
    # =================================================

    def retreat_from_player(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = a.centerx - b.centerx
        dy = a.centery - b.centery

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:

            dx = random.choice(
                [-1, 1]
            )

            dy = 0

            distance = 1

        self.update_direction_towards_player(
            player
        )

        speed = self.speed * 0.85

        self.x += (
            dx / distance
        ) * speed

        self.y += (
            dy / distance
        ) * speed

    # =================================================
    # STRAFE
    # =================================================

    def strafe_player(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = b.centerx - a.centerx
        dy = b.centery - a.centery

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:
            return

        self.update_direction_towards_player(
            player
        )

        side_x = -dy / distance
        side_y = dx / distance

        speed = self.speed * 0.85

        self.x += (
            side_x
            * speed
            * self.strafe_direction
        )

        self.y += (
            side_y
            * speed
            * self.strafe_direction
        )

    # =================================================
    # REPOSITION
    # =================================================

    def reposition(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = b.centerx - a.centerx
        dy = b.centery - a.centery

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:
            return

        self.update_direction_towards_player(
            player
        )

        side_x = -dy / distance
        side_y = dx / distance

        speed = self.speed * 0.35

        self.x += (
            side_x
            * speed
            * self.strafe_direction
        )

        self.y += (
            side_y
            * speed
            * self.strafe_direction
        )

    # =================================================
    # DODGE
    # =================================================

    def dodge_player(self, player):

        a = self.get_rect()
        b = player.get_rect()

        dx = b.centerx - a.centerx
        dy = b.centery - a.centery

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:
            return

        side_x = -dy / distance
        side_y = dx / distance

        self.update_direction_towards_player(
            player
        )

        speed = self.speed * 1.5

        self.x += (
            side_x
            * speed
            * self.strafe_direction
        )

        self.y += (
            side_y
            * speed
            * self.strafe_direction
        )

        self.dodge_timer = 35

    # =================================================
    # ENEMY PUNCH RECT
    # =================================================

    def get_enemy_punch_rect(self):

        rect = self.get_rect()

        size = 28
        extension = 0

        if self.attack_animation_active:

            progress = (
                self.attack_animation_duration
                - self.attack_animation_timer
            ) / self.attack_animation_duration

            if progress < 0.5:

                amount = (
                    progress / 0.5
                )

            else:

                amount = (
                    1
                    - (
                        (progress - 0.5)
                        / 0.5
                    )
                )

            extension = int(
                amount * 32
            )

        if self.direction == "up":

            return pygame.Rect(
                rect.centerx - size // 2,
                rect.top
                - size
                - extension,
                size,
                size
            )

        elif self.direction == "down":

            return pygame.Rect(
                rect.centerx - size // 2,
                rect.bottom + extension,
                size,
                size
            )

        elif self.direction == "left":

            return pygame.Rect(
                rect.left
                - size
                - extension,
                rect.centery - size // 2,
                size,
                size
            )

        else:

            return pygame.Rect(
                rect.right + extension,
                rect.centery - size // 2,
                size,
                size
            )

    # =================================================
    # CHECK ATTACK HIT
    # =================================================

    def check_attack_hit(self, player):

        if not self.attack_animation_active:
            return

        if self.attack_has_hit:
            return

        progress = (
            self.attack_animation_duration
            - self.attack_animation_timer
        ) / self.attack_animation_duration

        if progress < 0.25:
            return

        if progress > 0.65:
            return

        punch_rect = self.get_enemy_punch_rect()

        if punch_rect.colliderect(
            player.get_rect()
        ):

            player.take_damage(
                self.attack_damage
            )

            self.attack_has_hit = True

    # =================================================
    # ATTACK
    # =================================================

    def can_attack(self, player):

        return (
            self.get_distance_to_player(player)
            <= self.attack_distance
            and self.attack_timer <= 0
            and not self.attack_animation_active
        )

    def attack(self, player):

        if not self.can_attack(player):
            return False

        self.update_direction_towards_player(
            player
        )

        self.attack_animation_active = True

        self.attack_animation_timer = (
            self.attack_animation_duration
        )

        self.attack_has_hit = False

        self.attack_timer = (
            self.attack_cooldown
        )

        self.action_timer = random.randint(
            8,
            18
        )

        return True

    # =================================================
    # CLOSE ATTACK OVERRIDE
    # =================================================

    def close_range_attack_check(self, player):

        """
        اگر بازیکن وارد محدوده مشت شده باشد،
        دشمن قبل از هر تصمیم حرکتی تلاش می‌کند مشت بزند.

        این بخش هوش اصلی را حذف نمی‌کند.
        فقط یک قانون نزدیک‌برد اضافه می‌کند:
        «اگر می‌توانی الان مشت بزنی، فرصت را از دست نده.»
        """

        distance = self.get_distance_to_player(
            player
        )

        if distance > self.attack_distance:
            return False

        if self.attack_animation_active:
            return True

        if self.attack_timer > 0:
            return False

        return self.attack(player)

    # =================================================
    # ATTACK ANIMATION UPDATE
    # =================================================

    def update_attack_animation(self, player):

        if not self.attack_animation_active:
            return

        self.check_attack_hit(player)

        self.attack_animation_timer -= 1

        if self.attack_animation_timer <= 0:

            self.attack_animation_timer = 0

            self.attack_animation_active = False

    # =================================================
    # DAMAGE
    # =================================================

    def take_damage(self, damage):

        self.health -= damage

        if self.health < 0:
            self.health = 0

        self.hit_timer = 8
        self.recent_hit_timer = 40

        self.decision_timer = 0

        if random.random() < 0.55:

            self.counter_window = 20

    # =================================================
    # AI UPDATE
    # =================================================

    def update_ai(self, player):

        self.decision_timer -= 1
        self.action_timer -= 1

        # ------------------------------------------------
        # اگر در حال مشت زدن است
        # ------------------------------------------------

        if self.attack_animation_active:

            self.update_direction_towards_player(
                player
            )

            return

        # ------------------------------------------------
        # قانون جدید:
        # اگر بازیکن خیلی نزدیک است و دشمن می‌تواند
        # مشت بزند، قبل از حرکت یک مشت بزند.
        # ------------------------------------------------

        if self.close_range_attack_check(player):

            return

        # ------------------------------------------------
        # تصمیم‌گیری اصلی AI
        # ------------------------------------------------

        if self.decision_timer <= 0:

            self.choose_action(player)

            self.decision_timer = random.randint(
                9,
                20
            )

        # ------------------------------------------------
        # اجرای تصمیم
        # ------------------------------------------------

        if self.current_action == "approach":

            self.approach_player(player)

        elif self.current_action == "attack":

            self.update_direction_towards_player(
                player
            )

            self.attack(player)

        elif self.current_action == "strafe":

            self.strafe_player(player)

        elif self.current_action == "retreat":

            self.retreat_from_player(player)

        elif self.current_action == "dodge":

            self.dodge_player(player)

        elif self.current_action == "reposition":

            self.reposition(player)

    # =================================================
    # UPDATE
    # =================================================

    def update(self, player):

        if self.hit_timer > 0:
            self.hit_timer -= 1

        if self.recent_hit_timer > 0:
            self.recent_hit_timer -= 1

        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.attack_memory_timer > 0:
            self.attack_memory_timer -= 1

        if self.counter_window > 0:
            self.counter_window -= 1

        if self.dodge_timer > 0:
            self.dodge_timer -= 1

        self.update_attack_animation(player)

        self.update_ai(player)

    # =================================================
    # HEALTH BAR
    # =================================================

    def draw_health_bar(self, screen, rect):

        bar_width = 70
        bar_height = 8

        bar_x = (
            rect.centerx
            - bar_width // 2
        )

        bar_y = rect.top - 20

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            )
        )

        ratio = (
            self.health
            / self.max_health
        )

        current_width = int(
            bar_width * ratio
        )

        if current_width > 0:

            pygame.draw.rect(
                screen,
                (200, 40, 40),
                (
                    bar_x,
                    bar_y,
                    current_width,
                    bar_height
                )
            )

        pygame.draw.rect(
            screen,
            (15, 15, 15),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            2
        )

    # =================================================
    # DRAW
    # =================================================

    def draw(self, screen):

        if self.hit_timer > 0:

            color = (
                255,
                100,
                100
            )

            direction_color = (
                255,
                150,
                150
            )

        else:

            color = self.color
            direction_color = self.direction_color

        rect = self.get_rect()

        pygame.draw.rect(
            screen,
            color,
            rect
        )

        self.draw_health_bar(
            screen,
            rect
        )

        dot_radius = 7

        if self.direction == "up":

            dot_pos = (
                rect.centerx,
                rect.top + 12
            )

        elif self.direction == "down":

            dot_pos = (
                rect.centerx,
                rect.bottom - 12
            )

        elif self.direction == "left":

            dot_pos = (
                rect.left + 12,
                rect.centery
            )

        else:

            dot_pos = (
                rect.right - 12,
                rect.centery
            )

        pygame.draw.circle(
            screen,
            direction_color,
            dot_pos,
            dot_radius
        )

        # Enemy punch animation

        if self.attack_animation_active:

            punch_rect = (
                self.get_enemy_punch_rect()
            )

            pygame.draw.rect(
                screen,
                (255, 100, 100),
                punch_rect,
                border_radius=7
            )