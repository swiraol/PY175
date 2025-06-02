def error_for_list_title(title, lists):

    if any(title.casefold() == lst['title'].casefold() for lst in lists):
        return "The title must be unique."
    elif not 1 <= len(title) <= 100:
        return "The title must be 100 characters or less."
    else:
        return None
    
def find_list_by_id(list_id, all_lsts):
    for lst in all_lsts:
        if lst['id'] == list_id:
            return lst
        else:   
            return None

    