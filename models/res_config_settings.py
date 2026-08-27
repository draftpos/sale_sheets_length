from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_sheets_length = fields.Boolean(
        related='company_id.allow_sheets_length',
        readonly=False,
        string="Allow Sheets and Length"
    )



