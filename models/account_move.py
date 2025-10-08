from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _set_next_sequence(self):
        custom_moves = self.filtered(lambda move: move._needs_custom_invoice_sequence())
        other_moves = self - custom_moves
        if other_moves:
            # Use the standard journal sequence for moves that do not opt into the custom logic.
            super(AccountMove, other_moves)._set_next_sequence()

        for move in custom_moves:
            sequence = move.company_id.invoice_custom_sequence_id
            if not sequence:
                # Fallback to standard sequence if custom sequence is not set
                super(AccountMove, move)._set_next_sequence()
                continue
            sequence_date = move.invoice_date or move.date or fields.Date.context_today(move)
            move.name = sequence.with_context(ir_sequence_date=sequence_date).next_by_id()

    def _needs_custom_invoice_sequence(self):
        self.ensure_one()
        if self.move_type not in ("out_invoice", "out_refund"):
            return False
        if not self.company_id.use_custom_invoice_sequence:
            return False
        if not self.company_id.invoice_custom_sequence_id:
            return False
        return not self.name or self.name in {"/", ""}
