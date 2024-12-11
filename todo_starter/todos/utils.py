def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
        return "The title must be unique"
    elif not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    else:
        return None

def error_for_todo_title(title, list):
    if not title:
        return "The title must not be empty."
    elif not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    else:
        return None

def find_list_by_id(list_id, lists):
    return next((lst for lst in lists if lst['id'] == list_id), None)

def todos_remaining(lst):
    return sum(1 for todo in lst['todos'] if not todo['completed'])

def is_list_completed(lst):
    print(f"Checking list: {lst['title']}")
    print(f"Number of todos: {len(lst['todos'])}")
    print(f"Remaining todos: {todos_remaining(lst)}")
    return len(lst['todos']) > 0 and todos_remaining(lst) == 0

# def sort_lists(lists):
#     sorted_lists = sorted(lists, key=lambda lst: lst['title'].lower())

#     incomplete_lists = [lst for lst in sorted_lists if not is_list_completed(lst)]
#     complete_lists = [lst for lst in sorted_lists if is_list_completed(lst)]

#     return incomplete_lists + complete_lists

def is_todo_completed(todo):
    return todo['completed']

def mark_all_completed(lst):
    for todo in lst['todos']:
        todo['completed'] = True

    return None

def find_todo_by_id(todo_id, todos):
    return next((todo for todo in todos if todo['id'] == todo_id), None)

def sort_items(items, select_completed):
    sorted_items = sorted(items, key=lambda item: item['title']. lower())

    incompleted_items = [item for item in sorted_items if not select_completed(item)]

    completed_items = [item for item in sorted_items if select_completed(item)]

    return incompleted_items + completed_items