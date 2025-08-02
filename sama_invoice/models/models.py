# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import xlwt
import io
from lxml import etree
from datetime import date, datetime, timedelta
import base64

class InvoivRes(models.Model):
    _inherit = "res.partner"

    currency_rate = fields.Float(string='Currency Rate') 



class MrpProductWizard(models.TransientModel):
    _name = 'invoice.data.wizard'

    partner_id = fields.Many2many("res.partner", string="Customer")
    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")
    currency_rate = fields.Float(string='Currency Rate')
    period = fields.Char("Period")
    average_exchange_rate  = fields.Float(string='Average Exchane Rate')

    def report_for_analytic_acount(self):
        filename = 'invoice_report.xls'
        string = 'invoice_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')

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
                     pattern: pattern solid, fore_color white; align: horiz centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre")


        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red; font: color white; align: horiz centre")
        cell_format = xlwt.easyxf()
        # filename = 'Department_level_Report_%s.xls' % date.today()

        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; align: horiz centre; font: bold 1,height 240;')
        
        

        row = 1
        col = 0

        total_credit_converted = 0
        total_debit_converted = 0
        total_sum = 0
        total_average_val = 0

        worksheet = wb.add_sheet(string)
        # worksheet.cols_right_to_left = True

        worksheet.write_merge(row , row , col , col + 5 , "Summary Invoices  Report", main_cell_total)

        row = row + 2

        worksheet.write_merge(row , row , col , col + 3 , "Period" + self.period, main_cell_total)

        row = row + 1

        worksheet.write_merge(row , row , col , col + 3 , "Date: %s " % date.today()  + self.period, main_cell_total)
   
        
        worksheet.write(row, 0, 'ت.', header_bold)

        worksheet.write(row, 1, 'القسم ', header_bold)

        worksheet.write(row, 2, 'سعر الصرف', header_bold)

        worksheet.write(row, 3, 'مجموع المبيعات ', header_bold)

        worksheet.write(row, 4, 'مجموع الكلف', header_bold)

        worksheet.write(row, 5, "الربح الكلي " , header_bold) 

        worksheet.write(row, 6, 'الكلف الحقيقية بسعر صرف', header_bold)

        row = row + 1
        for cust in  self.partner_id:
            credit_converted = 0
            debit_converted = 0
            worksheet.write(row, 0, row or '', main_cell_total)    #student 

            worksheet.write(row, 1, cust.display_name or '', main_cell_total)  #status
            worksheet.write(row, 2, cust.currency_rate or '', main_cell_total) 

            journal_items = self.env['account.move.line'].search([
                ('partner_id', '=', cust.id),
                ('credit', '>', 0),
                ('date' , '<' , self.date_end),
                ('date' , '>=' , self.date_start)
            ])
            total_credit = sum(journal_items.mapped('credit'))
            rate = cust.currency_rate or 1
            credit_converted = total_credit / rate

            total_credit_converted = total_credit_converted + credit_converted

            worksheet.write(row, 3, credit_converted or '', main_cell_total)

            journal_items = self.env['account.move.line'].search([
                ('partner_id', '=', cust.id),
                ('credit', '>', 0),
                ('date' , '<' , self.date_end),
                ('date' , '>=' , self.date_start)
            ])
            total_debit = sum(journal_items.mapped('debit'))
            rate = cust.currency_rate or 1
            debit_converted = total_debit / rate

            total_debit_converted = total_debit_converted + debit_converted

            worksheet.write(row, 4, debit_converted or '', main_cell_total)

            total_sum = total_sum + (debit_converted - credit_converted)


            worksheet.write(row, 5, debit_converted - credit_converted, main_cell_total)

            total_average_val = total_average_val + (debit_converted / self.average_exchange_rate)


            worksheet.write(row, 6, debit_converted / self.average_exchange_rate, main_cell_total)

            row = row + 1

        # row = row + 1

        worksheet.write_merge(row , row , col , col + 2 , "(total )المجموع ", main_cell_total)

        worksheet.write(row, 3, total_credit_converted, main_cell_total)
        worksheet.write(row, 4, total_debit_converted, main_cell_total)
        worksheet.write(row, 5, total_sum, main_cell_total)
        worksheet.write(row, 6, total_average_val, main_cell_total)

        row = row + 4

        worksheet.write_merge(row , row , col , col + 3 , "مجموع مبالغ الهدايا المدفوعة الى الأقسام  ", main_cell_total)
        
        row = row + 1

        worksheet.write_merge(row , row , col , col + 3 , "مجموع المصاريف بسعر صرف1420 ", main_cell_total)
        
        row = row + 1

        worksheet.write_merge(row , row , col , col + 3 , "صافي الربح الكلي بأسعار الصرف المختلفة  ", main_cell_total)
        worksheet.write(row, 4, total_sum, main_cell_total)

        row = row + 1

        worksheet.write_merge(row , row , col , col + 3 , "صافي الربح الكلي بسعر صرف1420 ", main_cell_total)
        worksheet.write(row, 4, total_credit_converted - total_average_val, main_cell_total)
        
            
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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }     






class SamaaSoSD(models.Model):
    _inherit = "sale.order"

    period = fields.Char("Period")

    section = fields.Selection([('option1','المصفى'),('option2','ام قصر')], string="Section")
    sub_section = fields.Selection([('ST','ST'),('OF','OF'),('SB','SB'),('BN','BN'),('WS','WS')], string="Sub Section")

    sequence = fields.Char("Sequence")

    # def unlink(self):
    #     for res in self:
    #         if res.sub_section:
    #             # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
    #             value = self.env['ir.config_parameter'].sudo().get_param(res.sub_section)
    #             res.sequence = res.sub_section + " - " + value +" - " + str(datetime.now().year)
    #             value = str(int(value) - 1)
    #             self.env['ir.config_parameter'].sudo().set_param(res.sub_section, value)

    #         if not res.sub_section:
    #             # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
    #             value = self.env['ir.config_parameter'].sudo().get_param("SM")
    #             res.sequence = "SM - " + value
    #             value = str(int(value) - 1)
    #             self.env['ir.config_parameter'].sudo().set_param("SM", value)
    #     return super(SamaaSoSD, self).unlink()

    # @api.model
    # def create(self, vals):
    #     res = super(SamaaSoSD, self).create(vals)

    #     if res.sub_section:
    #         # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
    #         value = self.env['ir.config_parameter'].sudo().get_param(res.sub_section)
    #         res.sequence = res.sub_section + " - " + value +" - " + str(datetime.now().year)
    #         value = str(int(value) + 1)
    #         self.env['ir.config_parameter'].sudo().set_param(res.sub_section, value)

    #     if not res.sub_section:
    #         # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
    #         value = self.env['ir.config_parameter'].sudo().get_param("SM")
    #         res.sequence = "SM - " + value
    #         value = str(int(value) + 1)
    #         self.env['ir.config_parameter'].sudo().set_param("SM", value)

    #     return res 
    

    # def action_confirm(self):
    #     res = super(SamaaSoSD, self).action_confirm()
    #     if res.invoice_count == 1:
    #         for inv in res.invoice_ids:  
    #             inv.sequence = res.sequence

    #     if res.invoice_count > 1:
    #         for inv in res.invoice_ids:  
    #             if not inv.sequence:
    #                 if res.sub_section:
    #                     # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
    #                     value = self.env['ir.config_parameter'].sudo().get_param(res.sub_section)
    #                     inv.sequence = res.sub_section + " - " + value +" - " + str(datetime.now().year)
    #                     value = str(int(value) + 1)
    #                     self.env['ir.config_parameter'].sudo().set_param(res.sub_section, value)

    #                 if not res.sub_section:
    #                     # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
    #                     value = self.env['ir.config_parameter'].sudo().get_param("SM")
    #                     inv.sequence = "SM - " + value
    #                     value = str(int(value) + 1)
    #                     self.env['ir.config_parameter'].sudo().set_param("SM", value)
    #     return res 

class SamaaSo(models.Model):
    _inherit = "account.move"

    sequence = fields.Char("Sequence")


    @api.model
    def create(self, vals):
        res = super(SamaaSo, self).create(vals)

        if res.type == "out_invoice":
            sale_order = self.env['sale.order'].search([("name","=",res.invoice_origin)])
            if sale_order.invoice_count == 1:
                res.sequence = sale_order.sequence

            if sale_order.invoice_count > 1:
                if sale_order.sub_section:
                    # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
                    value = self.env['ir.config_parameter'].sudo().get_param(sale_order.sub_section)
                    res.sequence = sale_order.sub_section + " - " + value +" - " + str(datetime.now().year)
                    value = str(int(value) + 1)
                    self.env['ir.config_parameter'].sudo().set_param(sale_order.sub_section, value)

                if not sale_order.sub_section:
                    # self.env['ir.config_parameter'].sudo().set_param('ST', '1')
                    value = self.env['ir.config_parameter'].sudo().get_param("SM")
                    res.sequence = "SM - " + value
                    value = str(int(value) + 1)
                    self.env['ir.config_parameter'].sudo().set_param("SM", value)

        return res 

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
