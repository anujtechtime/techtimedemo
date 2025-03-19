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
        ('contract', 'عقد'),
        ('payment', 'صرف')], string='Contract/Tender',
        copy=False, default='invitation', tracking=True,
        help="* Choose The one among Contract and Tender")
