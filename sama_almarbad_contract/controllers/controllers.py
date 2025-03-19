# -*- coding: utf-8 -*-
# from odoo import http


# class SamaAlmarbadContract(http.Controller):
#     @http.route('/sama_almarbad_contract/sama_almarbad_contract/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sama_almarbad_contract/sama_almarbad_contract/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sama_almarbad_contract.listing', {
#             'root': '/sama_almarbad_contract/sama_almarbad_contract',
#             'objects': http.request.env['sama_almarbad_contract.sama_almarbad_contract'].search([]),
#         })

#     @http.route('/sama_almarbad_contract/sama_almarbad_contract/objects/<model("sama_almarbad_contract.sama_almarbad_contract"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sama_almarbad_contract.object', {
#             'object': obj
#         })
