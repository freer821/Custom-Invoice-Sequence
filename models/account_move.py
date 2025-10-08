from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _set_next_sequence(self):
        custom_moves = self.filtered(lambda move: move._needs_custom_invoice_sequence())
        other_moves = self - custom_moves
        
        for move in custom_moves:
            sequence = move.company_id.invoice_custom_sequence_id
            sequence_date = move.invoice_date or move.date or fields.Date.context_today(move)
            move.name = sequence.with_context(ir_sequence_date=sequence_date).next_by_id()
        
        if other_moves:
            super(AccountMove, other_moves)._set_next_sequence()

    def _needs_custom_invoice_sequence(self):
        self.ensure_one()
        return (
            self.move_type in ("out_invoice", "out_refund")
            and self.company_id.use_custom_invoice_sequence
            and self.company_id.invoice_custom_sequence_id
            and (not self.name or self.name == "/")
        )
