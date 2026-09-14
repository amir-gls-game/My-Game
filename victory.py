import pygame
import random


class Victory:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.active = False

        # ==========================================
        # اندازه خروجی
        # ==========================================

        self.exit_width = 150

        self.current_exit_width = 0

        # باز شدن خروجی طی حدود 0.7 ثانیه
        self.exit_open_speed = (
            self.exit_width / 42
        )

        # ==========================================
        # ذرات کاغذ رنگی
        # ==========================================

        self.confetti = []

        self.confetti_timer = 0

        # ==========================================
        # متن Victory
        # ==========================================

        self.font = pygame.font.Font(
            None,
            150
        )

        self.letters_shown = 0

        self.write_timer = 0

        self.letter_delay = 4

        # ==========================================
        # شفافیت متن
        # ==========================================

        self.text_alpha = 0

        # ==========================================
        # چشمک زدن GO
        # ==========================================

        self.go_timer = 0

        # ==========================================
        # حرکت GO
        # ==========================================

        self.go_move_timer = 0

        # ==========================================
        # فونت GO
        # ==========================================

        self.go_font = pygame.font.Font(
            None,
            55
        )

    # =================================================
    # ACTIVATE
    # =================================================

    def activate(self):

        if self.active:
            return

        self.active = True

        # ==========================================
        # ریست Victory
        # ==========================================

        self.letters_shown = 0
        self.write_timer = 0
        self.text_alpha = 0

        # ==========================================
        # ریست خروجی
        # ==========================================

        self.current_exit_width = 0

        # ==========================================
        # ریست GO
        # ==========================================

        self.go_timer = 0
        self.go_move_timer = 0

        # ==========================================
        # ریست کاغذها
        # ==========================================

        self.confetti = []
        self.confetti_timer = 0

        # ==========================================
        # کاغذهای اولیه
        # ==========================================

        for i in range(35):

            side = random.choice(
                ["left", "right"]
            )

            if side == "left":

                x = random.randint(
                    -80,
                    0
                )

            else:

                x = random.randint(
                    self.width,
                    self.width + 80
                )

            y = random.randint(
                0,
                self.height
            )

            self.confetti.append(
                {
                    "x": x,
                    "y": y,

                    "vx": (
                        random.uniform(
                            2.0,
                            5.0
                        )
                        if side == "left"
                        else
                        random.uniform(
                            -5.0,
                            -2.0
                        )
                    ),

                    "vy": random.uniform(
                        -1.0,
                        2.5
                    ),

                    "size": random.randint(
                        6,
                        12
                    ),

                    "rotation": random.randint(
                        0,
                        360
                    ),

                    "rotation_speed": random.uniform(
                        -6,
                        6
                    ),

                    "color": random.choice(
                        [
                            (255, 70, 70),
                            (70, 160, 255),
                            (255, 220, 60),
                            (80, 220, 120),
                            (200, 90, 255),
                            (255, 140, 50)
                        ]
                    )
                }
            )

    # =================================================
    # UPDATE
    # =================================================

    def update(self):

        if not self.active:
            return

        # ==========================================
        # باز شدن تدریجی خروجی
        # ==========================================

        if self.current_exit_width < self.exit_width:

            self.current_exit_width += (
                self.exit_open_speed
            )

            if (
                self.current_exit_width
                > self.exit_width
            ):

                self.current_exit_width = (
                    self.exit_width
                )

        # ==========================================
        # نوشتن Victory
        # ==========================================

        if self.letters_shown < 7:

            self.write_timer += 1

            if self.write_timer >= self.letter_delay:

                self.write_timer = 0

                self.letters_shown += 1

        # ==========================================
        # ظاهر شدن متن
        # ==========================================

        if self.text_alpha < 255:

            self.text_alpha += 25

            if self.text_alpha > 255:

                self.text_alpha = 255

        # ==========================================
        # تایمر GO
        # ==========================================

        self.go_timer += 1

        # ==========================================
        # حرکت GO
        # ==========================================

        self.go_move_timer += 1

        # ==========================================
        # ساخت کاغذهای جدید
        # ==========================================

        self.confetti_timer += 1

        if self.confetti_timer >= 4:

            self.confetti_timer = 0

            for side in ["left", "right"]:

                if side == "left":

                    x = random.randint(
                        -50,
                        0
                    )

                    vx = random.uniform(
                        2.0,
                        5.0
                    )

                else:

                    x = random.randint(
                        self.width,
                        self.width + 50
                    )

                    vx = random.uniform(
                        -5.0,
                        -2.0
                    )

                self.confetti.append(
                    {
                        "x": x,

                        "y": random.randint(
                            0,
                            self.height
                        ),

                        "vx": vx,

                        "vy": random.uniform(
                            -1.5,
                            2.5
                        ),

                        "size": random.randint(
                            6,
                            12
                        ),

                        "rotation": random.randint(
                            0,
                            360
                        ),

                        "rotation_speed": random.uniform(
                            -6,
                            6
                        ),

                        "color": random.choice(
                            [
                                (255, 70, 70),
                                (70, 160, 255),
                                (255, 220, 60),
                                (80, 220, 120),
                                (200, 90, 255),
                                (255, 140, 50)
                            ]
                        )
                    }
                )

        # ==========================================
        # حرکت کاغذها
        # ==========================================

        for piece in self.confetti:

            piece["x"] += piece["vx"]

            piece["y"] += piece["vy"]

            piece["vy"] += 0.04

            piece["rotation"] += (
                piece["rotation_speed"]
            )

        # ==========================================
        # حذف کاغذهای دور
        # ==========================================

        self.confetti = [
            piece
            for piece in self.confetti
            if (
                -120 < piece["x"]
                < self.width + 120
                and
                -120 < piece["y"]
                < self.height + 120
            )
        ]

    # =================================================
    # EXIT
    # =================================================

    def is_exit(self, player_rect):

        if not self.active:
            return False

        exit_left = (
            self.width // 2
            - self.current_exit_width / 2
        )

        exit_right = (
            self.width // 2
            + self.current_exit_width / 2
        )

        if player_rect.top <= 20:

            if (
                player_rect.centerx >= exit_left
                and
                player_rect.centerx <= exit_right
            ):

                return True

        return False

    # =================================================
    # DRAW ARROW
    # =================================================

    def draw_arrow(
        self,
        screen,
        center_x,
        center_y,
        alpha
    ):

        surface = pygame.Surface(
            (60, 60),
            pygame.SRCALPHA
        )

        color = (
            255,
            60,
            60,
            alpha
        )

        # ==========================================
        # بدنه فلش
        # ==========================================

        pygame.draw.line(
            surface,
            color,
            (30, 48),
            (30, 15),
            6
        )

        # ==========================================
        # سر فلش
        # ==========================================

        pygame.draw.line(
            surface,
            color,
            (30, 15),
            (17, 29),
            6
        )

        pygame.draw.line(
            surface,
            color,
            (30, 15),
            (43, 29),
            6
        )

        rect = surface.get_rect(
            center=(
                center_x,
                center_y
            )
        )

        screen.blit(
            surface,
            rect
        )

    # =================================================
    # DRAW GO
    # =================================================

    def draw_go(
        self,
        screen,
        center_x,
        center_y
    ):

        # ==========================================
        # چشمک زدن
        # ==========================================

        cycle = self.go_timer % 50

        if cycle < 25:

            alpha = 255

        else:

            alpha = 110

        # ==========================================
        # حرکت عمودی
        # ==========================================

        movement = (
            (self.go_move_timer % 40) / 20
        )

        if movement > 1:

            movement = 2 - movement

        movement = movement * 10

        # ==========================================
        # سطح GO
        # ==========================================

        surface = pygame.Surface(
            (130, 150),
            pygame.SRCALPHA
        )

        color = (
            235,
            45,
            45,
            alpha
        )

        # ==========================================
        # O
        #
        # ابتدا عادی ساخته می‌شود
        # سپس 90 درجه می‌چرخد
        # ==========================================

        o_surface = self.go_font.render(
            "O",
            True,
            color
        )

        o_surface = pygame.transform.rotate(
            o_surface,
            90
        )

        o_rect = o_surface.get_rect(
            center=(
                65,
                42
            )
        )

        surface.blit(
            o_surface,
            o_rect
        )

        # ==========================================
        # G
        #
        # ابتدا عادی ساخته می‌شود
        # سپس 90 درجه می‌چرخد
        # ==========================================

        g_surface = self.go_font.render(
            "G",
            True,
            color
        )

        g_surface = pygame.transform.rotate(
            g_surface,
            90
        )

        g_rect = g_surface.get_rect(
            center=(
                65,
                98
            )
        )

        surface.blit(
            g_surface,
            g_rect
        )

        # ==========================================
        # قرار دادن GO
        # ==========================================

        rect = surface.get_rect(
            center=(
                center_x,
                center_y - movement
            )
        )

        screen.blit(
            surface,
            rect
        )

    # =================================================
    # DRAW
    # =================================================

    def draw(self, screen):

        if not self.active:
            return

        # ==========================================
        # کاغذهای رنگی
        # ==========================================

        for piece in self.confetti:

            size = piece["size"]

            surface = pygame.Surface(
                (
                    size * 2,
                    size * 2
                ),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                surface,
                piece["color"],
                (
                    size // 2,
                    size // 2,
                    size,
                    size
                )
            )

            rotated = pygame.transform.rotate(
                surface,
                piece["rotation"]
            )

            rect = rotated.get_rect(
                center=(
                    int(piece["x"]),
                    int(piece["y"])
                )
            )

            screen.blit(
                rotated,
                rect
            )

        # ==========================================
        # Victory
        # ==========================================

        word = "Victory"

        visible_text = word[
            :self.letters_shown
        ]

        if visible_text != "":

            text = self.font.render(
                visible_text,
                True,
                (
                    255,
                    220,
                    60
                )
            )

            text.set_alpha(
                self.text_alpha
            )

            text_rect = text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2
                )
            )

            screen.blit(
                text,
                text_rect
            )

        # ==========================================
        # GO و فلش
        # ==========================================

        if self.current_exit_width > 20:

            exit_center_x = (
                self.width // 2
            )

            # ======================================
            # موقعیت GO
            # ======================================

            go_center_y = 145

            # ======================================
            # فلش بالای GO
            # ======================================

            self.draw_arrow(
                screen,
                exit_center_x,
                72,
                255
            )

            # ======================================
            # GO چرخیده
            #
            #        ↑
            #        O
            #        G
            # ======================================

            self.draw_go(
                screen,
                exit_center_x,
                go_center_y
            )