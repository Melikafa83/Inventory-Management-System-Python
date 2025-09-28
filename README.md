The application includes robust functionality to edit existing inventory items without needing a separate 'Save Changes' button.

1. Loading Data for Edit (load_item_for_editing)

This function is triggered by the "ویرایش" (Edit) button and is responsible for preparing the UI for modification:

    It identifies the currently selected item in the listbox.

    It sets a global variable, selected_item_index, to the index of the chosen item. This is the crucial flag the system uses to determine the next action.

    It populates the name, price, and quantity of the selected Item object into the respective input fields (Entry widgets).

2. Saving Edited Data (via add_item)

The system intentionally reuses the "افزودن/ذخیره" (Add/Save) button for two purposes:

    If selected_item_index is -1: A new item is created and appended to the inventory_list.

    If selected_item_index is an actual index (not -1): The function recognizes that an item is being edited. It directly modifies the attributes (name, price, quantity) of the existing Item object at that index within the inventory_list. After the update, it resets selected_item_index back to -1 to prepare for the next action.
