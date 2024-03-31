# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
import calendar

class TDAAdvisoryRequest(models.Model):
    _name = 'tda.advisory.request'
    _description = 'TDA Advisory Request'

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    message = fields.Text(string="message")
    state = fields.Selection([('read', 'Read'), ('unread', 'Unread')], string="State", default='unread')

    @api.model
    def get_advisory_request_by_month(self):
        result = {
            'last_7_month_name': [],
            'last_7_month_count': [],
        }
        last_7_month_name = []
        today = fields.Date.today()
        i = 6
        while i >= 0:
            month_name = today - relativedelta(months=i)
            first_day = month_name.replace(day=1)
            last_day = month_name.replace(day=int(calendar.monthrange(month_name.year, month_name.month)[1]))
            result['last_7_month_name'].append(month_name.strftime("%B"))
            result['last_7_month_count'].append(self.search_count([('create_date', '>=', first_day), ('create_date', '<=', last_day)]))
            i -= 1

        return result