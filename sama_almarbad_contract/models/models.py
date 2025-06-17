# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sama_almarbad_contract(models.Model):
    _name = 'contract.tender'
    _description = 'Contract/Tender'

    contract_tender = fields.Selection([
        ('contract', 'Contract'),
        ('tender', 'Tender')], string='Contract/Tender',
        copy=False, default='contract', tracking=True,
        help="* Choose The one among Contract and Tender")
    
    state = fields.Selection([
        ('invitation', 'دعوة'),
        ('bid', 'عطاء'),
        ('referral','الإحالة'),
        ('contract', 'عقد'),
        ('payment', 'صرف')], string='Contract/Tender',
        copy=False, default='invitation', tracking=True,
        help="* Choose The one among Contract and Tender")
    
    name = fields.Char("Name")
    number = fields.Integer("Number") 
    date = fields.Date("Date") 
    estimated_cost = fields.Float("Estimated Cost")

    proposed_cost = fields.Float("Proposed Cost")

    contract_number = fields.Char("Contract Number")
    approved_cost  = fields.Float("Estimated Cost")



    received_payment  =fields.Float("Received Payment")

    remaining_amount  = fields.Float("Remaining Amount")


    state_tender = fields.Selection([
        ('tender', 'مناقصة'),
        ('bid', 'عطاء'),
        ('referral','الإحالة'),
        ('contract', 'عقد'),
        ('payment', 'صرف')], string='Contract/Tender',
        copy=False, default='tender', tracking=True,
        help="* Choose The one among Contract and Tender")
    

    currency_id = fields.Many2one('res.currency', string="Currency")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", required=True)
    is_posted = fields.Boolean(string="Is Posted", default=False)

    @api.model
    def _get_default_journal(self, type):
        journal_map = {
            'received': 181,  # Receivable Journal
            'payable': 491,   # Payable Journal
        }
        return self.env['account.journal'].browse(journal_map[type])

    def action_post_entries(self):
        for record in self:
            if not record.analytic_account_id or not record.approved_cost or not record.received_payment:
                raise UserError(_("All required fields must be filled before posting."))

            move_vals = []

            # Entry 1: Approved Cost
            move_vals.append({
                'journal_id': self._get_default_journal('payable').id,
                'line_ids': [
                    (0, 0, {
                        'account_id': 359,
                        'name': 'Approved Value',
                        'debit': record.approved_cost,
                        'analytic_account_id': record.analytic_account_id.id,
                    }),
                    (0, 0, {
                        'account_id': 354,
                        'name': 'Approved Value',
                        'credit': record.approved_cost,
                    }),
                ],
                'currency_id': record.currency_id.id,
            })

            # Entry 2: Received Payment
            move_vals.append({
                'journal_id': self._get_default_journal('received').id,
                'line_ids': [
                    (0, 0, {
                        'account_id': 34,
                        'name': 'Received Payment',
                        'debit': record.received_payment,
                        'analytic_account_id': record.analytic_account_id.id,
                    }),
                    (0, 0, {
                        'account_id': 359,
                        'name': 'Received Payment',
                        'credit': record.received_payment,
                    }),
                ],
                'currency_id': record.currency_id.id,
            })

            for vals in move_vals:
                self.env['account.move'].create(vals).post()

            record.is_posted = True


    def action_bit(self):
        self.state = 'bid'

    def action_contract(self):
        self.state = 'contract'
        
    def action_payment(self):
        self.state = 'payment'

    def action_referral(self):
        self.state = 'referral'    

        