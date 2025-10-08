from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_custom_invoice_sequence = fields.Boolean(
        related="company_id.use_custom_invoice_sequence",
        string="Use Custom Invoice Sequence",
        readonly=False,
    )
    invoice_custom_sequence_id = fields.Many2one(
        "ir.sequence",
        related="company_id.invoice_custom_sequence_id",
        string="Customer Invoice Sequence",
        readonly=False,
    )
