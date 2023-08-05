# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Employee(metaclass=PoolMeta):
    __name__ = 'company.employee'

    roundup_user = fields.Char('Roundup User', help='The roundup username '
        'of this employee.')
