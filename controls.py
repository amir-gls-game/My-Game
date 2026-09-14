import pygame


class Controls:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # ==================================================
        # اندازه دکمه‌ها
        # ==================================================

        self.button_size = 130
        self.diagonal_size = 105
        self.attack_size = 150

        # ==================================================
        # موقعیت کنترل‌های حرکت
        # ==================================================

        cx = 210
        cy = height - 270

        self.up_rect = pygame.Rect(
            cx - self.button_size // 2,
            cy - 190,
            self.button_size,
            self.button_size
        )

        self.down_rect = pygame.Rect(
            cx - self.button_size // 2,
            cy + 60,
            self.button_size,
            self.button_size
        )

        self.left_rect = pygame.Rect(
            cx - 190,
            cy - self.button_size // 2,
            self.button_size,
            self.button_size
        )

        self.right_rect = pygame.Rect(
            cx + 60,
            cy - self.button_size // 2,
            self.button_size,
            self.button_size
        )

        # ==================================================
        # دکمه‌های مورب
        # ==================================================

        self.forward_left_rect = pygame.Rect(
            self.up_rect.left - self.diagonal_size - 20,
            self.up_rect.top + 10,
            self.diagonal_size,
            self.diagonal_size
        )

        self.forward_right_rect = pygame.Rect(
            self.up_rect.right + 20,
            self.up_rect.top + 10,
            self.diagonal_size,
            self.diagonal_size
        )

        self.backward_left_rect = pygame.Rect(
            self.down_rect.left - self.diagonal_size - 20,
            self.down_rect.top + 10,
            self.diagonal_size,
            self.diagonal_size
        )

        self.backward_right_rect = pygame.Rect(
            self.down_rect.right + 20,
            self.down_rect.top + 10,
            self.diagonal_size,
            self.diagonal_size
        )

        # ==================================================
        # دکمه مشت
        # ==================================================

        self.attack_rect = pygame.Rect(
            width - 230,
            height - 300,
            self.attack_size,
            self.attack_size
        )

        # ==================================================
        # دکمه منو
        # ==================================================

        self.menu_size = 90

        self.menu_rect = pygame.Rect(
            width - self.menu_size - 30,
            30,
            self.menu_size,
            self.menu_size
        )

        # ==================================================
        # چندلمسی
        # ==================================================

        self.fingers = {}

        # برای هر انگشت مشخص می‌کنیم که
        # آیا مورب‌ها را باز کرده یا نه
        #
        # finger_id : True / False
        self.diagonal_revealed = {}

        # ==================================================
        # وضعیت مشت
        # ==================================================

        # برای جلوگیری از مشت زدن پشت سر هم هنگام نگه داشتن
        self.attack_fingers = set()

        self.mouse_touching = False
        self.mouse_pos = (0, 0)

        self.mouse_diagonal_revealed = False
        self.mouse_attack_pressed = False

    # ==================================================
    # دریافت لمس
    # ==================================================

    def handle_event(self, event):

        # --------------------------------------------------
        # لمس واقعی موبایل
        # --------------------------------------------------

        if event.type == pygame.FINGERDOWN:

            finger_id = event.finger_id

            x = int(event.x * self.width)
            y = int(event.y * self.height)

            self.fingers[finger_id] = (x, y)

            # ----------------------------------------------
            # آیا لمس از ابتدا روی بالا یا پایین شروع شده؟
            # ----------------------------------------------

            if (
                self.up_rect.collidepoint(x, y)
                or
                self.down_rect.collidepoint(x, y)
            ):

                self.diagonal_revealed[finger_id] = True

            else:

                # اگر مستقیماً روی مورب مخفی زده شود،
                # مورب باز نمی‌شود.
                self.diagonal_revealed[finger_id] = False

            # ----------------------------------------------
            # مشت
            #
            # فقط همان لحظه یک بار ثبت می‌شود
            # ----------------------------------------------

            if self.attack_rect.collidepoint(x, y):

                self.attack_fingers.add(
                    finger_id
                )

        elif event.type == pygame.FINGERMOTION:

            finger_id = event.finger_id

            if finger_id in self.fingers:

                x = int(event.x * self.width)
                y = int(event.y * self.height)

                self.fingers[finger_id] = (x, y)

        elif event.type == pygame.FINGERUP:

            finger_id = event.finger_id

            # ----------------------------------------------
            # حذف انگشت
            # ----------------------------------------------

            if finger_id in self.fingers:

                del self.fingers[finger_id]

            # ----------------------------------------------
            # حذف وضعیت مورب
            # ----------------------------------------------

            if finger_id in self.diagonal_revealed:

                del self.diagonal_revealed[
                    finger_id
                ]

            # ----------------------------------------------
            # مشت
            # ----------------------------------------------

            if finger_id in self.attack_fingers:

                self.attack_fingers.remove(
                    finger_id
                )

        # --------------------------------------------------
        # موس / تست روی کامپیوتر
        # --------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                self.mouse_touching = True

                self.mouse_pos = event.pos

                # ------------------------------------------
                # باز شدن مورب
                # ------------------------------------------

                if (
                    self.up_rect.collidepoint(
                        *event.pos
                    )
                    or
                    self.down_rect.collidepoint(
                        *event.pos
                    )
                ):

                    self.mouse_diagonal_revealed = True

                else:

                    self.mouse_diagonal_revealed = False

                # ------------------------------------------
                # مشت
                # ------------------------------------------

                if self.attack_rect.collidepoint(
                    *event.pos
                ):

                    self.mouse_attack_pressed = True

        elif event.type == pygame.MOUSEMOTION:

            if self.mouse_touching:

                self.mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                self.mouse_touching = False

                self.mouse_diagonal_revealed = False

                self.mouse_attack_pressed = False

    # ==================================================
    # گرفتن تمام موقعیت‌های لمس
    # ==================================================

    def get_touch_positions(self):

        positions = list(
            self.fingers.values()
        )

        if self.mouse_touching:

            positions.append(
                self.mouse_pos
            )

        return positions

    # ==================================================
    # آیا یک انگشت مورب‌ها را باز کرده؟
    # ==================================================

    def diagonal_is_revealed(self):

        for finger_id in self.fingers:

            if self.diagonal_revealed.get(
                finger_id,
                False
            ):

                return True

        if (
            self.mouse_touching
            and
            self.mouse_diagonal_revealed
        ):

            return True

        return False

    # ==================================================
    # حرکت
    # ==================================================

    def get_movement(self):

        dx = 0
        dy = 0

        # ==================================================
        # لمس‌های واقعی موبایل
        # ==================================================

        for finger_id, (x, y) in self.fingers.items():

            # ----------------------------------------------
            # بالا
            # ----------------------------------------------

            if self.up_rect.collidepoint(x, y):

                dy -= 1

            # ----------------------------------------------
            # پایین
            # ----------------------------------------------

            elif self.down_rect.collidepoint(x, y):

                dy += 1

            # ----------------------------------------------
            # چپ
            # ----------------------------------------------

            elif self.left_rect.collidepoint(x, y):

                dx -= 1

            # ----------------------------------------------
            # راست
            # ----------------------------------------------

            elif self.right_rect.collidepoint(x, y):

                dx += 1

            # ----------------------------------------------
            # مورب بالا-چپ
            #
            # فقط اگر این انگشت قبلاً از بالا
            # شروع کرده باشد
            # ----------------------------------------------

            elif (
                self.diagonal_revealed.get(
                    finger_id,
                    False
                )
                and
                self.forward_left_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx -= 1
                dy -= 1

            # ----------------------------------------------
            # مورب بالا-راست
            # ----------------------------------------------

            elif (
                self.diagonal_revealed.get(
                    finger_id,
                    False
                )
                and
                self.forward_right_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx += 1
                dy -= 1

            # ----------------------------------------------
            # مورب پایین-چپ
            # ----------------------------------------------

            elif (
                self.diagonal_revealed.get(
                    finger_id,
                    False
                )
                and
                self.backward_left_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx -= 1
                dy += 1

            # ----------------------------------------------
            # مورب پایین-راست
            # ----------------------------------------------

            elif (
                self.diagonal_revealed.get(
                    finger_id,
                    False
                )
                and
                self.backward_right_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx += 1
                dy += 1

        # ==================================================
        # موس
        # ==================================================

        if self.mouse_touching:

            x, y = self.mouse_pos

            if self.up_rect.collidepoint(x, y):

                dy -= 1

            elif self.down_rect.collidepoint(x, y):

                dy += 1

            elif self.left_rect.collidepoint(x, y):

                dx -= 1

            elif self.right_rect.collidepoint(x, y):

                dx += 1

            elif (
                self.mouse_diagonal_revealed
                and
                self.forward_left_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx -= 1
                dy -= 1

            elif (
                self.mouse_diagonal_revealed
                and
                self.forward_right_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx += 1
                dy -= 1

            elif (
                self.mouse_diagonal_revealed
                and
                self.backward_left_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx -= 1
                dy += 1

            elif (
                self.mouse_diagonal_revealed
                and
                self.backward_right_rect.collidepoint(
                    x,
                    y
                )
            ):

                dx += 1
                dy += 1

        # ==================================================
        # جلوگیری از سرعت بیشتر
        # ==================================================

        dx = max(
            -1,
            min(1, dx)
        )

        dy = max(
            -1,
            min(1, dy)
        )

        return dx, dy

    # ==================================================
    # مشت
    # ==================================================

    def attack_pressed(self):

        # ----------------------------------------------
        # این متغیر فقط وقتی True می‌شود که
        # انگشت تازه روی دکمه مشت قرار گرفته باشد.
        #
        # نگه داشتن دکمه باعث تکرار نمی‌شود.
        # ----------------------------------------------

        for finger_id in list(
            self.attack_fingers
        ):

            if finger_id in self.fingers:

                x, y = self.fingers[
                    finger_id
                ]

                if self.attack_rect.collidepoint(
                    x,
                    y
                ):

                    self.attack_fingers.remove(
                        finger_id
                    )

                    return True

                else:

                    # اگر انگشت از مشت خارج شد،
                    # آماده ضربه بعدی می‌شود.
                    self.attack_fingers.remove(
                        finger_id
                    )

        # ----------------------------------------------
        # موس
        # ----------------------------------------------

        if self.mouse_attack_pressed:

            x, y = self.mouse_pos

            if self.attack_rect.collidepoint(
                x,
                y
            ):

                self.mouse_attack_pressed = False

                return True

            else:

                self.mouse_attack_pressed = False

        return False

    # ==================================================
    # رسم بدنه دکمه
    # ==================================================

    def draw_button_base(
        self,
        screen,
        rect,
        active=False
    ):

        if active:

            fill_color = (
                150,
                150,
                150
            )

        else:

            fill_color = (
                90,
                90,
                90
            )

        pygame.draw.rect(
            screen,
            fill_color,
            rect,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (
                180,
                180,
                180
            ),
            rect,
            width=4,
            border_radius=20
        )

    # ==================================================
    # بررسی فعال بودن یک دکمه
    # ==================================================

    def is_pressed(self, rect):

        positions = self.get_touch_positions()

        for x, y in positions:

            if rect.collidepoint(
                x,
                y
            ):

                return True

        return False

    # ==================================================
    # رسم فلش
    # ==================================================

    def draw_arrow(
        self,
        screen,
        rect,
        dx,
        dy,
        active=False
    ):

        cx = rect.centerx
        cy = rect.centery

        length = 35
        head = 18

        if active:

            color = (
                255,
                255,
                255
            )

        else:

            color = (
                230,
                230,
                230
            )

        start_x = cx - dx * length
        start_y = cy - dy * length

        end_x = cx + dx * length
        end_y = cy + dy * length

        pygame.draw.line(
            screen,
            color,
            (
                start_x,
                start_y
            ),
            (
                end_x,
                end_y
            ),
            10
        )

        px = -dy
        py = dx

        left_x = (
            end_x
            - dx * head
            + px * head
        )

        left_y = (
            end_y
            - dy * head
            + py * head
        )

        right_x = (
            end_x
            - dx * head
            - px * head
        )

        right_y = (
            end_y
            - dy * head
            - py * head
        )

        pygame.draw.line(
            screen,
            color,
            (
                end_x,
                end_y
            ),
            (
                left_x,
                left_y
            ),
            10
        )

        pygame.draw.line(
            screen,
            color,
            (
                end_x,
                end_y
            ),
            (
                right_x,
                right_y
            ),
            10
        )

    # ==================================================
    # رسم مشت
    # ==================================================

    def draw_fist(
        self,
        screen,
        rect,
        active=False
    ):

        if active:

            color = (
                255,
                255,
                255
            )

        else:

            color = (
                235,
                235,
                235
            )

        cx = rect.centerx
        cy = rect.centery

        fist_rect = pygame.Rect(
            cx - 28,
            cy - 20,
            56,
            45
        )

        pygame.draw.rect(
            screen,
            color,
            fist_rect,
            border_radius=10
        )

        for i in range(4):

            finger_rect = pygame.Rect(
                cx - 25 + i * 13,
                cy - 35,
                11,
                22
            )

            pygame.draw.rect(
                screen,
                color,
                finger_rect,
                border_radius=5
            )

        thumb_points = [
            (
                cx - 28,
                cy + 5
            ),
            (
                cx - 42,
                cy - 5
            ),
            (
                cx - 35,
                cy - 18
            ),
            (
                cx - 20,
                cy - 5
            )
        ]

        pygame.draw.polygon(
  screen,
            color,
            thumb_points
        )

    # ==================================================
    # رسم سه خط منو
    # ==================================================

    def draw_menu_icon(
        self,
        screen,
        rect
    ):

        color = (
            235,
            235,
            235
        )

        cx = rect.centerx
        cy = rect.centery

        line_width = 7
        line_length = 38
        gap = 13

        for i in range(3):

            y = (
                cy
                - gap
                + i * gap
            )

            pygame.draw.line(
                screen,
                color,
                (
                    cx - line_length // 2,
                    y
                ),
                (
                    cx + line_length // 2,
                    y
                ),
                line_width
            )

    # ==================================================
    # رسم کنترل‌ها
    # ==================================================

    def draw(self, screen):

        # ==================================================
        # وضعیت دکمه‌های اصلی
        # ==================================================

        up_active = self.is_pressed(
            self.up_rect
        )

        down_active = self.is_pressed(
            self.down_rect
        )

        left_active = self.is_pressed(
            self.left_rect
        )

        right_active = self.is_pressed(
            self.right_rect
        )

        # ==================================================
        # دکمه بالا
        # ==================================================

        self.draw_button_base(
            screen,
            self.up_rect,
            up_active
        )

        self.draw_arrow(
            screen,
            self.up_rect,
            0,
            -1,
            up_active
        )

        # ==================================================
        # دکمه پایین
        # ==================================================

        self.draw_button_base(
            screen,
            self.down_rect,
            down_active
        )

        self.draw_arrow(
            screen,
            self.down_rect,
            0,
            1,
            down_active
        )

        # ==================================================
        # دکمه چپ
        # ==================================================

        self.draw_button_base(
            screen,
            self.left_rect,
            left_active
        )

        self.draw_arrow(
            screen,
            self.left_rect,
            -1,
            0,
            left_active
        )

        # ==================================================
        # دکمه راست
        # ==================================================

        self.draw_button_base(
            screen,
            self.right_rect,
            right_active
        )

        self.draw_arrow(
            screen,
            self.right_rect,
            1,
            0,
            right_active
        )

        # ==================================================
        # آیا مورب‌های بالا باید دیده شوند؟
        # ==================================================

        forward_visible = False
        backward_visible = False

        for finger_id, revealed in self.diagonal_revealed.items():

            if not revealed:
                continue

            if finger_id not in self.fingers:
                continue

            x, y = self.fingers[
                finger_id
            ]

            # اگر این انگشت از بالا شروع شده
            # و هنوز در یکی از دکمه‌های بالا
            # یا مورب‌های بالا است
            if (
                self.up_rect.collidepoint(x, y)
                or
                self.forward_left_rect.collidepoint(
                    x,
                    y
                )
                or
                self.forward_right_rect.collidepoint(
                    x,
                    y
                )
            ):

                forward_visible = True

            # اگر از پایین شروع شده
            # و هنوز در یکی از مورب‌های پایین
            # یا دکمه پایین است
            if (
                self.down_rect.collidepoint(x, y)
                or
                self.backward_left_rect.collidepoint(
                    x,
                    y
                )
                or
                self.backward_right_rect.collidepoint(
                    x,
                    y
                )
            ):

                backward_visible = True

        # ==================================================
        # وضعیت مورب‌های موس
        # ==================================================

        if self.mouse_touching:

            x, y = self.mouse_pos

            if self.mouse_diagonal_revealed:

                if (
                    self.up_rect.collidepoint(x, y)
                    or
                    self.forward_left_rect.collidepoint(
                        x,
                        y
                    )
                    or
                    self.forward_right_rect.collidepoint(
                        x,
                        y
                    )
                ):

                    forward_visible = True

                if (
                    self.down_rect.collidepoint(x, y)
                    or
                    self.backward_left_rect.collidepoint(
                        x,
                        y
                    )
                    or
                    self.backward_right_rect.collidepoint(
                        x,
                        y
                    )
                ):

                    backward_visible = True

        # ==================================================
        # مورب‌های جلو
        # ==================================================

        if forward_visible:

            forward_left_active = self.is_pressed(
                self.forward_left_rect
            )

            forward_right_active = self.is_pressed(
                self.forward_right_rect
            )

            self.draw_button_base(
                screen,
                self.forward_left_rect,
                forward_left_active
            )

            self.draw_arrow(
                screen,
                self.forward_left_rect,
                -1,
                -1,
                forward_left_active
            )

            self.draw_button_base(
                screen,
                self.forward_right_rect,
                forward_right_active
            )

            self.draw_arrow(
                screen,
                self.forward_right_rect,
                1,
                -1,
                forward_right_active
            )

        # ==================================================
        # مورب‌های عقب
        # ==================================================

        if backward_visible:

            backward_left_active = self.is_pressed(
                self.backward_left_rect
            )

            backward_right_active = self.is_pressed(
                self.backward_right_rect
            )

            self.draw_button_base(
                screen,
                self.backward_left_rect,
                backward_left_active
            )

            self.draw_arrow(
                screen,
                self.backward_left_rect,
                -1,
                1,
                backward_left_active
            )

            self.draw_button_base(
                screen,
                self.backward_right_rect,
                backward_right_active
            )

            self.draw_arrow(
                screen,
                self.backward_right_rect,
                1,
                1,
                backward_right_active
            )

        # ==================================================
        # دکمه مشت
        # ==================================================

        attack_active = self.is_pressed(
            self.attack_rect
        )

        self.draw_button_base(
            screen,
            self.attack_rect,
            attack_active
        )

        self.draw_fist(
            screen,
            self.attack_rect,
            attack_active
        )

        # ==================================================
        # دکمه منو
        # ==================================================

        menu_active = self.is_pressed(
            self.menu_rect
        )

        self.draw_button_base(
            screen,
            self.menu_rect,
            menu_active
        )

        self.draw_menu_icon(
            screen,
            self.menu_rect
        )