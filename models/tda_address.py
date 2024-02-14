# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class TDAAddress(models.Model):
    _name = 'tda.address'
    _description = 'TDA Address'

    name = fields.Char(string="Name")
    address = fields.Text(string="Address")