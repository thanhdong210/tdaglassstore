from odoo import http
from odoo.http import request
from odoo.http import Response
from werkzeug.exceptions import BadRequest

class TDAAdvisoryRequestControllers(http.Controller):

    @http.route('/advisory_requests', auth='public', methods=['POST'], type='json', website=True, csrf=False, cors="*")
    def advisory_request_get(self, **kw):
        create_data = {
            'name': "",
            'email': "",
            'phone': "",
            'message': "",
        }
        if not kw.get("name", False) and not kw.get("email", False) and not kw.get("phone", False):
            raise BadRequest('Dont allow create empty advisory')
        if kw.get("name", False):
            create_data.update({
                'name': kw.get("name", False)
            })
        if kw.get("email", False):
            create_data.update({
                'email': kw.get("email", False)
            })
        if kw.get("phone", False):
            create_data.update({
                'phone': kw.get("phone", False)
            })
        if kw.get("message", False):
            create_data.update({
                'message': kw.get("message", False)
            })
        try:
            request.env['tda.advisory.request'].sudo().create(create_data)
            return Response('success', status=200)
        except:
            return Response('error while posting advisory', status=500)