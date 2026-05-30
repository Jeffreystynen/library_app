"""Input validation utilities."""
from utils.constants import BookStatus, Rating, ErrorMessages


def validate_book_status(status):
    """Validate book status."""
    if not BookStatus.is_valid(status):
        return False, ErrorMessages.INVALID_STATUS
    return True, None


def validate_rating(rating):
    """Validate book rating."""
    if not Rating.is_valid(rating):
        return False, ErrorMessages.INVALID_RATING
    return True, None


def validate_required_fields(data, required_fields):
    """Validate that required fields are present in data."""
    if not isinstance(data, dict):
        return False, ErrorMessages.INVALID_REQUEST

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            return False, ErrorMessages.MISSING_FIELD.format(field)

    return True, None


def validate_string(value, field_name, min_length=1, max_length=None):
    """Validate string field."""
    if not isinstance(value, str):
        return False, f"{field_name} must be a string"

    if len(value) < min_length:
        return False, f"{field_name} must be at least {min_length} character(s)"

    if max_length and len(value) > max_length:
        return False, f"{field_name} must be at most {max_length} character(s)"

    return True, None


def validate_integer(value, field_name, min_value=None, max_value=None):
    """Validate integer field."""
    try:
        val = int(value)
    except (ValueError, TypeError):
        return False, f"{field_name} must be an integer"

    if min_value is not None and val < min_value:
        return False, f"{field_name} must be at least {min_value}"

    if max_value is not None and val > max_value:
        return False, f"{field_name} must be at most {max_value}"

    return True, None


def validate_book_data(data):
    """Validate book creation/update data."""
    errors = {}

    # Title (required)
    if "title" in data:
        valid, msg = validate_string(data["title"], "title", min_length=1, max_length=255)
        if not valid:
            errors["title"] = msg

    # Author ID (required for new books)
    if "author_id" in data:
        valid, msg = validate_integer(data["author_id"], "author_id", min_value=1)
        if not valid:
            errors["author_id"] = msg

    # Pages (optional but must be valid)
    if "pages" in data and data["pages"] is not None:
        valid, msg = validate_integer(data["pages"], "pages", min_value=1)
        if not valid:
            errors["pages"] = msg

    # Publication year (optional but must be valid)
    if "publication_year" in data and data["publication_year"] is not None:
        valid, msg = validate_integer(data["publication_year"], "publication_year", min_value=1000, max_value=2100)
        if not valid:
            errors["publication_year"] = msg

    # Description (optional)
    if "description" in data and data["description"] is not None:
        if not isinstance(data["description"], str):
            errors["description"] = "description must be a string"

    if errors:
        return False, str(errors)
    return True, None


def validate_status_update(data):
    """Validate status update data."""
    errors = {}

    if "status" not in data:
        return False, "status field is required"

    valid, msg = validate_book_status(data["status"])
    if not valid:
        errors["status"] = msg

    if errors:
        return False, str(errors)
    return True, None


def validate_rating_update(data):
    """Validate rating update data."""
    errors = {}

    if "rating" not in data:
        return False, "rating field is required"

    valid, msg = validate_rating(data["rating"])
    if not valid:
        errors["rating"] = msg

    if errors:
        return False, str(errors)
    return True, None


def validate_progress_update(data):
    """Validate reading progress update."""
    errors = {}

    if "pages_read" not in data:
        return False, "pages_read field is required"

    valid, msg = validate_integer(data["pages_read"], "pages_read", min_value=0)
    if not valid:
        errors["pages_read"] = msg

    if errors:
        return False, str(errors)
    return True, None


def validate_review_data(data):
    """Validate review data."""
    errors = {}

    # Rating (required)
    if "rating" not in data:
        return False, "rating field is required"

    valid, msg = validate_rating(data["rating"])
    if not valid:
        errors["rating"] = msg

    # Title (optional)
    if "title" in data and data["title"] is not None:
        valid, msg = validate_string(data["title"], "title", min_length=1, max_length=255)
        if not valid:
            errors["title"] = msg

    # Content (required)
    if "content" not in data or not data["content"]:
        return False, "content field is required"

    if not isinstance(data["content"], str):
        errors["content"] = "content must be a string"
    elif len(data["content"]) < 10:
        errors["content"] = "content must be at least 10 characters"

    # Spoiler warning (optional, boolean)
    if "spoiler_warning" in data and data["spoiler_warning"] is not None:
        if not isinstance(data["spoiler_warning"], bool):
            errors["spoiler_warning"] = "spoiler_warning must be a boolean"

    if errors:
        return False, str(errors)
    return True, None
