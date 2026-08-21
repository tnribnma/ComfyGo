from typing import Dict, Any
from math import ceil


def calculate_pagination(total: int, page: int, page_size: int) -> Dict[str, Any]:
    if page_size <= 0:
        raise ValueError("page_size must be greater than 0")
    
    pages = ceil(total / page_size) if total > 0 else 1
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
        "skip": (page - 1) * page_size,
    }