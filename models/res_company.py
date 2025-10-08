from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    use_custom_invoice_sequence = fields.Boolean(
        string="Use Custom Invoice Sequence",
        help="When enabled, customer invoices use the configured custom sequence instead of"
             " the journal sequence.",
    )
    invoice_custom_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Customer Invoice Sequence",
        help="Sequence applied to customer invoices when the custom sequence option is enabled.",
        copy=False,
    )
