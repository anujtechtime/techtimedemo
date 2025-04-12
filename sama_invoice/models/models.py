# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class SamaaSo(models.Model):
    _inherit = "account.move"

    section = fields.Selection([('option1','المصفى'),('option2','ام قصر')], string="Sectiomn")
    sub_section = fields.Selection([('ST','ST'),('OF','OF'),('SB','SB'),('BN','BN'),('WS','WS')], string="Sub Sectiomn")

    sequence = fields.Char("Sequence")

    @api.model
    def create(self, vals):
        res = super(SamaaSo, self).create(vals)

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
