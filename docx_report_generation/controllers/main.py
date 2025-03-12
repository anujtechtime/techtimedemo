from json import dumps as json_dumps, loads as json_loads
from werkzeug.urls import url_decode

from odoo.http import (
    content_disposition,
    request,
    route,
    serialize_exception as _serialize_exception,
)
import time
import os

import base64


from logging import getLogger
from odoo.tools import html_escape
from odoo.tools.safe_eval import safe_eval

from odoo.addons.web.controllers.main import ReportController

_logger = getLogger(__name__)

class DocxReportController(ReportController):
    @route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        """
        Запускает генерацию файла отчета и возвращает его
        """
        if converter == "pdf":
            return super(DocxReportController, self).report_routes(
                reportname=reportname, docids=docids, converter=converter, **data
            )
        report = request.env["ir.actions.report"]._get_report_from_name(reportname)
        context = dict(request.env.context)
        _data = dict()
        if docids and converter == "docx":
            _docids = [int(i) for i in docids.split(",")]
        if docids and converter == "xlsx":
            _docids = docids    
        if data.get("options"):
            _data.update(json_loads(data.pop("options")))
        if data.get("context"):
            # Ignore 'lang' here, because the context in data is the one from the webclient *but* if
            # the user explicitely wants to change the lang, this mechanism overwrites it.
            _data["context"] = json_loads(data["context"])
            if _data["context"].get("lang") and not _data.get("force_context_lang"):
                del _data["context"]["lang"]
            context.update(_data["context"])
        if converter == "xlsx":
            print("EEEEEEEEEEEEEE",converter)
            docx = report.with_context(context)._render_docx_xlsx(_docids, data=_data)
            file_bytes = docx[0]

            file_path = os.path.join('/tmp', "output.xlsx")
            with open(file_path, 'wb') as file:
                file.write(file_bytes)

            response = request.make_response(file_bytes, [
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml'),
            ])
            return response    


            # docxhttpheaders = [
            #     (
            #         "Content-Type",
            #         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml",
            #     ),
            # ]
            # return request.make_response(docx, headers=docxhttpheaders)
        elif converter == "docx":
            docx = report.with_context(context)._render_docx_docx(_docids, data=_data)
            docxhttpheaders = [
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
            ]
            return request.make_response(docx, headers=docxhttpheaders)    
        elif converter == "pdf" and "docx" in report.report_type:
            pdf = report.with_context(context)._render_docx_pdf(_docids, data=_data)
            pdfhttpheaders = [
                (
                    "Content-Type",
                    "application/pdf",
                ),
                ("Content-Length", len(pdf[0])),
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return super().report_routes(
                reportname, docids=docids, converter=converter, **data
            )

    @route()
    def report_download(self, data, token, context=None):
        print("3333333333333333333333333333333")
        """
        Обрабатывает запрос на скачивание файла отчета
        """
        requestcontent = json_loads(data)
        url, type = requestcontent[0], requestcontent[1]
        print("type@@@@@@@@@@@@@@@@@@@",type)
        if type not in ["docx-docx", "docx-pdf","xlsx-xlxs", "pdf-pdf"]:
            return super(DocxReportController, self).report_download(data, token, context)
        try:
            print("type@@@@@@@@@@@@@@@@@@@22222222222",type)
            if type in ["docx-docx", "docx-pdf", "xlsx-xlxs", "pdf-pdf"]:
                if type == "xlsx-xlxs":
                    converter = "xlsx"
                    extension = "xlsx"
                    pattern = "/report/%s/" % ("xlsx")
                    print("url@@@@@@@@@@@@@",url.split("/"))
                    reportname = url.split(pattern)[0]
                    docids = None
                    print("reportname@@@@@@@@@@@@@@",reportname)
                    if "/" in url:
                        docids = url.split("/")[4]
                        reportname = url.split("/")[3]
                elif type == "docx-docx":
                    converter = "docx"
                    extension = "docx"
                    pattern = "/report/%s/" % ("docx")
                    reportname = url.split(pattern)[1].split("?")[0]
                    docids = None
                    if "/" in reportname:
                        reportname, docids = reportname.split("/")
                else:
                    converter = "pdf"
                    extension = "pdf" 
                    pattern = "/report/%s/" % ("pdf")
                    if 4 < len(url.split("/")):
                        reportname = url.split(pattern)[0]
                        docids = None
                        if "/" in url:
                            docids = url.split("/")[4]
                            reportname = url.split("/")[3]
                    else:
                        reportname = url.split(pattern)[1].split("?")[0]
                        docids = None
                        if "/" in reportname:
                            reportname, docids = reportname.split("/")

                print("docids@@@@@@@@@@@@@@@@",docids)
                if docids:
                    # Generic report:
                    response = self.report_routes(
                        reportname, docids=docids, converter=converter, context=context
                    )
                else:
                    # Particular report:
                    data = dict(
                        url_decode(url.split("?")[1]).items()
                    )  # decoding the args represented in JSON
                    if "context" in data:
                        context, data_context = json_loads(context or "{}"), json_loads(
                            data.pop("context")
                        )
                        context = json_dumps({**context, **data_context})
                    response = self.report_routes(
                        reportname, converter=converter, context=context, **data
                    )

                report = request.env["ir.actions.report"]._get_report_from_name(
                    reportname
                )
                filename = "%s.%s" % (report.name, extension)

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(
                            report.print_report_name, {"object": obj, "time": time}
                        )
                        filename = "%s.%s" % (report_name, extension)
                response.headers.add(
                    "Content-Disposition", content_disposition(filename)
                )
                response.set_cookie("fileToken", token)
                return response
            else:
                return super().report_download(data, token, context=context)
        except Exception as e:
            se = _serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}
            return request.make_response(html_escape(json_dumps(error)))
