📊 RetailMart Data Engineering Project

 📝 Project Description
RetailMart is a retail store chain with multiple branches across India. Every day, sales data from these branches is saved in different CSV files. This raw data is usually quite messy—it contains duplicate rows, missing values, and incorrect formats.

The goal of this project was to build a Python ETL Pipeline that automatically reads these files (`sales_data.csv`, `products.csv`, `stores.csv`), cleans up the errors, and saves everything into a structured SQL Database (`retail_mart.db`). Finally, a simple frontend dashboard was created to visualize the cleaned sales data.

---

🛠️ Tech Stack Used & Reasons

 1. Python
Why used: It is the core language used to automate the entire process. We wrapped all the steps into a single function called `run_pipeline()` so the entire project runs with just one command

 2. Pandas Library
Why used: It makes it very easy to load CSV files, merge different tables together using common keys, and find or fix missing values in rows and columns.

 3. NumPy Library
Why used: We needed to calculate the total revenue (`quantity × price`). Instead of using slow standard Python loops, NumPy uses fast array math to calculate this column instantly.

 4. SQLite & SQL
Why used: SQLite creates a lightweight, local database file (`retail_mart.db`) without needing a heavy external database server. We used core SQL queries like `SELECT`, `SUM`, and `GROUP BY` to find business insights like the top-selling products and daily store revenues.

 5. Streamlit
Why used: Streamlit allows building a clean frontend web dashboard (with charts and tables) using purely Python, without needing to write complex HTML, CSS, or JavaScript.



 🚀 Project Approach (How it Works)

The project follows a standard 3-step data engineering process:

1. Extract: The script checks if the raw CSV files exist in the folder and loads them into memory.
2. Transform (Data Cleaning): Removed exact duplicate rows based on transaction IDs.
   * Filled missing item quantities with `0` so the calculations don't break.
   * Dropped any rows completely if the main sales amount was missing.
   * Multiplied quantity and price using NumPy to create a new `total_revenue` column.
3. Load: The final cleaned and merged data is saved into a table named `retail_sales` inside the SQLite database.



 🔗 Project Components & Links

Frontend Dashboard UI: Built with Streamlit. It displays visual bar charts of revenue per city and top-selling items. *(To run it, type `streamlit run dashboard.py` in the terminal).*
Backend & SQL Database: Powered by the main Python pipeline script (`pipeline.py`) and a local SQLite database (`retail_mart.db`).
Source Code Link: [https://github.com/your-username/RetailMart-Data-Pipeline](https://github.com/your-username/RetailMart-Data-Pipeline) 