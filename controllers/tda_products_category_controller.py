from odoo import http
from odoo.http import request
from odoo.http import Response
import json
from werkzeug.exceptions import Forbidden, NotFound

from . import resource_mixin

class TDAProductCategoryControllers(http.Controller):

    @http.route('/product_category', auth='public', type='http', website=True, csrf=True, cors="*")
    def products_category_view(self, sort_price=False, pagination=0, **kw):
        products = request.env['tda.product.category'].sudo().search_read(
            domain=[],
            fields=['id', 'name', 'name_url', 'parent_id', 'product_info', 'image_links'],
        )
        return Response(json.dumps(products, default=str, ensure_ascii=False))
    
    @http.route('/category_parent', auth='public', type='http', website=True, csrf=True, cors="*")
    def products_category_parent_views(self, id=0, **kw):
        products = False
        products = request.env['tda.product.category'].sudo().search_read(
            domain=[('parent_id', '!=', False)],
            fields=['id', 'name', 'name_url', 'image_links', 'product_info'],
        )
        return Response(json.dumps(products, default=str, ensure_ascii=False))
    
    @http.route('/product_category/<string:name_url>', auth='public', type='http', website=True, csrf=True, cors="*")
    def product_category_detail_view(self, id=0, name_url="", **kw):
        category = False
        if name_url:
            category = request.env['tda.product.category'].sudo().search_read(
                domain=[('name_url', '=', name_url)],
                fields=['id', 'name', 'name_url', 'image_links', 'product_info'],
                limit=1
            )
            total_products = len(category[0].get("product_info"))

            product_info_sorted = resource_mixin.pagination_the_products(category[0].get("product_info"), sort=kw.get("sort", False), page=kw.get("page", False), limit=kw.get("limit", False))

            if product_info_sorted:
                category[0]["product_info"] = product_info_sorted
            if category:
                category = category[0]
                category.update({
                    'total_products': total_products
                })
        return Response(json.dumps(category, default=str, ensure_ascii=False))