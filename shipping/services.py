from decimal import Decimal
from itertools import permutations

from .models import Box


def get_product_volume(product):
    return product.length * product.width * product.height


def get_box_volume(box):
    return box.inner_length * box.inner_width * box.inner_height


def dimensions_fit(product_dimensions, box_dimensions):
    """Check simple rotation fit for one product inside one box."""
    for rotated_dimensions in permutations(product_dimensions):
        if all(
            item <= box
            for item, box in zip(rotated_dimensions, box_dimensions)
        ):
            return True
    return False


def recommend_box_for_order(order):
    items = order.items.select_related('product').all()

    if not items:
        return None

    total_weight = Decimal('0')
    total_product_volume = Decimal('0')
    product_dimensions_list = []

    for item in items:
        product = item.product
        total_weight += product.weight * item.quantity
        total_product_volume += get_product_volume(product) * item.quantity

        product_dimensions_list.append(
            (product.length, product.width, product.height),
        )

    suitable_boxes = []

    for box in Box.objects.filter(is_active=True):
        box_dimensions = (box.inner_length, box.inner_width, box.inner_height)

        if total_weight > box.max_weight:
            continue

        if total_product_volume > get_box_volume(box):
            continue

        if not all(
            dimensions_fit(product_dimensions, box_dimensions)
            for product_dimensions in product_dimensions_list
        ):
            continue

        suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    best_box = sorted(
        suitable_boxes,
        key=lambda box: (box.cost, get_box_volume(box)),
    )[0]

    return {
        'box': best_box,
        'total_weight': total_weight,
        'total_product_volume': total_product_volume,
    }
