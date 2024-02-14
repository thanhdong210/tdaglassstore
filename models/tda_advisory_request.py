# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class TDAAdvisoryRequest(models.Model):
    _name = 'tda.advisory.request'
    _description = 'TDA Advisory Request'

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    message = fields.Text(string="message")
    state = fields.Selection([('read', 'Read'), ('unread', 'Unread')], string="State", default='unread')