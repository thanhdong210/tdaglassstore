# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class TDAInfo(models.Model):
    _name = 'tda.info'
    _description = 'TDA Info'

    name = fields.Char(string="Name")
    tax_code = fields.Char(string="Tax code")
    phone1 = fields.Char(string="Phone 1")
    phone2 = fields.Char(string="Phone 2")
    email = fields.Char(string="Email")
    address_ids = fields.Many2many('tda.address', string="Address")
    working_time_ids = fields.One2many('tda.working.time', 'info_id', string="Working time")
    company_detail_html = fields.Html(string="Product html")