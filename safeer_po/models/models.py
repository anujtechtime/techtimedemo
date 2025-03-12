# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import io
import json
import base64
import xlwt
from datetime import date, datetime, timedelta

class safeer_po(models.Model):
    _inherit = "purchase.order"

    requested_costumer = fields.Many2one("res.partner",string="Requested Customer")

    def action_view_invoice(self):
        lines = super(safeer_po, self).action_view_invoice()
        # for order in self:
            # invoices = order.mapped('order_line.invoice_lines.move_id')
        print("invoices@@@@@@@@@@@@@@@",self.invoice_ids)
        for bil in self.invoice_ids:
            bil.requested_costumer = self.requested_costumer.id
            # order.invoice_ids = invoices
            # order.invoice_count = len(invoices)
        return lines    

class SafeerSP(models.Model):
    _inherit = "stock.picking"

    custumer_po_number = fields.Char(string="Customer PO")

class ProfitCustomerWizard(models.TransientModel):
    _name = 'customer.profit.wizard'

    
    requested_costumer = fields.Many2many("res.partner",string="Customer")
    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")

    def action_done(self):
        print("@@@@@@@@@@@@@@",self)
        filename = 'profit_report.xls'
        string = 'profit_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string, cell_overwrite_ok=True)
        # worksheet.cols_right_to_left = True
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        # worksheet.col(0).width = 10000
        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 5000

        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25; align: horiz centre; font: bold 1,height 240;")


        header_bold_main_header = xlwt.easyxf("font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; align: horiz centre; align: vert centre")


        
        main_cell_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre; align: vert centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre; align: vert centre")
        tttyl = xlwt.easyxf("align: horiz centre; align: vert centre")

        row = 0
        col = 0
        count = 1
        
        worksheet.write(row, 0, 'Invoice Number', header_bold) #sequence
        worksheet.write(row, 1, 'Invoice Date', header_bold) #sequence
        worksheet.write(row, 2, 'Customer', header_bold) #sequence
        worksheet.write(row, 3, 'Sale Price (Invoice Amount)', header_bold) #sequence
        worksheet.write(row, 4, 'Purchase Price(Bill Amount)', header_bold) #sequence
        worksheet.write(row, 5, 'Profit (Sale - Purchase)', header_bold) #sequence

        row = 1
        invoice_amount_total = 0
        invoice_bill_total = 0
        symbol = ""
        sale_ord = self.env["sale.order"].search([("partner_id","in",self.requested_costumer.mapped('id')),("date_order",">=",self.date_start),("date_order","<=",self.date_end)])
        for sl_in in sale_ord:
            for inv in sl_in.invoice_ids:
                if inv.state == "posted":
                    worksheet.write(row, col, inv.display_name, border_normal) #sequence
                    worksheet.write(row, col + 1, inv.invoice_date.strftime('%m/%d/%Y'), border_normal) #sequence
                    worksheet.write(row, col + 2, inv.partner_id.display_name, border_normal) #sequence
                    invoice_amount = sum(x.debit for x in inv.line_ids)

                    worksheet.write(row, col + 3, sl_in.company_id.currency_id.symbol + str(invoice_amount), border_normal) #sequence 

                    symbol = sl_in.company_id.currency_id.symbol

                    invoice_amount_total = invoice_amount_total + invoice_amount

                    purchase = self.env["purchase.order"].search([("sale_order_id","=",sl_in.id)])
                    bill_total = 0
                    for pur in purchase:
                        for bi in pur.invoice_ids:
                            bill_total = bill_total + bi.amount_total

                    worksheet.write(row, col + 4, sl_in.company_id.currency_id.symbol + str(bill_total), border_normal) #sequence

                    invoice_bill_total = invoice_bill_total + bill_total

                    worksheet.write(row, col + 5, sl_in.company_id.currency_id.symbol + str( float(invoice_amount) - float(bill_total) ), border_normal) #sequence
                            
                    row = row + 1

        row = row + 1
        worksheet.write(row, 0, "Total", header_bold) #sequence

        worksheet.write(row, 3, symbol + str(invoice_amount_total), header_bold) #sequence
        worksheet.write(row, 4, symbol + str(invoice_bill_total), header_bold) #sequence
        worksheet.write(row, 5, symbol + str(float(invoice_amount_total) - float(invoice_bill_total)) , header_bold) #sequence   

        fp = io.BytesIO()
        print("fp@@@@@@@@@@@@@@@@@@",fp)
        wb.save(fp)
        print(wb)
        out = base64.encodebytes(fp.getvalue())
        attachment = {
                       'name': str(filename),
                       'display_name': str(filename),
                       'datas': out,
                       'type': 'binary'
                   }
        ir_id = self.env['ir.attachment'].create(attachment) 
        print("ir_id@@@@@@@@@@@@@@@@",ir_id)

        xlDecoded = base64.b64decode(out)

        # file_added = "/home/anuj/Desktop/workspace13/Student_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

class SafeerSo(models.Model):
    _inherit = "sale.order"

    custumer_po_number = fields.Char(string="Customer PO")

    custumer_req_number = fields.Char(string="Customer RFQ")


    def action_confirm(self):
        lines = super(SafeerSo, self).action_confirm()
        print("lines@@@@@@@@@@@@@@@@",lines)
        for dev in self.picking_ids:
            dev.custumer_po_number = self.custumer_po_number
        return lines

class SafeerInvoice(models.Model):
    _inherit = "account.move"

    custumer_po_number = fields.Char(string="Customer PO")  
    requested_costumer = fields.Many2one("res.partner",string="Requested Customer")      

class SaleAdvancePaymentInvSafeer(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        lines = super(SaleAdvancePaymentInvSafeer, self).create_invoices()
        # self.env['account.move'].search([('invoice_origin','=',)])
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for sale_name in sale_orders:
            inv = self.env['account.move'].search([('invoice_origin','=',sale_name.name)])
            for invt in inv:
                invt.custumer_po_number = sale_name.custumer_po_number
        return lines
#     _name = 'safeer_po.safeer_po'
#     _description = 'safeer_po.safeer_po'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
