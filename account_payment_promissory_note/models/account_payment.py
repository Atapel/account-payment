# Copyright 2018 Sergio Teruel <sergio.teruel@tecnativa.com>
# Copyright 2018 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    promissory_note = fields.Boolean(
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    date_due = fields.Date(
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    def _get_liquidity_move_line_vals(self, amount):
        res = super()._get_liquidity_move_line_vals(amount)
        if self.promissory_note:
            res['date_maturity'] = self.date_due
        return res

    @api.onchange('promissory_note')
    def _onchange_promissory_note(self):
        super()._onchange_promissory_note()
        if not self.date_due and self.promissory_note:
            invoices = False
            if self._name == 'account.payment':
                invoices = self.invoice_ids
            if invoices:
                self.date_due = max(invoices.mapped('date_due'))
