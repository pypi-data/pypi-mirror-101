# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool


class Configuration(ModelSingleton, ModelSQL, ModelView):
    'Roundup Configuration'
    __name__ = 'project.roundup.configuration'
    billing_product = fields.Many2One('product.product',
            'Default Billing Product', domain=[
                ('type', '=', 'service'),
                ],
            help='The product that shall be used as default billing product '
            'on new projects/tasks.')
    default_invoice_method = fields.Selection('get_invoice_options',
        'Default Invoice Method',
        help='The Invoice Method used when creating new projects '
        'or tasks from Roundup.')
    default_project_prefix = fields.Char('Default Project Prefix',
        help='The prefix to use for automatically created projects '
        'or tasks by Roundup.')

    @classmethod
    def get_invoice_options(cls):
        Work = Pool().get('project.work')
        field_name = 'project_invoice_method'
        selection = Work.fields_get(
            [field_name])[field_name]['selection']
        selection.insert(0, ('', ''))
        return selection

    @staticmethod
    def default_default_invoice_method():
        return 'manual'

    @staticmethod
    def default_default_project_prefix():
        return 'Roundup:'
