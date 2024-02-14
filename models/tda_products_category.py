# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from . import resource_mixin

class TDAProductsCategory(models.Model):
    _name = 'tda.product.category'
    _description = 'Products Category'

    name = fields.Char(string="Name")
    parent_id = fields.Many2one("tda.product.category", string="Parent")
    name_url = fields.Char(string="Name url", compute="_compute_name_url", store=True)
    image_file_ids = fields.Many2many('ir.attachment')
    image_links = fields.Json(string="Image Link", compute="_compute_image_link", store=True)
    product_ids = fields.One2many("tda.product.product", 'category_id', string="Products")
    product_info = fields.Json(string="Product info", compute="_compute_product_info", store=True)

    @api.depends( "product_ids", "product_ids.image_links", "product_ids.name", "product_ids.name_url")
    def _compute_product_info(self):
        for rec in self:
            list_data = []
            for product in rec.product_ids:
                list_data.append({
                    'id': product.id,
                    'name': product.name,
                    'name_url': product.name_url,
                    'product_image': product.image_links,
                })
            rec.product_info = list_data

    @api.depends("name")
    def _compute_name_url(self):
        for rec in self:
            if rec.name:
                rec.name_url = "-".join(resource_mixin.convert(rec.name).split())

    @api.depends("image_file_ids")
    def _compute_image_link(self):
        list_data = []
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            for attachment in rec.image_file_ids:
                idx = False
                if attachment.id:
                    idx = attachment.id
                elif attachment._origin:
                    idx = attachment._origin.id
                if idx:
                    list_data.append({
                        'id': idx,
                        'image_link': base_url + "/web/image/ir.attachment/%s/datas" % idx
                    })
            rec.image_links = list_data