#!/usr/bin/env python
from decimal import Decimal

print 'Mat Cutting Guide for Pictures'
print
print '8" = 203.2mm'
print '10" = 254mm'
print
print 'Default values are in mm'
print

def get_decimal(prompt, default=None):
    if default:
        result = raw_input('%s (default %s):' % (prompt, str(default)))
    else:
        result = raw_input(prompt + ': ')
    if (not result) and default:
        return Decimal(default)
    try:
        return Decimal(result)
    except Exception:
        print 'Cannot convert to number, please try again'
        return get_decimal(prompt, default)


x_mat = get_decimal('Horizonal mat size')
y_mat = get_decimal('Vertical mat size')
x_image = get_decimal('Horizonal image size')
y_image = get_decimal('Vertical image size')
horizontal_overlap = get_decimal('Horizontal overlap', 3)
vertical_overlap = get_decimal('Vertical overlap', horizontal_overlap)
vertical_offset = get_decimal('Vertical offset', 10)
second_mat = get_decimal('Second mat spacing', 10)
second_mat_bottom_multiplier = get_decimal('Second mat bottom multiplier', Decimal(1.5))

x_border = (x_mat - x_image)/2 + horizontal_overlap
y_border = (y_mat - y_image)/2 + vertical_overlap

print
print '-- Picture Window --'
print 'Side borders: %.2f' % x_border
print 'Top border: %.2f' % (y_border - vertical_offset/2)
print 'Bottom border: %.2f' % (y_border + vertical_offset/2)
print
print '-- Second Mat --'
print 'Side borders: %.2f' % (x_border - second_mat)
print 'Top border: %.2f' % (y_border - vertical_offset/2 - second_mat)
print 'Bottom border: %.2f' % (y_border + vertical_offset/2 - second_mat*second_mat_bottom_multiplier)
