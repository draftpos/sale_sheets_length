from odoo import api, fields, models
from lxml import etree

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allow_sheets_length = fields.Boolean(related='company_id.allow_sheets_length')

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            doc = arch
            
            # 1. Inject allow_sheets_length into the main form so parent.allow_sheets_length is available
            for order_line_node in doc.xpath("//field[@name='order_line']"):
                allow_field = etree.Element("field", name="allow_sheets_length", invisible="1")
                order_line_node.addprevious(allow_field)
            
            # 2. Inject sheets and length into the list view of order_line using parent.allow_sheets_length
            for node in doc.xpath("//field[@name='order_line']//list//field[@name='product_uom_qty']"):
                sheets = etree.Element("field", name="sheets", optional="show")
                sheets.set("column_invisible", "not parent.allow_sheets_length")
                length = etree.Element("field", name="length", optional="show")
                length.set("column_invisible", "not parent.allow_sheets_length")
                node.addprevious(length)
                node.addprevious(sheets)
                
                # Make Qty readonly if allow_sheets_length is checked
                old_readonly = node.get("readonly")
                if old_readonly and old_readonly not in ['0', 'False', '']:
                    if old_readonly not in ['1', 'True']:
                        node.set("readonly", f"({old_readonly}) or parent.allow_sheets_length")
                else:
                    node.set("readonly", "parent.allow_sheets_length")
                node.set("force_save", "1")
                
            # 3. Inject sheets and length into the form view of order_line
            for node in doc.xpath("//field[@name='order_line']//form//field[@name='product_uom_qty']"):
                sheets = etree.Element("field", name="sheets")
                sheets.set("invisible", "not parent.allow_sheets_length")
                length = etree.Element("field", name="length")
                length.set("invisible", "not parent.allow_sheets_length")
                node.addprevious(length)
                node.addprevious(sheets)
                
                # Make Qty readonly if allow_sheets_length is checked
                old_readonly = node.get("readonly")
                if old_readonly and old_readonly not in ['0', 'False', '']:
                    if old_readonly not in ['1', 'True']:
                        node.set("readonly", f"({old_readonly}) or parent.allow_sheets_length")
                else:
                    node.set("readonly", "parent.allow_sheets_length")
                node.set("force_save", "1")
                
        return arch, view
