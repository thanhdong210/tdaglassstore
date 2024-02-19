from werkzeug.exceptions import NotFound

def pagination_the_products(products, sort=False, page=False, limit=False, search=False):
    product_info_sorted = products
    if sort:
        if sort == "newest":
            product_info_sorted = sorted(products, key=lambda d: d['id'], reverse=True)
        elif sort == "alphabet":
            product_info_sorted = sorted(products, key=lambda d: d['name'])

    if page and limit:
        page_pag = 0
        limit_pag = 0
        try:
            page_pag = int(page)
            limit_pag = int(limit)
        except:
            return NotFound()
        if page_pag < 0 or limit_pag <= 0:
            return NotFound()
        
        # Retrieve data for a specify page
        start_index = (page_pag - 1) * limit_pag
        end_index = page_pag * limit_pag
        product_info_sorted = product_info_sorted[start_index:end_index]

    return product_info_sorted