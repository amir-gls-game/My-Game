import pygame

from player import Player
from enemy import Enemy
from controls import Controls
from collision import keep_inside_room, separate_entities
from death import DeathScreen
from menu import Menu
from victory import Victory


class Stage1:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        # ==========================================
        # محیط
        # ==========================================

        self.floor_color = (
            110,
            110,
            110
        )

        self.room_rect = pygame.Rect(
            20,
            20,
            self.width - 40,
            self.height - 40
        )

        # ==========================================
        # بازیکن
        # ==========================================

        self.player = Player(
            self.width // 2 - 30,
            self.height - 600
        )

        # ==========================================
        # دشمن
        # ==========================================

        self.enemy = Enemy(
            self.width // 2 - 30,
            500
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
        # منوی بازی
        # ==========================================

        self.menu = Menu(
            self.width,
            self.height
        )

        # ==========================================
        # پیروزی
        # ==========================================

        self.victory = Victory(
            self.width,
            self.height
        )

        # ==========================================
        # مرحله بعد
        # ==========================================

        self.next_stage = None

        # ==========================================
        # وضعیت Transition
        # ==========================================

        self.transition_ready = False

        # در این حالت مرحله دیگر نباید حرکت کند
        self.transition_locked = False

        # ==========================================
        # حمله بازیکن
        # ==========================================

        self.player_attack_damage = 20

        self.player_attack_cooldown = 25

        self.player_attack_timer = 0

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
        # اگر Transition آماده/قفل شده
        # ==========================================

        if self.transition_locked:

            return

        # ==========================================
        # اگر منوی بازی باز است
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
        # اگر Game Over فعال است
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
        # کنترل‌های بازی
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

        if self.enemy.health <= 0:

            return

        # ------------------------------------------
        # دشمن متوجه حمله می‌شود
        # ------------------------------------------

        self.enemy.notice_player_attack(
            self.player
        )

        # ------------------------------------------
        # محدوده مشت
        # ------------------------------------------

        punch_rect = (
            self.player.get_punch_rect()
        )

        enemy_rect = (
            self.enemy.get_rect()
        )

        # ------------------------------------------
        # Damage
        # ------------------------------------------

        if punch_rect.colliderect(
            enemy_rect
        ):

            self.enemy.take_damage(
                self.player_attack_damage
            )

        # ------------------------------------------
        # انیمیشن مشت
        # ------------------------------------------

        self.player.punch_animation.start(
            self.player.direction
        )

        # ------------------------------------------
        # Cooldown
        # ------------------------------------------

        self.player_attack_timer = (
            self.player_attack_cooldown
        )

    # =================================================
    # UPDATE
    # =================================================

    def update(self):

        # ==========================================
        # اگر انتقال قفل شده
        # ==========================================

        if self.transition_locked:

            return

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
        # محدودیت حرکت
        # ==========================================

        if self.victory.active:

            # --------------------------------------
            # عرض خروجی
            # --------------------------------------

            exit_width = (
                self.victory.current_exit_width
            )

            exit_left = (
                self.width // 2
                - exit_width // 2
            )

            exit_right = (
                self.width // 2
                + exit_width // 2
            )

            player_rect = (
                self.player.get_rect()
            )

            # --------------------------------------
            # سمت چپ
            # --------------------------------------

            if (
                player_rect.left
                < self.room_rect.left
            ):

                self.player.x = (
                    self.room_rect.left
                )

            # --------------------------------------
            # سمت راست
            # --------------------------------------

            if (
                player_rect.right
                > self.room_rect.right
            ):

                self.player.x = (
                    self.room_rect.right
                    - self.player.width
                )

            # --------------------------------------
            # پایین
            # --------------------------------------

            if (
                player_rect.bottom
                > self.room_rect.bottom
            ):

                self.player.y = (
                    self.room_rect.bottom
                    - self.player.height
                )

            # --------------------------------------
            # بالای اتاق
            # فقط از خروجی اجازه عبور دارد
            # --------------------------------------

            if (
                player_rect.top
                < self.room_rect.top
                and
                not (
                    player_rect.centerx
                    >= exit_left
                    and
                    player_rect.centerx
                    <= exit_right
                )
            ):

                self.player.y = (
                    self.room_rect.top
                )

            # --------------------------------------
            # بازیکن از در خارج شد
            # --------------------------------------

            if self.victory.is_exit(
                self.player.get_rect()
            ):

                # ----------------------------------
                # آماده شدن برای Transition
                # ----------------------------------

                self.transition_ready = True

                self.transition_locked = True

                self.next_stage = "stage2"

                # ----------------------------------
                # کنترل‌ها کاملاً متوقف شوند
                # ----------------------------------

                self.controls.fingers.clear()

                self.controls.mouse_touching = False

                self.controls.mouse_pos = (
                    0,
                    0
                )

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

                return

        else:

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
        # آپدیت دشمن
        # ==========================================

        if self.enemy.health > 0:

            self.enemy.update(
                self.player
            )

            keep_inside_room(
                self.enemy,
                self.room_rect
            )

            separate_entities(
                self.player,
                self.enemy,
                self.room_rect
            )

        # ==========================================
        # بررسی کشته شدن دشمن
        # ==========================================

        if (
            self.enemy.health <= 0
            and
            not self.victory.active
        ):

            self.victory.activate()

        # ==========================================
        # حمله بازیکن
        # ==========================================

        if (
            not self.victory.active
            and
            self.controls.attack_pressed()
        ):

            self.player_attack()

        # ==========================================
        # آپدیت Victory
        # ==========================================

        if self.victory.active:

            self.victory.update()

    # =================================================
    # RESTART
    # =================================================

    def restart(self):

        # ==========================================
        # کنترل‌ها
        # ==========================================

        self.controls.fingers.clear()

        self.controls.mouse_touching = False

        self.controls.mouse_pos = (
            0,
            0
        )

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
            self.width // 2 - 30,
            self.height - 600
        )

        # ==========================================
        # دشمن
        # ==========================================

        self.enemy = Enemy(
            self.width // 2 - 30,
            500
        )

        # ==========================================
        # تایمر حمله
        # ==========================================

        self.player_attack_timer = 0

        # ==========================================
        # Game Over
        # ==========================================

        self.death_screen.active = False

        self.death_screen.alpha = 0

        # ==========================================
        # Victory
        # ==========================================

        self.victory.active = False

        self.victory.confetti = []

        self.victory.text_alpha = 0

        self.victory.current_exit_width = 0

        # ==========================================
        # Transition
        # ==========================================

        self.transition_ready = False

        self.transition_locked = False

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
        # زمین
        # ==========================================

        self.screen.fill(
            self.floor_color
        )

        # ==========================================
        # دیوار
        # ==========================================

        if not self.victory.active:

            pygame.draw.rect(
                self.screen,
                (70, 70, 70),
                self.room_rect,
                width=8,
                border_radius=18
            )

        else:

            # --------------------------------------
            # عرض خروجی
            # --------------------------------------

            exit_width = (
                self.victory.current_exit_width
            )

            exit_left = (
                self.width // 2
                - exit_width // 2
            )

            exit_right = (
                self.width // 2
                + exit_width // 2
            )

            # --------------------------------------
            # دیوار بالایی - چپ خروجی
            # --------------------------------------

            pygame.draw.line(
                self.screen,
                (70, 70, 70),
                (
                    self.room_rect.left,
                    self.room_rect.top
                ),
                (
                    exit_left,
                    self.room_rect.top
                ),
                8
            )

            # --------------------------------------
            # دیوار بالایی - راست خروجی
            # --------------------------------------

            pygame.draw.line(
                self.screen,
                (70, 70, 70),
                (
                    exit_right,
                    self.room_rect.top
                ),
                (
                    self.room_rect.right,
                    self.room_rect.top
                ),
                8
            )

            # --------------------------------------
            # دیوار چپ
            # --------------------------------------

            pygame.draw.line(
                self.screen,
                (70, 70, 70),
                (
                    self.room_rect.left,
                    self.room_rect.top
                ),
                (
                    self.room_rect.left,
                    self.room_rect.bottom
                ),
                8
            )

            # --------------------------------------
            # دیوار راست
            # --------------------------------------

            pygame.draw.line(
                self.screen,
                (70, 70, 70),
                (
                    self.room_rect.right,
                    self.room_rect.top
                ),
                (
                    self.room_rect.right,
                    self.room_rect.bottom
                ),
                8
            )

            # --------------------------------------
            # دیوار پایین
            # --------------------------------------

            pygame.draw.line(
                self.screen,
                (70, 70, 70),
                (
                    self.room_rect.left,
                    self.room_rect.bottom
                ),
                (
                    self.room_rect.right,
                    self.room_rect.bottom
                ),
                8
            )

        # ==========================================
        # Victory
        # ==========================================

        self.victory.draw(
            self.screen
        )

        # ==========================================
        # دشمن
        # ==========================================

        if self.enemy.health > 0:

            self.enemy.draw(
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