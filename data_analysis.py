import pandas as pd
import matplotlib.pyplot as plt

# مرحله ۱: خواندن فایل CSV و ذخیره در یک DataFrame
try:
    df = pd.read_csv('sales_data.csv')

    # مرحله ۲: نمایش ۵ ردیف اول برای بررسی
    print("Top 5 rows of the data (Head):")
    print(df.head())

    # مرحله ۳: بررسی اطلاعات کلی ستون‌ها (انواع داده و تعداد مقادیر)
    print("\nData Info:")
    df.info()

except FileNotFoundError:
    print("خطا: فایل sales_data.csv پیدا نشد.")
    print("لطفاً یک فایل CSV به نام 'sales_data.csv' در کنار این فایل پایتون ایجاد کنید.")# محاسبه مجموع کل فروش
total_revenue = df['Sales'].sum()

# محاسبه مجموع کل تعداد
total_quantity_sold = df['Quantity'].sum()

print("\n--- Summary Statistics ---")
print(f"Total Revenue: ${total_revenue}")
print(f"Total Quantity Sold: {total_quantity_sold} units")

# فیلتر کردن DataFrame برای فقط منطقه 'East'
east_sales_df = df[df['Region'] == 'East']

print("\n--- Sales in East Region ---")
print(east_sales_df)

# محاسبه مجموع کل فروش فقط در منطقه 'East'
east_revenue = east_sales_df['Sales'].sum()

print(f"\nTotal Revenue in East: ${east_revenue}")

sales_by_region=df.groupby('Region')['Sales'].sum()
print("\n---Total sales by Region---")
print(sales_by_region)

average_sales_by_region=df.groupby('Region')['Sales'].mean()
print("\n---Average Sales by Region---")
print(average_sales_by_region)

plt.figure(figsize=(8,6))
sales_by_region.plot(kind='bar',color=['blue','green','red'])
plt.title("Total Sales Revenue by Region")
plt.xlabel('Region')
plt.ylabel('Total sales (in currency)')
plt.xticks(rotation=0)
plt.show()
