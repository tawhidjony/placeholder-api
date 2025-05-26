def response_paginated(data, total, page, limit, message="Data fetched successfully."):
    """
    পেজিনেটেড API রেসপন্স তৈরির জন্য কমন ফাংশন।

    Parameters:
    - data (list): মূল ডেটার তালিকা (যেমন: ইউজার লিস্ট)
    - total (int): মোট ডেটার সংখ্যা
    - page (int): কারেন্ট পেজ নম্বর
    - limit (int): প্রতি পেজে কতটি আইটেম
    - message (str): রেসপন্স মেসেজ (ঐচ্ছিক)

    Returns:
    dict: সফল রেসপন্স সহ পেজিনেশন ডেটা
    """
    if not isinstance(page, int) or page < 1:
        return {
            "success": False,
            "message": "Invalid page number. Page must be a positive integer.",
            "data": [],
            "pagination": None
        }

    if not isinstance(limit, int) or limit < 1:
        return {
            "success": False,
            "message": "Invalid limit. Limit must be a positive integer.",
            "data": [],
            "pagination": None
        }

    offset = (page - 1) * limit
    total_pages = (total + limit - 1) // limit

    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": total_pages,
            "has_next": offset + limit < total,
            "has_prev": page > 1
        }
    }
