# -----------------------------------------------------------------------------
def paginate(path, items, per_page):
    """
    Paginate a list of items and return all necessary data for static HTML generation.

    :param items: list of items to paginate.
    :param per_page: number of items per page (default is 10).
    :return: a dictionary with pagination details for static HTML generation.
    """
    total_items = len(items)

    # calculate total number of pages
    total_pages = (total_items + per_page - 1) // per_page

    # generate pagination data for each page
    pagination_data = []

    for current_page in range(1, total_pages + 1):
        # calculate start and end indices for current page
        start_index = (current_page - 1) * per_page
        end_index = min(start_index + per_page, total_items)

        # define the page range to display in the paginator (current page ± 2)
        page_range_start = max(1, current_page - 2)
        page_range_end = min(total_pages, current_page + 2)
        page_range = list(range(page_range_start, page_range_end + 1))

        # data for the current page
        page_data = {
            "path": path,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "items": items[start_index:end_index],
            "page_range": page_range,
            "has_previous": current_page > 1,
            "has_next": current_page < total_pages,
            "previous_page": current_page - 1 if current_page > 1 else None,
            "next_page": current_page + 1 if current_page < total_pages else None,
            "first_page": 1,
            "last_page": total_pages,
        }

        pagination_data.append(page_data)

    return {
        "pages": pagination_data,
        "total_items": total_items,
        "total_pages": total_pages,
    }


# -----------------------------------------------------------------------------
def empty(path):
    return {
        "pages": [],
        "total_items": 0,
        "total_pages": 0,
    }
