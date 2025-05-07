# -*- coding: utf-8 -*-
# from odoo import http


# class SamaCurrencyRate(http.Controller):
#     @http.route('/sama_currency_rate/sama_currency_rate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sama_currency_rate/sama_currency_rate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sama_currency_rate.listing', {
#             'root': '/sama_currency_rate/sama_currency_rate',
#             'objects': http.request.env['sama_currency_rate.sama_currency_rate'].search([]),
#         })

#     @http.route('/sama_currency_rate/sama_currency_rate/objects/<model("sama_currency_rate.sama_currency_rate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sama_currency_rate.object', {
#             'object': obj
#         })
