import tkinter as tk
import json
from tkinter import messagebox

class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {"name": self.name, "price": self.price, "quantity": self.quantity}
    
    def display_info(self):
        return f"✔️ {self.name} (قیمت: {self.price}, تعداد: {self.quantity})"

    # متد برای افزایش موجودی (جدید)
    def increase_quantity(self, amount):
        self.quantity += amount
        print(f"موجودی {self.name} به اندازه {amount} افزایش یافت. تعداد کل: {self.quantity}")

    # متد برای کاهش موجودی (درخواستی شما)
    def reduce_quantity(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            print(f"{amount} واحد از {self.name} فروخته شد. تعداد باقی‌مانده: {self.quantity}")
            return True
        else:
            print(f"موجودی کافی نیست. تعداد فعلی: {self.quantity}")
            return False

inventory_list = []
selected_item_index = -1

def add_item():
    global selected_item_index
    item_name = name_entry.get()
    item_price_str = price_entry.get()
    item_quantity_str = quantity_entry.get()
    
    try:
        item_price = float(item_price_str)
        item_quantity = int(item_quantity_str)
        
        if selected_item_index == -1:
            new_item = Item(item_name, item_price, item_quantity)
            inventory_list.append(new_item)
            output_label.config(text="کالای جدید اضافه شد.", fg="green")
        else:
            inventory_list[selected_item_index].name = item_name
            inventory_list[selected_item_index].price = item_price
            inventory_list[selected_item_index].quantity = item_quantity
            output_label.config(text="کالا با موفقیت ویرایش شد.", fg="blue")
            selected_item_index = -1

        update_listbox_display(inventory_list)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        calculate_total_value()
    
    except ValueError:
        output_label.config(text="لطفاً قیمت و تعداد را به صورت عدد وارد کنید.", fg="red")

def update_listbox_display(items_to_display):
    inventory_box.delete(0, tk.END)
    for item in items_to_display:
        inventory_box.insert(tk.END, item.display_info())

def remove_item():
    try:
        selected_indices = inventory_box.curselection()
        for index in reversed(selected_indices):
            inventory_box.delete(index)
            inventory_list.pop(index)
        
        output_label.config(text="آیتم‌های انتخاب شده با موفقیت حذف شدند.", fg="blue")
        calculate_total_value()
    
    except IndexError:
        output_label.config(text="لطفاً یک یا چند آیتم را برای حذف انتخاب کنید.", fg="red")

def load_item_for_editing():
    global selected_item_index
    try:
        selected_index = inventory_box.curselection()[0]
        selected_item_index = selected_index
        item = inventory_list[selected_index]
        
        name_entry.delete(0, tk.END)
        name_entry.insert(0, item.name)
        
        price_entry.delete(0, tk.END)
        price_entry.insert(0, str(item.price))
        
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, str(item.quantity))
        
        output_label.config(text="لطفاً آیتم را ویرایش و ذخیره کنید.", fg="blue")
    
    except IndexError:
        output_label.config(text="لطفاً یک آیتم را برای ویرایش انتخاب کنید.", fg="red")

def save_inventory():
    try:
        data_to_save = [item.to_dict() for item in inventory_list]
        with open("inventory.json", "w") as file:
            json.dump(data_to_save, file)
        output_label.config(text="موجودی با موفقیت ذخیره شد.", fg="blue")
    except Exception as e:
        output_label.config(text=f"خطا در ذخیره سازی: {e}", fg="red")

def load_inventory():
    global inventory_list
    try:
        with open("inventory.json", "r") as file:
            data_loaded = json.load(file)
            inventory_list = [Item(item['name'], item['price'], item['quantity']) for item in data_loaded]
        update_listbox_display(inventory_list)
        calculate_total_value()
        output_label.config(text="موجودی با موفقیت بارگذاری شد.", fg="blue")
    except FileNotFoundError:
        output_label.config(text="فایل ذخیره شده‌ای پیدا نشد.", fg="red")
    except Exception as e:
        output_label.config(text=f"خطا در بارگذاری: {e}", fg="red")

def on_closing():
    if messagebox.askyesno("خروج", "آیا می‌خواهید موجودی را قبل از خروج ذخیره کنید؟"):
        save_inventory()
    root.destroy()

def calculate_total_value():
    total_value = sum(item.price * item.quantity for item in inventory_list)
    total_value_label.config(text=f"ارزش کل موجودی: {total_value} تومان")

root = tk.Tk()
root.title("سیستم مدیریت موجودی")
root.protocol("WM_DELETE_WINDOW", on_closing)

name_label = tk.Label(root, text="نام کالا:")
name_label.pack(pady=2)
name_entry = tk.Entry(root)
name_entry.pack(pady=2)

price_label = tk.Label(root, text="قیمت کالا:")
price_label.pack(pady=2)
price_entry = tk.Entry(root)
price_entry.pack(pady=2)

quantity_label = tk.Label(root, text="تعداد:")
quantity_label.pack(pady=2)
quantity_entry = tk.Entry(root)
quantity_entry.pack(pady=2)

add_button = tk.Button(root, text="افزودن/ذخیره", command=add_item) 
add_button.pack(pady=5) 

remove_button = tk.Button(root, text="حذف", command=remove_item)
remove_button.pack(pady=5)

edit_button = tk.Button(root, text="ویرایش", command=load_item_for_editing)
edit_button.pack(pady=5)

save_button = tk.Button(root, text="ذخیره موجودی", command=save_inventory)
save_button.pack(pady=5)

load_button = tk.Button(root, text="بارگذاری موجودی", command=load_inventory)
load_button.pack(pady=5)

output_label = tk.Label(root, text="", fg="red")           
output_label.pack(pady=5) 

inventory_box = tk.Listbox(root, height=10, width=50, selectmode=tk.EXTENDED)
inventory_box.pack(pady=10)

total_value_label = tk.Label(root, text="ارزش کل موجودی: 0 تومان", font=("Arial", 12, "bold"))
total_value_label.pack(pady=10)

load_inventory()

root.mainloop()