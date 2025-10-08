import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info("=== Custom Invoice Sequence: create called ===")
        moves = super().create(vals_list)
        for move in moves:
            _logger.info(f"Move: {move.name}, Type: {move.move_type}")
            _logger.info(f"Use custom: {move.company_id.use_custom_invoice_sequence}")
            _logger.info(f"Sequence ID: {move.company_id.invoice_custom_sequence_id}")
            _logger.info(f"Current name: '{move.name}'")
            
            if move._needs_custom_invoice_sequence():
                _logger.info("=== Applying custom sequence ===")
                sequence = move.company_id.invoice_custom_sequence_id
                sequence_date = move.invoice_date or move.date or fields.Date.context_today(move)
                move.name = sequence.with_context(ir_sequence_date=sequence_date).next_by_id()
                _logger.info(f"New name: {move.name}")
            else:
                _logger.info("=== NOT applying custom sequence ===")
        return moves

    def _needs_custom_invoice_sequence(self):
        self.ensure_one()
        return (
            self.move_type in ("out_invoice", "out_refund")
            and self.company_id.use_custom_invoice_sequence
            and self.company_id.invoice_custom_sequence_id
            and (not self.name or self.name == "/")
        )
