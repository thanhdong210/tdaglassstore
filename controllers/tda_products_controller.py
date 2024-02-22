from odoo import http
from odoo.http import request
import requests
from odoo.http import Response
import json
from . import resource_mixin

class TDAProductControllers(http.Controller):

    @http.route('/products', auth='public', type='http', website=True, csrf=True, cors="*")
    def products_view(self, **kw):
        if kw.get("keyword", False):
            products = request.env['tda.product.product'].sudo().search_read(
                domain=[
                    '|',
                        ('name', 'ilike', kw.get("keyword")),
                        ('name_url', 'ilike', kw.get("keyword"))
                ],
                fields=['id', 'name', 'category_name', 'discount_price', 'price', 'is_price_contact', 'name_url', 'image_link'],
            )
        else:
            products = request.env['tda.product.product'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'category_name', 'discount_price', 'price', 'is_price_contact', 'name_url', 'image_link'],
            )

        total_products = len(products)

        product_info_sorted = resource_mixin.pagination_the_products(products, sort=kw.get("sort", False), page=kw.get("page", False), limit=kw.get("limit", False), search=kw.get("keyword", False))

        dict_data = {
            'list_product': product_info_sorted,
            'total_products': total_products
        }
        return Response(json.dumps(dict_data, default=str, ensure_ascii=False))

    @http.route('/products_by_category/<string:name_url>', auth='public', type='http', website=True, csrf=True, cors="*")
    def products_category_views(self, id=0, name_url="", **kw):
        products = False
        if name_url:
            products = request.env['tda.product.product'].sudo().search_read(
                domain=[('category_id.name_url', '=', id)],
                fields=['id', 'name', 'category_name', 'discount_price', 'price', 'is_price_contact', 'name_url'],
            )
        return Response(json.dumps(products, default=str, ensure_ascii=False))
    
    @http.route('/product_detail/<string:name_url>', auth='public', type='http', website=True, csrf=True, cors="*")
    def product_detail_view(self, id=0, name_url="", **kw):
        products = False
        if name_url:
            products = request.env['tda.product.product'].sudo().search_read(
                domain=[('name_url', '=', name_url)],
                fields=['id', 'name', 'category_name', 'image_links', 'discount_price', 'price', 'is_price_contact', 'description', 'product_detail_html', 'name_url', 'category_name_url'],
            )
        if products:
            products = products[0]
        return Response(json.dumps(products, default=str, ensure_ascii=False))
    
    @http.route('/products_featured', auth='public', type='http', website=True, csrf=True, cors="*")
    def product_featured_view(self, **kw):
        products = request.env['tda.product.product'].sudo().search_read(
            domain=[('is_featured', '=', True)],
            fields=['id', 'name', 'featured_link', 'name_url'],
        )
        return Response(json.dumps(products, default=str, ensure_ascii=False))
    
    @http.route('/products_search', auth='public', type='http', website=True, csrf=True, cors="*")
    def product_search(self, **kw):
        if kw.get("name"):
            products = request.env['tda.product.product'].sudo().search_read(
                domain=[
                    '|',
                        ('name', 'ilike', kw.get("name")),
                        ('name_url', 'ilike', kw.get("name"))
                ],
                fields=['id', 'name', 'category_name', 'discount_price', 'price', 'is_price_contact', 'name_url'],
            )
        else:
            products = request.env['tda.product.product'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'category_name', 'discount_price', 'price', 'is_price_contact', 'name_url'],
            )
        return Response(json.dumps(products, default=str, ensure_ascii=False))