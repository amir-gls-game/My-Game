import pygame
from animation import PunchAnimation


class Player:

    def __init__(self, x, y):

        # ==============================
        # اندازه بازیکن
        # ==============================

        self.width = 60
        self.height = 60

        # ==============================
        # موقعیت
        # ==============================

        self.x = x
        self.y = y

        # ==============================
        # سرعت
        # ==============================

        self.speed = 5.8

        # ==============================
        # رنگ
        # ==============================

        self.color = (40, 200, 80)

        # رنگ نقطه جهت
        self.direction_color = (75, 235, 115)

        # ==============================
        # جهت نگاه
        # ==============================

        self.direction = "up"

        # ==============================
        # جان
        # ==============================

        self.max_health = 100
        self.health = 100

        # ==============================
        # افکت ضربه خوردن
        # ==============================

        self.hit_timer = 0

        # ==============================
        # انیمیشن مشت
        # ==============================

        self.punch_animation = PunchAnimation()

    # ==================================================
    # مستطیل بازیکن
    # ==================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    # ==================================================
    # محدوده مشت
    # ==================================================

    def get_punch_rect(self):

        rect = self.get_rect()

        punch_width = 45
        punch_height = 45

        # --------------------------------
        # مشت به بالا
        # --------------------------------

        if self.direction == "up":

            return pygame.Rect(
                rect.centerx - punch_width // 2,
                rect.top - punch_height,
                punch_width,
                punch_height
            )

        # --------------------------------
        # مشت به پایین
        # --------------------------------

        elif self.direction == "down":

            return pygame.Rect(
                rect.centerx - punch_width // 2,
                rect.bottom,
                punch_width,
                punch_height
            )

        # --------------------------------
        # مشت به چپ
        # --------------------------------

        elif self.direction == "left":

            return pygame.Rect(
                rect.left - punch_width,
                rect.centery - punch_height // 2,
                punch_width,
                punch_height
            )

        # --------------------------------
        # مشت به راست
        # --------------------------------

        else:

            return pygame.Rect(
                rect.right,
                rect.centery - punch_height // 2,
                punch_width,
                punch_height
            )

    # ==================================================
    # حرکت
    # ==================================================

    def move(self, dx, dy):

        # --------------------------------
        # تشخیص جهت
        # --------------------------------

        if dx > 0:
            self.direction = "right"

        elif dx < 0:
            self.direction = "left"

        elif dy > 0:
            self.direction = "down"

        elif dy < 0:
            self.direction = "up"

        # --------------------------------
        # حرکت
        # --------------------------------

        self.x += dx * self.speed
        self.y += dy * self.speed

    # ==================================================
    # دریافت آسیب
    # ==================================================

    def take_damage(self, damage):

        self.health -= damage

        if self.health < 0:
            self.health = 0

        # افکت ضربه
        self.hit_timer = 8

    # ==================================================
    # بروزرسانی
    # ==================================================

    def update(self):

        # افکت ضربه خوردن
        if self.hit_timer > 0:

            self.hit_timer -= 1

        # انیمیشن مشت
        self.punch_animation.update()

    # ==================================================
    # نوار سلامتی
    # ==================================================

    def draw_health_bar(self, screen, rect):

        bar_width = 70
        bar_height = 8
        bar_gap = 12

        bar_x = (
            rect.centerx
            - bar_width // 2
        )

        bar_y = (
            rect.top
            - bar_gap
            - bar_height
        )

        # پس‌زمینه
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

        # مقدار سلامتی
        health_ratio = (
            self.health
            / self.max_health
        )

        current_width = int(
            bar_width * health_ratio
        )

        if current_width > 0:

            pygame.draw.rect(
                screen,
                (50, 220, 80),
                (
                    bar_x,
                    bar_y,
                    current_width,
                    bar_height
                )
            )

        # کادر
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

    # ==================================================
    # رسم بازیکن
    # ==================================================

    def draw(self, screen):

        # --------------------------------
        # رنگ هنگام ضربه
        # --------------------------------

        if self.hit_timer > 0:

            color = (
                120,
                255,
                150
            )

            direction_color = (
                150,
                255,
                175
            )

        else:

            color = self.color
            direction_color = (
                self.direction_color
            )

        # --------------------------------
        # مربع بازیکن
        # --------------------------------

        rect = self.get_rect()

        pygame.draw.rect(
            screen,
            color,
            rect
        )

        # --------------------------------
        # نوار سلامتی
        # --------------------------------

        self.draw_health_bar(
            screen,
            rect
        )

        # --------------------------------
        # محل نقطه جهت
        # --------------------------------

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

        # --------------------------------
        # نقطه جهت
        # --------------------------------

        pygame.draw.circle(
            screen,
            direction_color,
            dot_pos,
            dot_radius
        )

        # --------------------------------
        # رسم انیمیشن مشت
        # --------------------------------

        self.punch_animation.draw(
            screen,
            rect,
            self.direction,
            color
        )