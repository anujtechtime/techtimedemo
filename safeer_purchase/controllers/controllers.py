# -*- coding: utf-8 -*-
# from odoo import http


# class SafeerPurchase(http.Controller):
#     @http.route('/safeer_purchase/safeer_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/safeer_purchase/safeer_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('safeer_purchase.listing', {
#             'root': '/safeer_purchase/safeer_purchase',
#             'objects': http.request.env['safeer_purchase.safeer_purchase'].search([]),
#         })

#     @http.route('/safeer_purchase/safeer_purchase/objects/<model("safeer_purchase.safeer_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('safeer_purchase.object', {
#             'object': obj
#         })
