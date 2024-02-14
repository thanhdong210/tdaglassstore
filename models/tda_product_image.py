# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class TDAProductImage(models.Model):
    _name = 'tda.product.image'
    _description = "Product Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    name = fields.Char("Name")
    sequence = fields.Integer(default=10)

    image_1920 = fields.Image()
    tda_product_id = fields.Many2one('tda.product.product')
    tda_feature_product_id = fields.Many2one('tda.product.product')
