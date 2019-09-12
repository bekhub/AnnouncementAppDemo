from django import template

register = template.Library()


def currency(value, name='сом'):
    if value == 0:
        return 'Цена договорная'
    else:
        return '%1.2f %s' % (value, name)


register.filter('currency', currency)
