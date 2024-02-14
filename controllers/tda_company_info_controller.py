from odoo import http
from odoo.http import request
from odoo.http import Response
import json

class TDACompanyInfo(http.Controller):
    
    @http.route('/company_info', auth='public', type='http', website=True, csrf=True, cors="*")
    def company_info(self, id=0, **kw):
        company_info = request.env['tda.info'].sudo().search_read(
            domain=[],
            fields=['id', 'name', 'tax_code', 'phone1', 'phone2', 'email'],
            limit=3
        )

        for item in company_info:
            company_info_object = request.env['tda.info'].sudo().browse(item.get("id"))
            item.update({
                'address': []
            })
            for address in company_info_object.address_ids:
                item.get("address").append({
                    "name": address.name,
                    "address_detail": address.address
                })
        
        return Response(json.dumps(company_info, default=str, ensure_ascii=False))
    
    @http.route('/projects', auth='public', type='http', website=True, csrf=True, cors="*")
    def tda_projects(self, id=0, **kw):
        projects = request.env['tda.projects'].sudo().search_read(
            domain=[],
            fields=['name', 'name_url', 'category_name', 'create_date'],
        )
        return Response(json.dumps(projects, default=str, ensure_ascii=False))
    
    @http.route('/projects/<string:name_url>', auth='public', type='http', website=True, csrf=True, cors="*")
    def tda_projects_detail(self, id=0, name_url="", **kw):
        projects = False
        if name_url:
            projects = request.env['tda.projects'].sudo().search_read(
                domain=[('name_url', '=', name_url)],
                fields=['name', 'category_name', 'project_detail_html', 'name_url', 'create_date'],
            )
        if projects:
            projects = projects[0]
        return Response(json.dumps(projects, default=str, ensure_ascii=False))    
    
    @http.route('/projects_by_parent/<string:name_url>', auth='public', type='http', website=True, csrf=True, cors="*")
    def tda_projects__by_parent(self, id=0, name_url="", **kw):
        projects_category = False
        if name_url:
            projects_category = request.env['tda.projects.category'].sudo().search_read(
                domain=[('name_url', '=', name_url)],
                fields=['name', 'name_url', 'project_info'],
            )
        if projects_category:
            projects_category = projects_category[0]
        return Response(json.dumps(projects_category, default=str, ensure_ascii=False))
    
    @http.route('/feng_shui', auth='public', type='http', website=True, csrf=True, cors="*")
    def tda_feng_shui(self, id=0, **kw):
        feng_shui_info = request.env['tda.feng.shui'].sudo().search_read(
            domain=[],
            fields=['name', 'image_link', 'create_date', 'name_url'],
        )
        return Response(json.dumps(feng_shui_info, default=str, ensure_ascii=False))
    
    @http.route('/feng_shui/<string:name_url>', auth='public', type='http', website=True, csrf=True, cors="*")
    def tda_feng_shui_detail(self, name_url="", **kw):
        feng_shui_info = False
        if name_url:
            feng_shui_info = request.env['tda.feng.shui'].sudo().search_read(
                domain=[('name_url', '=', name_url)],
                fields=['name', 'feng_shui_detail_html', 'image_link', 'create_date', 'name_url'],
            )
        if feng_shui_info:
            feng_shui_info = feng_shui_info[0]
        return Response(json.dumps(feng_shui_info, default=str, ensure_ascii=False))