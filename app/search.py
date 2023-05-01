from app import app

def add_to_index(index, model):
    """
    Get the index and model
    Check if elasticsearch is accessible
    Loop through the fields listed in the choice model as searchable
    Get the index, id, and search content
    """

    # Check if elasticsearch is configured, if not return nothing
    if not app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    app.elasticsearch.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
    """
    Get the index and a model's id
    Pass the values to the delete() function from elasticsearch
    """
    if not app.elasticsearch:
        return
    app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if app.elasticsearch:
        return [], 0
    search = app.elasticsearch.search(
        index=index,
        body={
            'query': {'multi_match': {'query': query, 'fields': ['*']}},
            'from': (page - 1) * per_page,
            'size': per_page
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
