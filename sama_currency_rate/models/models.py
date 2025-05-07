# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SamaCurrencyRate(models.Model):

    _inherit = "sale.order.line"

    currency_rate1 = fields.Float("Currency Rate")

    @api.model
    def create(self, vals):
        res = super(SamaCurrencyRate, self).create(vals)

        print("res.price_unit@@@@@@@@@@@@@@@2222222222222",res.order_id)
        
        print("vals@@@@@@222222222444444444444",vals)

        print("res.currency_rate########################",res.currency_rate1)

        if res.price_unit > 0:
            print("VBBBBBBBBBBBBBBBBBBBBB",float(res.currency_rate1) * float(res.price_unit))
            res.price_unit = res.currency_rate1 * res.price_unit
            print("VVVVVVVVVVVVVVVVVVVV",res.price_subtotal)
        return res
#     _name = 'sama_currency_rate.sama_currency_rate'
#     _description = 'sama_currency_rate.sama_currency_rate'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
