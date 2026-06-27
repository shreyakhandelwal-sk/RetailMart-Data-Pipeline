import pandas as pd
import numpy as np
import sqlite3
import os

def run_pipeline():
    conn = None
    try:
        print("=" * 60)
        print("🚀 STARTING RETAILMART ETL PIPELINE")
        print("=" * 60)

        # TASK 1: DATA INGESTION
        
        print("\n📥 [Task 1] Ingesting CSV Files...")
        
        # Check if files exist to support Task 6 error handling requirements
        for file in ['sales_data.csv', 'products.csv', 'stores.csv']:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file '{file}' is missing from the directory.")

        sales_df = pd.read_csv('sales_data.csv')
        products_df = pd.read_csv('products.csv')
        stores_df = pd.read_csv('stores.csv')

        print(f"-> Loaded 'sales_data.csv'. Shape: {sales_df.shape}")
        print(f"-> Loaded 'products.csv'. Shape: {products_df.shape}")
        print(f"-> Loaded 'stores.csv'. Shape: {stores_df.shape}")
        
        print("\n--- Summary of Null Values Before Cleaning ---")
        print(sales_df.isnull().sum())


        # TASK 2: DATA CLEANING
    
        print("\n🧼 [Task 2] Cleaning Sales Data...")
        
        # 3. Remove all duplicate rows
        initial_rows = len(sales_df)
        sales_df.drop_duplicates(inplace=True)
        removed_duplicates = initial_rows - len(sales_df)
        print(f"-> Removed {removed_duplicates} duplicate row(s).")

        # 4. Fill missing values in 'quantity' with 0 and drop rows where 'amount' is NULL
        sales_df['quantity'] = sales_df['quantity'].fillna(0)
        sales_df.dropna(subset=['amount'], inplace=True)
        print(f"-> Handled missing values. Cleaned Sales Shape: {sales_df.shape}")

        # 5. Convert 'sale_date' to proper datetime and 'amount' to float
        sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
        sales_df['amount'] = sales_df['amount'].astype(float)
        print("-> Data types successfully cast (sale_date to datetime, amount to float).")

        
        # TASK 3: DATA TRANSFORMATION
        
        print("\n⚡ [Task 3] Transforming Data...")
        
        # 6. Merge all three DataFrames on store_id and product_id
        merged_df = sales_df.merge(products_df, on='product_id', how='inner')
        merged_df = merged_df.merge(stores_df, on='store_id', how='inner')
        print(f"-> DataFrames successfully merged. Merged Shape: {merged_df.shape}")

        # 7. Add a new column 'total_revenue' = quantity * price using NumPy
        merged_df['total_revenue'] = np.multiply(merged_df['quantity'], merged_df['price'])
        
        print("\n--- NumPy Metrics for 'total_revenue' ---")
        print(f"Mean Revenue : INR {np.mean(merged_df['total_revenue']):,.2f}")
        print(f"Max Revenue  : INR {np.max(merged_df['total_revenue']):,.2f}")
        print(f"Min Revenue  : INR {np.min(merged_df['total_revenue']):,.2f}")

        # 8. Group by 'city', find total revenue per city, and sort descending
        city_revenue = merged_df.groupby('city')['total_revenue'].sum().reset_index()
        city_revenue = city_revenue.sort_values(by='total_revenue', ascending=False)
        print("\n--- Total Revenue Generated Per City ---")
        print(city_revenue.to_string(index=False))


        # TASK 4: DATA LOADING (SQL)

        print("\n💾 [Task 4] Loading Final Dataset to SQLite Database...")
        
        # 9. Establish connection to SQLite and write data to 'retail_sales' table
        conn = sqlite3.connect('retail_mart.db')
        merged_df.to_sql('retail_sales', conn, if_exists='replace', index=False)
        print("-> Loaded final cleaned DataFrame into 'retail_sales' table successfully.")

        
        # TASK 5: REPORTING & INSIGHTS

        print("\n📊 [Task 5] Running Database Reporting Queries...")
        
        # 10. Query for Top 3 best-selling products by total quantity sold
        top_products_query = """
        SELECT product_name, SUM(quantity) as total_quantity_sold
        FROM retail_sales
        GROUP BY product_name
        ORDER BY total_quantity_sold DESC
        LIMIT 3;
        """
        print("\n--- Top 3 Best-Selling Products ---")
        print(pd.read_sql_query(top_products_query, conn).to_string(index=False))

        # 11. Query for total revenue per store per day
        store_day_query = """
        SELECT store_name, DATE(sale_date) as sale_date, SUM(total_revenue) as daily_revenue
        FROM retail_sales
        GROUP BY store_name, sale_date
        ORDER BY sale_date ASC, daily_revenue DESC;
        """
        print("\n--- Total Revenue Per Store Per Day ---")
        print(pd.read_sql_query(store_day_query, conn).to_string(index=False))

        # 12. Python High-level summary report
        print("\n📋 Python Summary Report")
        print("-" * 40)
        print(f"Total Number of Transactions : {len(merged_df)}")
        print(f"Total Revenue Generated      : INR {merged_df['total_revenue'].sum():,.2f}")
        print(f"Top Selling City             : {city_revenue.iloc[0]['city']}")
        
        # Determine top product by aggregating quantity
        top_prod_df = merged_df.groupby('product_name')['quantity'].sum().reset_index()
        top_product = top_prod_df.sort_values(by='quantity', ascending=False).iloc[0]['product_name']
        print(f"Top Selling Product          : {top_product}")

        print("\n" + "=" * 60)
        print("🎉 PIPELINE RUN COMPLETED SUCCESSFULLY WITHOUT CRASHES!")
        print("=" * 60)


    # TASK 6: PIPELINE & ERROR HANDLING
    
    # 14. Basic error handling so missing files print a clear error instead of crashing
    except FileNotFoundError as e:
        print("\n❌ [PIPELINE CRITICAL ERROR]: A required data file was missing.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\n❌ [UNEXPECTED PIPELINE FAILURE]: {e}")
    finally:
        if conn:
            conn.close()
            print("\n🔒 SQLite database connection cleanly closed.")

# 13. Write a python function called run_pipeline() that runs all above steps in one single function call.
if __name__ == "__main__":
    run_pipeline()