from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sheets = fields.Float(string='Sheets', default=1.0)
    length = fields.Float(string='Length', default=1.0)
    allow_sheets_length = fields.Boolean(related='order_id.allow_sheets_length')

    @api.onchange('sheets', 'length')
    def _onchange_sheets_length(self):
        for line in self:
            if line.sheets and line.length:
                line.product_uom_qty = line.sheets * line.length
