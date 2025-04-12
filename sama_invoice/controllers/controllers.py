# -*- coding: utf-8 -*-
# from odoo import http


# class SamaInvoice(http.Controller):
#     @http.route('/sama_invoice/sama_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sama_invoice/sama_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sama_invoice.listing', {
#             'root': '/sama_invoice/sama_invoice',
#             'objects': http.request.env['sama_invoice.sama_invoice'].search([]),
#         })

#     @http.route('/sama_invoice/sama_invoice/objects/<model("sama_invoice.sama_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sama_invoice.object', {
#             'object': obj
#         })
