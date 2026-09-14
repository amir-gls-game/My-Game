import pygame


class Menu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.active = False
        self.game_over_mode = False

        # -----------------------------------------
        # MENU PANEL
        # -----------------------------------------

        self.panel_width = 500
        self.panel_height = 560

        self.panel_rect = pygame.Rect(
            0,
            0,
            self.panel_width,
            self.panel_height
        )

        self.panel_rect.center = (
            self.width // 2,
            self.height // 2
        )

        # -----------------------------------------
        # FONTS
        # -----------------------------------------

        self.title_font = pygame.font.Font(
            None,
            58
        )

        self.button_font = pygame.font.Font(
            None,
            34
        )

        # -----------------------------------------
        # BUTTONS
        # -----------------------------------------

        self.buttons = []

        self.create_buttons()

    # =================================================
    # CREATE BUTTONS
    # =================================================

    def create_buttons(self):

        self.buttons = []

        if self.game_over_mode:

            names = [
                "Settings",
                "Stage"
            ]

        else:

            names = [
                "Continue",
                "Restart",
                "Settings",
                "Stage",
                "Exit"
            ]

        button_width = 400
        button_height = 70

        gap = 15

        total_height = (
            len(names) * button_height
            + (len(names) - 1) * gap
        )

        start_y = (
            self.panel_rect.centery
            - total_height // 2
            + 45
        )

        for index, name in enumerate(names):

            rect = pygame.Rect(
                0,
                0,
                button_width,
                button_height
            )

            rect.centerx = self.panel_rect.centerx

            rect.y = (
                start_y
                + index * (
                    button_height + gap
                )
            )

            self.buttons.append(
                {
                    "name": name,
                    "rect": rect
                }
            )

    # =================================================
    # OPEN
    # =================================================

    def open(self, game_over=False):

        self.active = True
        self.game_over_mode = game_over

        self.create_buttons()

    # =================================================
    # CLOSE
    # =================================================

    def close(self):

        self.active = False

    # =================================================
    # ICONS
    # =================================================

    def draw_continue_icon(
        self,
        screen,
        center
    ):

        x, y = center

        points = [
            (x - 9, y - 16),
            (x + 15, y),
            (x - 9, y + 16)
        ]

        pygame.draw.polygon(
            screen,
            (240, 240, 240),
            points
        )

    def draw_restart_icon(
        self,
        screen,
        center
    ):

        x, y = center

        pygame.draw.arc(
            screen,
            (240, 240, 240),
            (
                x - 16,
                y - 16,
                32,
                32
            ),
            0.5,
            5.5,
            4
        )

        points = [
            (x + 13, y - 15),
            (x + 18, y - 2),
            (x + 5, y - 4)
        ]

        pygame.draw.polygon(
            screen,
            (240, 240, 240),
            points
        )

    def draw_settings_icon(
        self,
        screen,
        center
    ):

        x, y = center

        pygame.draw.circle(
            screen,
            (240, 240, 240),
            (x, y),
            17,
            4
        )

        pygame.draw.circle(
            screen,
            (240, 240, 240),
            (x, y),
            6
        )

        for angle in (
            0,
            45,
            90,
            135,
            180,
            225,
            270,
            315
        ):

            direction = pygame.math.Vector2(
                1,
                0
            ).rotate(angle)

            start = (
                x + int(direction.x * 17),
                y + int(direction.y * 17)
            )

            end = (
                x + int(direction.x * 23),
                y + int(direction.y * 23)
            )

            pygame.draw.line(
                screen,
                (240, 240, 240),
                start,
                end,
                5
            )

    def draw_stage_icon(
        self,
        screen,
        center
    ):

        x, y = center

        # نقشه

        pygame.draw.rect(
            screen,
            (240, 240, 240),
            (
                x - 19,
                y - 17,
                38,
                34
            ),
            3
        )

        # مسیر روی نقشه

        pygame.draw.line(
            screen,
            (240, 240, 240),
            (
                x - 10,
                y + 8
            ),
            (
                x - 2,
                y - 5
            ),
            3
        )

        pygame.draw.line(
            screen,
            (240, 240, 240),
            (
                x - 2,
                y - 5
            ),
            (
                x + 10,
                y + 4
            ),
            3
        )

        # نقطه مرحله

        pygame.draw.circle(
            screen,
            (240, 240, 240),
            (
                x + 10,
                y - 7
            ),
            4
        )

    def draw_exit_icon(
        self,
        screen,
        center
    ):

        x, y = center

        # چارچوب در

        door_frame = pygame.Rect(
            x - 15,
            y - 22,
            25,
            44
        )

        pygame.draw.rect(
            screen,
            (240, 240, 240),
            door_frame,
            4
        )

        # درِ باز شده

        points = [
            (x - 10, y - 17),
            (x + 12, y - 8),
            (x + 12, y + 17),
            (x - 10, y + 8)
        ]

        pygame.draw.polygon(
            screen,
            (240, 240, 240),
            points,
            3
        )

        # فلش خروج

        pygame.draw.line(
            screen,
            (240, 240, 240),
            (
                x + 5,
                y
            ),
            (
                x + 30,
                y
            ),
            4
        )

        pygame.draw.line(
            screen,
            (240, 240, 240),
            (
                x + 30,
                y
            ),
            (
                x + 20,
                y - 8
            ),
            4
        )

        pygame.draw.line(
            screen,
            (240, 240, 240),
            (
                x + 30,
                y
            ),
            (
                x + 20,
                y + 8
            ),
            4
        )

    # =================================================
    # DRAW ICON
    # =================================================

    def draw_icon(
        self,
        screen,
        name,
        center
    ):

        if name == "Continue":

            self.draw_continue_icon(
                screen,
                center
            )

        elif name == "Restart":

            self.draw_restart_icon(
                screen,
                center
            )

        elif name == "Settings":

            self.draw_settings_icon(
                screen,
                center
            )

        elif name == "Stage":

            self.draw_stage_icon(
                screen,
                center
            )

        elif name == "Exit":

            self.draw_exit_icon(
                screen,
                center
            )

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

        for button in self.buttons:

            if button["rect"].collidepoint(
                position
            ):

                return button["name"]

        # کلیک بیرون منو

        if not self.panel_rect.collidepoint(
            position
        ):

            self.close()

        return None

    # =================================================
    # DRAW
    # =================================================

    def draw(self, screen):

        if not self.active:
            return

        # -----------------------------------------
        # DARK OVERLAY
        # -----------------------------------------

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
                170
            )
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # -----------------------------------------
        # PANEL
        # -----------------------------------------

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            self.panel_rect,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (110, 110, 110),
            self.panel_rect,
            3,
            border_radius=20
        )

        # -----------------------------------------
        # TITLE
        # -----------------------------------------

        title = self.title_font.render(
            "MENU",
            True,
            (245, 245, 245)
        )

        title_rect = title.get_rect(
            center=(
                self.panel_rect.centerx,
                self.panel_rect.top + 55
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # -----------------------------------------
        # BUTTONS
        # -----------------------------------------

        for button in self.buttons:

            rect = button["rect"]
            name = button["name"]

            pygame.draw.rect(
                screen,
                (50, 50, 50),
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                (100, 100, 100),
                rect,
                2,
                border_radius=12
            )

            icon_center = (
                rect.left + 45,
                rect.centery
            )

            self.draw_icon(
                screen,
                name,
                icon_center
            )

            text = self.button_font.render(
                name,
                True,
                (240, 240, 240)
            )

            text_rect = text.get_rect(
                midleft=(
                    rect.left + 85,
                    rect.centery
                )
            )

            screen.blit(
                text,
                text_rect
            )