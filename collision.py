import pygame


# نگه داشتن بازیکن یا دشمن داخل محدوده اتاق
def keep_inside_room(entity, room_rect):

    rect = entity.get_rect()

    # دیوار چپ
    if rect.left < room_rect.left:
        entity.x = room_rect.left

    # دیوار راست
    if rect.right > room_rect.right:
        entity.x = room_rect.right - entity.width

    # دیوار بالا
    if rect.top < room_rect.top:
        entity.y = room_rect.top

    # دیوار پایین
    if rect.bottom > room_rect.bottom:
        entity.y = room_rect.bottom - entity.height


# جلوگیری از رد شدن بازیکن و دشمن از داخل هم
def separate_entities(a, b, room_rect):

    rect_a = a.get_rect()
    rect_b = b.get_rect()

    # اگر اصلاً برخوردی ندارند، کاری نکن
    if not rect_a.colliderect(rect_b):
        return

    # مقدار هم‌پوشانی در محور افقی
    overlap_x = min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left)

    # مقدار هم‌پوشانی در محور عمودی
    overlap_y = min(rect_a.bottom, rect_b.bottom) - max(rect_a.top, rect_b.top)

    if overlap_x <= 0 or overlap_y <= 0:
        return

    # از سمتی که فاصله کمتری دارد جدا می‌کنیم
    if overlap_x < overlap_y:

        push = overlap_x / 2

        if rect_a.centerx < rect_b.centerx:
            a.x -= push
            b.x += push
        else:
            a.x += push
            b.x -= push

    else:

        push = overlap_y / 2

        if rect_a.centery < rect_b.centery:
            a.y -= push
            b.y += push
        else:
            a.y += push
            b.y -= push

    # بعد از جدا کردن، مطمئن شو هیچ‌کدام از اتاق خارج نشده‌اند
    keep_inside_room(a, room_rect)
    keep_inside_room(b, room_rect)