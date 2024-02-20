# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from . import resource_mixin

class TDAProjectsCategory(models.Model):
    _name = 'tda.projects.category'
    _description = 'TDA projects category'

    name = fields.Char(string="Name")
    name_url = fields.Char(string="Name url", compute="_compute_name_url", store=True)
    project_ids = fields.One2many("tda.projects", 'category_id', string="Projects")
    project_info = fields.Json(string="Product info", compute="_compute_project_info", store=True)

    @api.depends("project_ids", "project_ids.image", "project_ids.name", "project_ids.name_url")
    def _compute_project_info(self):
        for rec in self:
            list_data = []
            for project in rec.project_ids:
                list_data.append({
                    'id': project.id,
                    'name': project.name,
                    'name_url': project.name_url,
                    'project_image': project.image_link,
                })
            rec.project_info = list_data

    @api.depends("name")
    def _compute_name_url(self):
        for rec in self:
            if rec.name:
                rec.name_url = "-".join(resource_mixin.convert(rec.name).split())

class TDAProjects(models.Model):
    _name = 'tda.projects'
    _description = 'TDA projects'

    name = fields.Char(string="Name")
    name_url = fields.Char(string="Name url", compute="_compute_name_url", store=True)
    category_id = fields.Many2one('tda.projects.category', string="Category")
    category_name = fields.Char(string="Category Name", related="category_id.name")
    project_detail_html = fields.Html(string="Product detail html")
    image = fields.Image("Image", max_width=1920, max_height=1920)
    image_link = fields.Char("Image link", compute="_compute_image_link", store=True)
    author = fields.Char("Author", related="create_uid.name")
    type = fields.Char(default='project')

    def _compute_image_link(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            rec.image_link = base_url + "/web/image?model=tda.projects&id=%s&field=image" % (rec.id)

    @api.depends("name")
    def _compute_name_url(self):
        for rec in self:
            if rec.name:
                rec.name_url = "-".join(resource_mixin.convert(rec.name).split())