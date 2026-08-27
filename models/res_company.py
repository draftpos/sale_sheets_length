from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    allow_sheets_length = fields.Boolean(string="Allow Sheets and Length")
