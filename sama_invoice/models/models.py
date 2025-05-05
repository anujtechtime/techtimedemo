# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class SamaaSoSD(models.Model):
    _inherit = "sale.order"

    section = fields.Selection([('option1','المصفى'),('option2','ام قصر')], string="Section")
    sub_section = fields.Selection([('ST','ST'),('OF','OF'),('SB','SB'),('BN','BN'),('WS','WS')], string="Sub Section")

    sequence = fields.Char("Sequence")

    @api.model
    def create(self, vals):
        res = super(SamaaSoSD, self).create(vals)

        if res.sub_section:
            # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
            value = self.env['ir.config_parameter'].sudo().get_param(res.sub_section)
            res.sequence = res.sub_section + " - " + value +" - " + str(datetime.now().year)
            value = str(int(value) + 1)
            self.env['ir.config_parameter'].sudo().set_param(res.sub_section, value)

        if not res.sub_section:
            # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
            value = self.env['ir.config_parameter'].sudo().get_param("SM")
            res.sequence = "SM - " + value
            value = str(int(value) + 1)
            self.env['ir.config_parameter'].sudo().set_param("SM", value)

        return res 
    

    @api.onchange('invoice_count')
    def _onchange_invoice_count(self):
        res = super(SamaaSoSD, self).action_confirm()
        if res.invoice_count == 1:
            for inv in res.invoice_ids:  
                inv.sequence = res.sequence

        if res.invoice_count > 1:
            for inv in res.invoice_ids:  
                if not inv.sequence:
                    if res.sub_section:
                        # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
                        value = self.env['ir.config_parameter'].sudo().get_param(res.sub_section)
                        inv.sequence = res.sub_section + " - " + value +" - " + str(datetime.now().year)
                        value = str(int(value) + 1)
                        self.env['ir.config_parameter'].sudo().set_param(res.sub_section, value)

                    if not res.sub_section:
                        # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
                        value = self.env['ir.config_parameter'].sudo().get_param("SM")
                        inv.sequence = "SM - " + value
                        value = str(int(value) + 1)
                        self.env['ir.config_parameter'].sudo().set_param("SM", value)
        return res 

class SamaaSo(models.Model):
    _inherit = "account.move"

    sequence = fields.Char("Sequence")

class StockMoveInh(models.Model):
    _inherit = 'stock.move'

    sale_price_unit = fields.Float(string='Sale Price Unit')


class SaleOrderLineIn(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_stock_moves(self, picking):
        res = super(SaleOrderLineIn, self)._prepare_stock_moves(picking)
        for move in res:
            move['sale_price_unit'] = self.price_unit
        return res

# class sama_invoice(models.Model):
#     _name = 'sama_invoice.sama_invoice'
#     _description = 'sama_invoice.sama_invoice'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
