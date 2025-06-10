def error_for_list_title(title, lists):

    if any(title.casefold() == lst['title'].casefold() for lst in lists):
        return "The title must be unique."
    elif not 1 <= len(title) <= 100:
        return "The title must be 100 characters or less."
    else:
        return None

def error_for_todo_title(title, todo):
    if 0 < len(title) <= 100:
        return 'You created a new todo item'
    else:
        return None
    
def find_list_by_id(list_id, all_lsts):
    for lst in all_lsts:
        print(f"Comparing (repr): '{repr(list_id)}' vs '{repr(lst['id'])}'")
        print(f"Lengths: '{len(list_id)}' vs '{len(lst['id'])}'")
        print(f"Types: '{type(list_id)}' vs '{type(lst['id'])}'")
        if lst['id'] == list_id:
            return lst
    return None

    