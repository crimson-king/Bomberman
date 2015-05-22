import math

from pybomberman.objects import GameObject
from pybomberman.shapes import Shape, Rectangle


def raise_not_impl(shape: Shape, other: Shape):
    raise NotImplementedError(
        'collision for {} not implemented'.format((shape, other)))


def collides_rect(rect: Rectangle, other: Rectangle):
    return rect.x < other.x + other.width \
           and rect.x + rect.width > other.x \
           and rect.y < other.y + other.height \
           and rect.y + rect.height > other.y


def collides(obj: GameObject, other: GameObject, resolve: bool=False) -> bool:
    """
    :param resolve: If True, collision will ve resolved if exists on obj.
    :returns bool: True if objects collide, False elsewhere.
    """
    if isinstance(obj.shape, Rectangle):
        if isinstance(other.shape, Rectangle):
            obj.shape.position += obj.position
            other.shape.position += other.position

            result = collides_rect(obj.shape, other.shape)

            if result and resolve:
                resolve_collision_rect(obj, other)

            obj.shape.position -= obj.position
            other.shape.position -= other.position

            obj.position.x += obj.shape.position.x
            obj.position.y += obj.shape.position.y

            obj.shape.position.x = 0
            obj.shape.position.y = 0

            return result
        else:
            raise_not_impl(obj.shape, other.shape)
    else:
        raise_not_impl(obj.shape, other.shape)


def resolve_collision_rect(obj: GameObject, other: GameObject):
    obj_center_x = obj.shape.x + obj.shape.width * .5
    obj_center_y = obj.shape.y + obj.shape.height * .5

    other_center_x = other.shape.x + other.shape.width * .5
    other_center_y = other.shape.y + other.shape.height * .5

    dx = (obj_center_x - other_center_x) / (other.shape.width * .5)
    dy = (obj_center_y - other_center_y) / (other.shape.height * .5)

    adx, ady = math.fabs(dx), math.fabs(dy)

    if math.fabs(adx - ady) < .1:
        if dx < 0:
            obj.shape.x = other.shape.x - obj.shape.width
        else:
            obj.shape.x = other.shape.x + other.shape.width

        if dy > 0:
            obj.shape.y = other.shape.y + other.shape.height
        else:
            obj.shape.y = other.shape.y - obj.shape.height
    elif adx > ady:
        if dx < 0:
            obj.shape.x = other.shape.x - obj.shape.width
        else:
            obj.shape.x = other.shape.x + other.shape.width
    else:
        if dy > 0:
            obj.shape.y = other.shape.y + other.shape.height
        else:
            obj.shape.y = other.shape.y - obj.shape.height
