import json
from deepdiff import DeepDiff

def get_data_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
    return file_data

def compare_dicts(expected, actual, exclude_paths=None):
    diff = DeepDiff(expected, actual, exclude_paths=exclude_paths)
    diffs_list = []
    has_diffs = len(diff) != 0

    if 'values_changed' in diff:
        for key, change in diff['values_changed'].items():
            diffs_list.append(f"Field '{key}' has changed. Expected value = {change['old_value']}, Actual value = {change['new_value']}")
    if 'dictionary_item_added' in diff:
        for key in diff['dictionary_item_added']:
            diffs_list.append(f"Unexpected field: {key}.")
    if 'dictionary_item_removed' in diff:
        for key in diff['dictionary_item_removed']:
            diffs_list.append(f"Cannot find: {key} field.")
    if 'type_changes' in diff:
        for key, change in diff['type_changes'].items():
            diffs_list.append(f"Field '{key}' changed type: Expected type = {change['old_type']}, Actual type = {change['new_type']}")
    return has_diffs, diffs_list
