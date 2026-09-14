import pygame


class PunchAnimation:

    def __init__(self):

        self.active = False
        self.timer = 0

        # مدت انیمیشن
        self.duration = 8

        # جهت مشت
        self.direction = "up"

    # ==================================================
    # شروع انیمیشن مشت
    # ==================================================

    def start(self, direction):

        if self.active:
            return

        self.active = True
        self.timer = self.duration
        self.direction = direction

    # ==================================================
    # بروزرسانی انیمیشن
    # ==================================================

    def update(self):

        if not self.active:
            return

        self.timer -= 1

        if self.timer <= 0:

            self.timer = 0
            self.active = False

    # ==================================================
    # مقدار جلو رفتن مشت
    # ==================================================

    def get_extension(self):

        if not self.active:
            return 0

        progress = (
            self.duration - self.timer
        ) / self.duration

        # نیمه اول: جلو رفتن
        if progress < 0.5:

            amount = progress / 0.5

        # نیمه دوم: برگشتن
        else:

            amount = (
                1 - progress
            ) / 0.5

        return int(28 * amount)

    # ==================================================
    # رسم مشت
    # ==================================================

    def draw(
        self,
        screen,
        player_rect,
        direction,
        player_color
    ):

        if not self.active:
            return

        extension = self.get_extension()

        punch_width = 25
        punch_height = 25

        # کمی روشن‌تر از رنگ بازیکن
        punch_color = (
            min(player_color[0] + 15, 255),
            min(player_color[1] + 15, 255),
            min(player_color[2] + 15, 255)
        )

        # ==================================================
        # بالا
        # ==================================================

        if direction == "up":

            rect = pygame.Rect(
                player_rect.centerx - punch_width // 2,
                player_rect.top
                - extension
                - punch_height,
                punch_width,
                punch_height
            )

        # ==================================================
        # پایین
        # ==================================================

        elif direction == "down":

            rect = pygame.Rect(
                player_rect.centerx - punch_width // 2,
                player_rect.bottom + extension,
                punch_width,
                punch_height
            )

        # ==================================================
        # چپ
        # ==================================================

        elif direction == "left":

            rect = pygame.Rect(
                player_rect.left
                - extension
                - punch_width,
                player_rect.centery - punch_height // 2,
                punch_width,
                punch_height
            )

        # ==================================================
        # راست
        # ==================================================

        else:

            rect = pygame.Rect(
                player_rect.right + extension,
                player_rect.centery - punch_height // 2,
                punch_width,
                punch_height
            )

        pygame.draw.rect(
            screen,
            punch_color,
            rect,
            border_radius=7
        )