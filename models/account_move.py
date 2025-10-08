from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            if move._needs_custom_invoice_sequence():
                sequence = move.company_id.invoice_custom_sequence_id
                sequence_date = move.invoice_date or move.date or fields.Date.context_today(move)
                move.name = sequence.with_context(ir_sequence_date=sequence_date).next_by_id()
        return moves

    def _needs_custom_invoice_sequence(self):
        self.ensure_one()
        return (
            self.move_type in ("out_invoice", "out_refund")
            and self.company_id.use_custom_invoice_sequence
            and self.company_id.invoice_custom_sequence_id
            and (not self.name or self.name == "/")
        )
