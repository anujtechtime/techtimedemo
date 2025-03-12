# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            sale_order = self.sale_order_id

            # Copy the customer info
            # self.partner_id = sale_order.partner_id
            # self.date_order = sale_order.confirmation_date
            self.currency_id = sale_order.currency_id

            # Clear existing lines and add new lines from the Sale Order
            new_order_lines = []
            for line in sale_order.order_line:
                new_order_line = (0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'name': line.name,
                    'product_uom': line.product_uom.id,
                    'date_planned': fields.Datetime.now(),  # Assuming immediate delivery for simplicity
                })
                new_order_lines.append(new_order_line)

            self.order_line = new_order_lines


class SalerefOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    number_inv = fields.Integer("Number INV")

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            sale_order = self.sale_order_id

            # Copy the customer info
            # self.partner_id = sale_order.partner_id
            # self.date_order = sale_order.confirmation_date
            self.currency_id = sale_order.currency_id

            # Clear existing lines and add new lines from the Sale Order
            new_order_lines = []
            for line in sale_order.order_line:
                new_order_line = (0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_qty,
                    'price_unit': line.price_unit,
                    'name': line.name,
                    'product_uom': line.product_uom.id,
                })
                new_order_lines.append(new_order_line)

            self.order_line = new_order_lines            
