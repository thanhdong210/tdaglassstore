# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from . import resource_mixin

class TDAFengshui(models.Model):
    _name = 'tda.feng.shui'
    _description = 'TDA Feng Shui'

    name = fields.Char(string="Name")
    name_url = fields.Char(string="Name url", compute="_compute_name_url", store=True)
    feng_shui_detail_html = fields.Html(string="Feng shui HTML")
    image = fields.Image("Image", max_width=1920, max_height=1920)
    image_link = fields.Char("Image link", compute="_compute_image_link")
    author = fields.Char("Author", related="create_uid.name")
    type = fields.Char(default='fengshui')

    @api.depends("name")
    def _compute_name_url(self):
        for rec in self:
            if rec.name:
                rec.name_url = "-".join(resource_mixin.convert(rec.name).split())

    def _compute_image_link(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            rec.image_link = base_url + "/web/image?model=tda.feng.shui&id=%s&field=image" % (rec.id)