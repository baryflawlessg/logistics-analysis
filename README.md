# Delivery Failure Root Cause Analysis System

## Overview

This system analyzes delivery failures by aggregating data from multiple sources to provide actionable insights and root cause analysis. It's designed to transform reactive problem-solving into proactive operational excellence.

## Features

- **Multi-Domain Data Aggregation**: Orders, fleet logs, warehouse records, external factors, customer feedback
- **Automated Correlation**: Links events across different data sources
- **Root Cause Analysis**: Identifies patterns and failure reasons
- **Human-Readable Insights**: Generates narrative explanations
- **Actionable Recommendations**: Suggests specific operational improvements
- **6 Sample Use Cases**: Pre-built analysis functions for common scenarios

## Sample Use Cases

1. **City-Specific Delays**: "Why were deliveries delayed in city X yesterday?"
2. **Client Failures**: "Why did Client X's orders fail in the past week?"
3. **Warehouse Performance**: "Explain the top reasons for delivery failures linked to Warehouse B?"
4. **City Comparison**: "Compare delivery failure causes between City A and City B?"
5. **Festival Risks**: "What are the likely causes of delivery failures during festival periods?"
6. **Scaling Risks**: "What risks should we expect with additional monthly orders?"

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Sample data files in `sample-files/` folder

### Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify sample data** is in the `sample-files/` folder:
   - clients.csv
   - drivers.csv
   - external_factors.csv
   - feedback.csv
   - fleet_logs.csv
   - orders.csv
   - warehouse_logs.csv
   - warehouses.csv

### Running the Demo

**Option 1: Run all use cases automatically**
```bash
python demo_analysis.py
```

**Option 2: Interactive mode**
```bash
python demo_analysis.py --interactive
```

**Option 3: Run individual analysis**
```python
from delivery_failure_analyzer import DeliveryFailureAnalyzer

analyzer = DeliveryFailureAnalyzer()
analyzer.load_all_data()

# Analyze city delays
result = analyzer.analyze_city_delays("Chennai", "2025-08-15")
print(result)
```

## File Structure

```
Shipping/
├── sample-files/                 # Sample CSV data files
│   ├── clients.csv
│   ├── drivers.csv
│   ├── external_factors.csv
│   ├── feedback.csv
│   ├── fleet_logs.csv
│   ├── orders.csv
│   ├── warehouse_logs.csv
│   └── warehouses.csv
├── delivery_failure_analyzer.py  # Main analysis engine
├── demo_analysis.py              # Demo script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── Delivery_Failure_Analysis_Solution.md  # Detailed solution document
└── Solution_Architecture_Diagram.md       # Architecture diagram
```

## How It Works

### 1. Data Loading
- Loads all CSV files from the `sample-files/` folder
- Converts date columns to proper datetime format
- Creates SQLite database for complex queries

### 2. Analysis Engine
- **Correlation Engine**: Links events across different data sources
- **Pattern Detection**: Identifies failure patterns and root causes
- **Insight Generation**: Creates human-readable explanations
- **Recommendation Engine**: Suggests actionable improvements

### 3. Output Generation
- JSON files with detailed analysis results
- Human-readable insights and recommendations
- Performance metrics and statistics

## Sample Output

```json
{
  "city": "Chennai",
  "total_orders": 45,
  "failed_orders": 8,
  "failure_rate": 17.8,
  "insights": [
    "Primary failure reason: Stockout",
    "Warehouse inventory management needs improvement",
    "External factors significantly impact delivery performance"
  ],
  "recommendations": [
    "Implement real-time inventory tracking and automated reorder systems",
    "Deploy dynamic routing software with real-time traffic data"
  ]
}
```

## Customization

### Adding New Analysis Functions

```python
def analyze_custom_metric(self, parameter):
    """Custom analysis function."""
    # Your analysis logic here
    return {
        "metric": "value",
        "insights": ["insight1", "insight2"],
        "recommendations": ["rec1", "rec2"]
    }
```

### Modifying Data Sources

To use your full dataset instead of sample files:

1. Replace files in `sample-files/` folder with your full CSV files
2. Ensure column names match the expected format
3. Run the analysis as usual

### Database Queries

The system creates a SQLite database (`delivery_analysis.db`) for complex queries:

```python
# Access the database directly
import sqlite3
conn = sqlite3.connect('delivery_analysis.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM orders WHERE status = 'Failed'")
results = cursor.fetchall()
```

## Troubleshooting

### Common Issues

**1. "No module named 'pandas'"**
```bash
pip install pandas numpy matplotlib seaborn
```

**2. "File not found" errors**
- Ensure `sample-files/` folder exists
- Check that all CSV files are present
- Verify file names match exactly

**3. "No data found" in analysis**
- Check if your sample data has records for the requested parameters
- Verify date formats in your CSV files
- Ensure city/client/warehouse names match exactly

**4. Database errors**
- Delete `delivery_analysis.db` and run again
- Check file permissions in the directory

### Getting Help

1. **Check the logs**: The system prints detailed information about what it's doing
2. **Verify data**: Ensure your CSV files have the expected structure
3. **Test with sample data**: Start with the provided sample files
4. **Run individual functions**: Test one analysis function at a time

## Scaling to Full Dataset

When you're ready to use your full dataset:

1. **Backup sample files** (optional)
2. **Replace CSV files** in `sample-files/` with your full data
3. **Verify column names** match the expected format
4. **Test with a small subset** first
5. **Run full analysis** when ready

The system is designed to handle larger datasets efficiently using pandas and SQLite.

## Performance Tips

- **Memory usage**: For very large datasets, consider processing in chunks
- **Database optimization**: SQLite automatically creates indexes for better performance
- **Parallel processing**: Can be added for multiple simultaneous analyses

## Next Steps

1. **Run the demo** to see the system in action
2. **Review the generated JSON files** for detailed results
3. **Modify parameters** to test different scenarios
4. **Add custom analysis functions** for your specific needs
5. **Scale to your full dataset** when ready

## Support

This system is designed to be self-contained and easy to use. The code is well-commented and includes error handling for common issues.

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Test with sample data first before using full dataset
