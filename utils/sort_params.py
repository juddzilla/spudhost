def sort_params(query_params):
    sort_direction = query_params.get('sortDirection')
    sort_property = query_params.get('sortProperty')
    search = query_params.get('search')    
    
    order_by = sort_property
    if sort_direction == 'desc':
        order_by = f"-{order_by}"
    
    return {
        'order_by': order_by,
        'search': search,
    }