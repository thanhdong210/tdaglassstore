# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from . import resource_mixin
from odoo.exceptions import ValidationError

class TDAProducts(models.Model):
    _name = 'tda.product.product'
    _description = 'Products'

    name = fields.Char(string="Name")
    category_id = fields.Many2one('tda.product.category', string="Product Category")
    category_name = fields.Char(string="Category Name", related="category_id.name", store=True)
    category_name_url = fields.Char(string="Category Name Url", related="category_id.name_url")
    price = fields.Float(string="Price")
    discount_price = fields.Float(string="Discount price")
    description = fields.Text(string="Description")
    product_detail_html = fields.Html(string="Product html")
    is_price_contact = fields.Boolean(string="Contact for price")
    name_url = fields.Char(string="Name url", compute="_compute_name_url", store=True)
    product_template_image_ids = fields.One2many('tda.product.image', 'tda_product_id', string="Extra Product Media", copy=True)
    image_links = fields.Json(string="Image Link", compute="_compute_image_link", store=True)
    image_link = fields.Json(string="Image Link", compute="_compute_image_link_one", store=True)
    is_featured = fields.Boolean(string="Featured")
    image_featured_file_ids = fields.One2many('tda.product.image', 'tda_feature_product_id', string="Featured product image")
    featured_link = fields.Json(string="Image Featured Link", compute="_compute_image_featured_link", store=True)
    
    @api.depends("name")
    def _compute_name_url(self):
        for rec in self:
            if rec.name:
                rec.name_url = "-".join(resource_mixin.convert(rec.name).split())

    @api.depends("image_links")
    def _compute_image_link_one(self):
        for rec in self:
            if rec.image_links:
                rec.image_link = rec.image_links[0].get("image_link", "")
            else:
                rec.image_link = ""

    @api.depends("product_template_image_ids")
    def _compute_image_link(self):
        for rec in self:
            if rec.product_template_image_ids:
                rec.get_image_url("product_template_image_ids", "image_links")
            else:
                rec.image_links = ""


    @api.depends("image_featured_file_ids", "featured_link")
    def _compute_image_featured_link(self):
        for rec in self:
            if rec.image_featured_file_ids:
                rec.get_image_url("image_featured_file_ids", "featured_link")
            else:
                rec.featured_link = ""

    def get_image_url(self, fields, fields_to_compute):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        list_data = []
        for attachment in self[fields]:
            idx = False
            if attachment.id:
                idx = attachment.id
            elif attachment._origin:
                idx = attachment._origin.id
            if idx:
                list_data.append({
                    'id': idx,
                    'image_link': base_url + "/web/image?model=tda.product.image&id=%s&field=image_1920" % (idx)
                })
            self[fields_to_compute] = list_data

        if not self[fields]:
            self[fields_to_compute] = []

    @api.constrains('image_featured_file_ids')
    def _check_image_feature(self):
        for image in self:
            if image.image_featured_file_ids and len(image.image_featured_file_ids) > 1:
                raise ValidationError(_("Feature image can only cantain one item!"))
                
    @api.model
    def get_data(self):
        """Returns data to the tiles of dashboard"""
        products = self.env['tda.product.product'].search_count([])
        categories = self.env['tda.product.category'].search_count([])
        return {
            'products': products,
            'categories': categories,
        }
    
    @api.model
    def get_product_by_category(self):
        products_group = self.read_group([], ['name', 'category_name'], 'category_id')

        result = {
            'categories_name': [],
            'categories_count': []
        }

        for data in products_group:
            if data["category_id"]:
                category_name = self.env['tda.product.category'].browse(data["category_id"][0])
                result['categories_name'].append(category_name.name)
            else:
                result['categories_name'].append(_("Undefined"))
            result['categories_count'].append(data["category_id_count"])

        # print("<<<<<<<<<<<<<<<<<<4", result)

        return result
    