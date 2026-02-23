# KAN-493: Performance Test Scenarios

This document defines the scenarios for performance testing the Customer Analysis Conversational Agent. The goal is to ensure the system is responsive, stable, and scalable under realistic load conditions.

## 1. Objectives

*   Identify performance bottlenecks in critical transactions.
*   Establish a baseline for key performance metrics (response time, throughput).
*   Validate that the system meets the non-functional requirements defined in the user stories.
*   Ensure the logging and caching systems do not introduce significant performance overhead.

## 2. Critical Transactions

The following user actions have been identified as critical and will be the focus of our performance tests:

1.  **Chat Message (Simple Query)**: A simple data lookup (e.g., "What are total sales?").
2.  **Chat Message (Complex Query)**: A query involving segmentation and aggregation (e.g., "Show me sales by country for customers who spent > 1000").
3.  **Chat Message (Visualization)**: A query that results in a chart (e.g., "Draw a bar chart of sales by country").
4.  **CLV Calculation (Single)**: Calculating CLV for one customer.
5.  **CLV Calculation (Batch)**: Calculating CLV for a large segment of 1000 customers (KAN-492).

## 3. Performance Metrics & Thresholds

| Metric                  | Threshold                                       | Story Reference |
| ----------------------- | ----------------------------------------------- | --------------- |
| Avg. Response Time (API)| < 2 seconds under load                          | KAN-495         |
| CLV Calculation (Single)| < 500ms                                         | KAN-485         |
| CLV Calculation (Batch) | < 5 minutes for 1000 customers                  | KAN-492         |
| Drill-Down (Segment)    | < 2 seconds for 1000 customers                  | KAN-482         |
| Segmentation (Batch)    | < 5 seconds for 10,000 customers                | KAN-480         |
| Error Rate              | < 1% under load                                 | General         |
| Logging Overhead        | < 5% increase in average response time          | KAN-465         |

## 4. Test Scenarios

### Scenario 1: Load Test (KAN-494)

*   **Objective**: To measure system performance under expected peak load.
*   **Load Profile**:
    *   Simulate 50 concurrent users.
    *   Ramp-up period: 2 minutes.
    *   Duration: 10 minutes.
    *   User Behavior: Users will execute a mix of the critical transactions defined above, with a think time of 5-10 seconds between requests.
*   **Expected Outcome**:
    *   The system remains stable with an error rate below 1%.
    *   Average response times for all transactions stay within their defined thresholds.
    *   CPU and Memory usage on the server remain below 80%.

### Scenario 2: Stress Test (KAN-494)

*   **Objective**: To identify the system's breaking point and how it behaves under extreme load.
*   **Load Profile**:
    *   Start with 50 concurrent users.
    *   Incrementally increase the number of users by 10 every minute until the system's response time degrades by more than 100% or the error rate exceeds 5%.
*   **Expected Outcome**:
    *   Identify the maximum number of concurrent users the system can handle.
    *   Document the system's failure mode (e.g., high response times, 5xx errors, crashes).
    *   This information will be used to define scaling policies.

### Scenario 3: Cache Effectiveness Test (KAN-490)

*   **Objective**: To validate the performance improvement provided by the caching layer.
*   **Test Steps**:
    1.  Disable the Redis cache.
    2.  Run a test with 10 users for 5 minutes, repeatedly requesting the same complex query (e.g., "top 5 products last year"). Record the average response time.
    3.  Enable the Redis cache and clear it.
    4.  Run the exact same test again.
*   **Expected Outcome**:
    *   The average response time in step 4 should be significantly lower (at least 80% reduction) than in step 2.
    *   The 'cache hit' metric should be high after the first request.
    *   The database load should be significantly lower during the second run.

### Scenario 4: Batch Processing Test (KAN-492)

*   **Objective**: To verify the performance of large-scale data processing tasks.
*   **Test Steps**:
    1.  Prepare a dataset with 1,000 customers for a specific segment.
    2.  Trigger the batch CLV calculation for this segment.
    3.  Measure the total execution time from start to finish.
    4.  Monitor memory and CPU usage during the process.
*   **Expected Outcome**:
    *   The entire process completes in under 5 minutes.
    *   Memory usage does not spike excessively and remains within acceptable limits.
