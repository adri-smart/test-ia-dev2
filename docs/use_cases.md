# KAN-468: 10 Predefined Business Use Cases

This document outlines 10 predefined business use cases for the conversational agent. These will be used to consistently measure the correct interpretation rate and ensure the project meets its success KPIs.

### Case 1: Total Sales in a Period
*   **User Query**: "What were our total sales last month?"
*   **Expected Interpretation**:
    *   **Intent**: `query_sales`
    *   **Entities**: `period: last_month`
*   **Expected Action**: The system should calculate the sum of sales from all transactions in the previous calendar month and return the total amount.

### Case 2: Top Selling Products
*   **User Query**: "Show me the top 5 best-selling products in Q2."
*   **Expected Interpretation**:
    *   **Intent**: `query_top_products`
    *   **Entities**: `limit: 5`, `period: Q2`
*   **Expected Action**: The system should identify the second quarter of the current year, aggregate sales data by product, and return a list of the top 5 products by sales volume or revenue.

### Case 3: Customer Segmentation by Location
*   **User Query**: "List all customers from Germany who have spent more than 1000 euros."
*   **Expected Interpretation**:
    *   **Intent**: `query_customer_segment`
    *   **Entities**: `location: Germany`, `total_spent > 1000`
*   **Expected Action**: The system should filter the customer list to show only those located in Germany with a total purchase amount exceeding 1000 euros.

### Case 4: CLV for a Specific Customer
*   **User Query**: "What is the Customer Lifetime Value for customer ID 852?"
*   **Expected Interpretation**:
    *   **Intent**: `query_clv`
    *   **Entities**: `customer_id: 852`
*   **Expected Action**: The system should calculate and return the CLV for the specified customer using the predefined model.

### Case 5: Inactive Customers
*   **User Query**: "Which customers haven't made a purchase in the last 6 months?"
*   **Expected Interpretation**:
    *   **Intent**: `query_inactive_customers`
    *   **Entities**: `inactive_period: 6_months`
*   **Expected Action**: The system should identify all customers whose last purchase date is more than 6 months ago and return the list.

### Case 6: Sales Trend Visualization
*   **User Query**: "Generate a line chart of our monthly revenue for the past year."
*   **Expected Interpretation**:
    *   **Intent**: `visualize_data`
    *   **Entities**: `chart_type: line`, `metric: monthly_revenue`, `period: past_year`
*   **Expected Action**: The system should generate data for monthly revenue over the last 12 months and present it as a line chart.

### Case 7: Product Purchase Combination
*   **User Query**: "Find customers who bought 'Product A' but not 'Product B'."
*   **Expected Interpretation**:
    *   **Intent**: `query_customer_segment`
    *   **Entities**: `bought: Product A`, `not_bought: Product B`
*   **Expected Action**: The system should return a list of customers who have 'Product A' in their purchase history but not 'Product B'. (KAN-483)

### Case 8: Average Order Value
*   **User Query**: "What was the average order value for the 'Premium' customer segment in the last quarter?"
*   **Expected Interpretation**:
    *   **Intent**: `query_metric`
    *   **Entities**: `metric: average_order_value`, `segment: Premium`, `period: last_quarter`
*   **Expected Action**: The system should calculate the average value of all transactions made by customers in the 'Premium' segment during the previous quarter.

### Case 9: CLV Projection for a Segment
*   **User Query**: "Project the CLV for the 'Standard' segment over the next 12 months."
*   **Expected Interpretation**:
    *   **Intent**: `project_clv`
    *   **Entities**: `segment: Standard`, `projection_period: 12_months`
*   **Expected Action**: The system should calculate the projected CLV for the 'Standard' customer segment and visualize it. (KAN-486)

### Case 10: Simple Greeting
*   **User Query**: "Hello, how are you?"
*   **Expected Interpretation**:
    *   **Intent**: `greeting`
*   **Expected Action**: The system should respond with a polite, non-analytical greeting.
