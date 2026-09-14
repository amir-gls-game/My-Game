import pygame


class DeathScreen:

    def __init__(self, width, height, controls=None):

        self.width = width
        self.height = height

        # کنترل‌های بازی
        self.controls = controls

        self.active = False

        # تعداد فریم برای ظاهر شدن صفحه مرگ
        self.fade_speed = 20

        self.alpha = 0

        # ----------------------------
        # Buttons
        # ----------------------------

        self.restart_rect = pygame.Rect(
            0, 0, 170, 60
        )

        self.menu_rect = pygame.Rect(
            0, 0, 70, 60
        )

        self.exit_rect = pygame.Rect(
            0, 0, 130, 60
        )

        self.update_button_positions()

        self.font = pygame.font.Font(
            None,
            82
        )

        self.button_font = pygame.font.Font(
            None,
            38
        )

    # =================================================
    # RESET CONTROLS
    # =================================================

    def reset_controls(self):

        if self.controls is None:
            return

        # پاک کردن تمام انگشت‌های فعال
        self.controls.fingers.clear()

        # پاک کردن لمس موس
        self.controls.mouse_touching = False

        self.controls.mouse_pos = (0, 0)

        # اگر نسخه Controls جدید این متغیرها را داشته باشد
        # آنها هم کاملاً ریست می‌شوند.

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

        # هر state موقتی دیگری که بعداً اضافه شود
        if hasattr(
            self.controls,
            "attack_held"
        ):
            self.controls.attack_held.clear()

    # =================================================
    # BUTTON POSITIONS
    # =================================================

    def update_button_positions(self):

        gap = 15

        total_width = (
            self.exit_rect.width
            + gap
            + self.menu_rect.width
            + gap
            + self.restart_rect.width
        )

        start_x = (
            self.width - total_width
        ) // 2

        button_y = (
            self.height // 2 + 70
        )

        # LEFT = EXIT
        self.exit_rect.topleft = (
            start_x,
            button_y
        )

        # CENTER = MENU
        self.menu_rect.topleft = (
            self.exit_rect.right + gap,
            button_y
        )

        # RIGHT = RESTART
        self.restart_rect.topleft = (
            self.menu_rect.right + gap,
            button_y
        )

    # =================================================
    # ACTIVATE
    # =================================================

    def activate(self):

        if self.active:
            return

        # ---------------------------------------------
        # خیلی مهم:
        # لحظه مرگ تمام لمس‌های قبلی پاک می‌شوند
        # ---------------------------------------------

        self.reset_controls()

        self.active = True

        self.alpha = 0

    # =================================================
    # UPDATE
    # =================================================

    def update(self):

        if not self.active:
            return

        if self.alpha < 255:

            self.alpha += 13

            if self.alpha > 255:
                self.alpha = 255

    # =================================================
    # EVENT
    # =================================================

    def handle_event(self, event):

        if not self.active:
            return None

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        position = event.pos

        # LEFT = EXIT
        if self.exit_rect.collidepoint(
            position
        ):
            return "exit"

        # CENTER = MENU
        if self.menu_rect.collidepoint(
            position
        ):
            return "menu"

        # RIGHT = RESTART
        if self.restart_rect.collidepoint(
            position
        ):
            return "restart"

        return None

    # =================================================
    # DRAW
    # =================================================

    def draw(self, screen):

        if not self.active:
            return

        alpha = int(
            max(
                0,
                min(
                    255,
                    self.alpha
                )
            )
        )

        # ----------------------------
        # Dark overlay
        # ----------------------------

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                0,
                0,
                0,
                min(alpha, 190)
            )
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # ----------------------------
        # GAME OVER
        # ----------------------------

        title_surface = self.font.render(
            "Game Over",
            True,
            (
                255,
                255,
                255
            )
        )

        title_surface.set_alpha(
            alpha
        )

        title_rect = title_surface.get_rect(
            center=(
                self.width // 2,
                self.height // 2 - 40
            )
        )

        screen.blit(
            title_surface,
            title_rect
        )

        # ----------------------------
        # EXIT
        # ----------------------------

        self.draw_button(
            screen,
            self.exit_rect,
            "Exit",
            alpha
        )

        # ----------------------------
        # MENU
        # ----------------------------

        self.draw_menu_button(
            screen,
            self.menu_rect,
            alpha
        )

        # ----------------------------
        # RESTART
        # ----------------------------

        self.draw_button(
            screen,
            self.restart_rect,
            "Restart",
            alpha
        )

    # =================================================
    # NORMAL BUTTON
    # =================================================

    def draw_button(
        self,
        screen,
        rect,
        text,
        alpha
    ):

        pygame.draw.rect(
            screen,
            (
                45,
                45,
                45
            ),
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (
                100,
                100,
                100
            ),
            rect,
            width=2,
            border_radius=12
        )

        text_surface = self.button_font.render(
            text,
            True,
            (
                240,
                240,
                240
            )
        )

        text_surface.set_alpha(
            alpha
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    # =================================================
    # GRAPHICAL MENU BUTTON
    # =================================================

    def draw_menu_button(
        self,
        screen,
        rect,
        alpha
    ):

        # ----------------------------
        # Button
        # ----------------------------

        pygame.draw.rect(
            screen,
            (
                45,
                45,
                45
            ),
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (
                100,
                100,
                100
            ),
            rect,
            width=2,
            border_radius=12
        )

        # ----------------------------
        # Three lines
        # ----------------------------

        line_color = (
            240,
            240,
            240
        )

        center_x = rect.centerx
        center_y = rect.centery

        line_width = 28
        thickness = 4

        for y in (
            center_y - 9,
            center_y,
            center_y + 9
        ):

            pygame.draw.line(
                screen,
                line_color,
                (
                    center_x - line_width // 2,
                    y
                ),
                (
                    center_x + line_width // 2,
                    y
                ),
                thickness
            )