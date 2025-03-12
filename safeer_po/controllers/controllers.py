# -*- coding: utf-8 -*-
# from odoo import http


# class SafeerPo(http.Controller):
#     @http.route('/safeer_po/safeer_po/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/safeer_po/safeer_po/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('safeer_po.listing', {
#             'root': '/safeer_po/safeer_po',
#             'objects': http.request.env['safeer_po.safeer_po'].search([]),
#         })

#     @http.route('/safeer_po/safeer_po/objects/<model("safeer_po.safeer_po"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('safeer_po.object', {
#             'object': obj
#         })
