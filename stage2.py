import pygame

from player import Player
from enemy import Enemy
from controls import Controls
from collision import keep_inside_room, separate_entities
from death import DeathScreen
from menu import Menu


class Stage2:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        # ==========================================
        # زمین سبز
        # ==========================================

        self.floor_color = (
            75,
            150,
            70
        )

        # ==========================================
        # محیط
        # دقیقاً مثل مرحله ۱
        # ==========================================

        self.room_rect = pygame.Rect(
            20,
            20,
            self.width - 40,
            self.height - 40
        )

        # ==========================================
        # بازیکن
        # نقطه شروع مرحله ۲
        # ==========================================

        self.start_player_x = (
            self.width // 2 - 30
        )

        self.start_player_y = (
            self.height - 600
        )

        self.player = Player(
            self.start_player_x,
            self.start_player_y
        )

        # ==========================================
        # دشمن اول
        # ==========================================

        enemy_y = 500

        self.enemy1 = Enemy(
            self.width // 2 - 60,
            enemy_y
        )

        # ==========================================
        # دشمن دوم
        # 60 پیکسل فاصله از دشمن اول
        # ==========================================

        self.enemy2 = Enemy(
            self.width // 2 + 60,
            enemy_y
        )

        # ==========================================
        # کنترل‌ها
        # ==========================================

        self.controls = Controls(
            self.width,
            self.height
        )

        # ==========================================
        # صفحه مرگ
        # ==========================================

        self.death_screen = DeathScreen(
            self.width,
            self.height,
            self.controls
        )

        # ==========================================
        # منو
        # ==========================================

        self.menu = Menu(
            self.width,
            self.height
        )

        # ==========================================
        # حمله بازیکن
        # ==========================================

        self.player_attack_damage = 20

        self.player_attack_cooldown = 25

        self.player_attack_timer = 0

        # ==========================================
        # مرحله بعد
        # ==========================================

        self.next_stage = None

        # ==========================================
        # علف‌ها
        # ==========================================

        self.grass = []

        self.create_grass()

    # =================================================
    # CREATE GRASS
    # =================================================

    def create_grass(self):

        # علف‌های ثابت و سبک
        # از حاشیه دیوار فاصله دارند

        positions = [

            (90, 100),
            (170, 170),
            (280, 90),
            (400, 150),
            (530, 100),
            (620, 220),

            (100, 330),
            (230, 300),
            (430, 330),
            (570, 380),

            (90, 520),
            (280, 480),
            (470, 530),
            (620, 560),

            (120, 700),
            (300, 650),
            (500, 720),

            (80, 850),
            (220, 900),
            (430, 850),
            (600, 920),

            (120, 1050),
            (350, 1000),
            (550, 1080),

        ]

        self.grass = positions

    # =================================================
    # DRAW GRASS
    # =================================================

    def draw_grass(self):

        for x, y in self.grass:

            # ساقه‌های کوچک علف

            pygame.draw.line(
                self.screen,
                (35, 105, 35),
                (x, y + 8),
                (x - 4, y),
                3
            )

            pygame.draw.line(
                self.screen,
                (35, 105, 35),
                (x, y + 8),
                (x + 4, y - 2),
                3
            )

    # =================================================
    # MENU BUTTON CHECK
    # =================================================

    def is_menu_button_pressed(self, event):

        if not hasattr(
            self.controls,
            "menu_rect"
        ):
            return False

        # ------------------------------------------
        # Mouse
        # ------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return False

            return self.controls.menu_rect.collidepoint(
                event.pos
            )

        # ------------------------------------------
        # Touch
        # ------------------------------------------

        if event.type == pygame.FINGERDOWN:

            x = int(
                event.x * self.width
            )

            y = int(
                event.y * self.height
            )

            return self.controls.menu_rect.collidepoint(
                x,
                y
            )

        return False

    # =================================================
    # EVENT
    # =================================================

    def handle_event(self, event):

        # ==========================================
        # منو
        # ==========================================

        if self.menu.active:

            result = self.menu.handle_event(
                event
            )

            if result == "Continue":

                self.menu.close()
                return

            elif result == "Restart":

                self.restart()
                self.menu.close()
                return

            elif result == "Settings":

                return

            elif result == "Stage":

                return

            elif result == "Exit":

                pygame.quit()
                raise SystemExit

            return

        # ==========================================
        # Game Over
        # ==========================================

        if self.death_screen.active:

            if self.is_menu_button_pressed(
                event
            ):

                self.menu.open(
                    game_over=True
                )

                return

            result = self.death_screen.handle_event(
                event
            )

            if result == "restart":

                self.restart()

            elif result == "exit":

                pygame.quit()
                raise SystemExit

            elif result == "menu":

                self.menu.open(
                    game_over=True
                )

            return

        # ==========================================
        # منوی معمولی
        # ==========================================

        if self.is_menu_button_pressed(
            event
        ):

            self.menu.open(
                game_over=False
            )

            return

        # ==========================================
        # کنترل‌ها
        # ==========================================

        self.controls.handle_event(
            event
        )

    # =================================================
    # حمله بازیکن
    # =================================================

    def player_attack(self):

        if self.player_attack_timer > 0:
            return

        punch_rect = (
            self.player.get_punch_rect()
        )

        # ==========================================
        # دشمن اول
        # ==========================================

        if self.enemy1.health > 0:

            self.enemy1.notice_player_attack(
                self.player
            )

            if punch_rect.colliderect(
                self.enemy1.get_rect()
            ):

                self.enemy1.take_damage(
                    self.player_attack_damage
                )

        # ==========================================
        # دشمن دوم
        # ==========================================

        if self.enemy2.health > 0:

            self.enemy2.notice_player_attack(
                self.player
            )

            if punch_rect.colliderect(
                self.enemy2.get_rect()
            ):

                self.enemy2.take_damage(
                    self.player_attack_damage
                )

        # ==========================================
        # انیمیشن مشت
        # ==========================================

        self.player.punch_animation.start(
            self.player.direction
        )

        # ==========================================
        # Cooldown
        # ==========================================

        self.player_attack_timer = (
            self.player_attack_cooldown
        )

    # =================================================
    # UPDATE
    # =================================================

    def update(self):

        # ==========================================
        # منو
        # ==========================================

        if self.menu.active:
            return

        # ==========================================
        # Game Over
        # ==========================================

        if self.death_screen.active:

            self.death_screen.update()

            return

        # ==========================================
        # تایمر مشت
        # ==========================================

        if self.player_attack_timer > 0:

            self.player_attack_timer -= 1

        # ==========================================
        # حرکت بازیکن
        # ==========================================

        dx, dy = (
            self.controls.get_movement()
        )

        self.player.move(
            dx,
            dy
        )

        # ==========================================
        # محدود کردن بازیکن
        # ==========================================

        keep_inside_room(
            self.player,
            self.room_rect
        )

        # ==========================================
        # آپدیت بازیکن
        # ==========================================

        self.player.update()

        # ==========================================
        # مرگ بازیکن
        # ==========================================

        if self.player.health <= 0:

            self.death_screen.activate()

            return

        # ==========================================
        # دشمن اول
        # ==========================================

        if self.enemy1.health > 0:

            self.enemy1.update(
                self.player
            )

            keep_inside_room(
                self.enemy1,
                self.room_rect
            )

        # ==========================================
        # دشمن دوم
        # ==========================================

        if self.enemy2.health > 0:

            self.enemy2.update(
                self.player
            )

            keep_inside_room(
                self.enemy2,
                self.room_rect
            )

        # ==========================================
        # جلوگیری از روی هم رفتن
        # ==========================================

        if self.enemy1.health > 0:

            separate_entities(
                self.player,
                self.enemy1,
                self.room_rect
            )

        if self.enemy2.health > 0:

            separate_entities(
                self.player,
                self.enemy2,
                self.room_rect
            )

        # ==========================================
        # حمله بازیکن
        # ==========================================

        if self.controls.attack_pressed():

            self.player_attack()

    # =================================================
    # RESTART
    # =================================================

    def restart(self):

        # ==========================================
        # پاک کردن کنترل‌های قبلی
        # ==========================================

        self.controls.fingers.clear()

        self.controls.mouse_touching = False

        self.controls.mouse_pos = (0, 0)

        if hasattr(
            self.controls,
            "diagonal_revealed"
        ):

            self.controls.diagonal_revealed.clear()

        if hasattr(
            self.controls,
            "attack_fingers"
        ):

            self.controls.attack_fingers.clear()

        if hasattr(
            self.controls,
            "attack_held"
        ):

            self.controls.attack_held.clear()

        # ==========================================
        # بازیکن
        # ==========================================

        self.player = Player(
            self.start_player_x,
            self.start_player_y
        )

        # ==========================================
        # دشمن‌ها
        # ==========================================

        self.enemy1 = Enemy(
            self.width // 2 - 60,
            500
        )

        self.enemy2 = Enemy(
            self.width // 2 + 60,
            500
        )

        # ==========================================
        # تایمر
        # ==========================================

        self.player_attack_timer = 0

        # ==========================================
        # Game Over
        # ==========================================

        self.death_screen.active = False

        self.death_screen.alpha = 0

        # ==========================================
        # مرحله بعد
        # ==========================================

        self.next_stage = None

        # ==========================================
        # منو
        # ==========================================

        self.menu.close()

    # =================================================
    # DRAW
    # =================================================

    def draw(self):

        # ==========================================
        # زمین سبز
        # ==========================================

        self.screen.fill(
            self.floor_color
        )

        # ==========================================
        # علف‌ها
        # ==========================================

        self.draw_grass()

        # ==========================================
        # دیوار
        # ==========================================

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            self.room_rect,
            width=8,
            border_radius=18
        )

        # ==========================================
        # دشمن اول
        # ==========================================

        if self.enemy1.health > 0:

            self.enemy1.draw(
                self.screen
            )

        # ==========================================
        # دشمن دوم
        # ==========================================

        if self.enemy2.health > 0:

            self.enemy2.draw(
                self.screen
            )

        # ==========================================
        # بازیکن
        # ==========================================

        self.player.draw(
            self.screen
        )

        # ==========================================
        # کنترل‌ها
        # ==========================================

        self.controls.draw(
            self.screen
        )

        # ==========================================
        # Game Over
        # ==========================================

        self.death_screen.draw(
            self.screen
        )

        # ==========================================
        # Menu
        # ==========================================

        self.menu.draw(
            self.screen
        )