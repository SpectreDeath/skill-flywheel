#!/usr/bin/env python3
"""
Data Analysis Skill

This skill provides data analysis capabilities including:
- Statistical analysis
- Data visualization
- Trend analysis
- Data cleaning and preprocessing
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def analyze_dataset(data: List[Dict[str, Any]], 
                   analysis_type: str = "comprehensive",
                   output_format: str = "json") -> Dict[str, Any]:
    "
    Analyze a dataset and provide insights
    
    Args:
        data: List of dictionaries representing the dataset
        analysis_type: Type of analysis ("basic", "statistical", "comprehensive")
        output_format: Output format ("json", "text", "detailed")
    
    Returns:
        Analysis results
    "
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        if df.empty:
            return {"error": "Empty dataset provided"}
        
        results = {
            "dataset_info": {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "data_types": {col: str(df[col].dtype) for col in df.columns}
            }
        }
        
        # Basic statistics
        if analysis_type in ["basic", "statistical", "comprehensive"]:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_columns:
                results["basic_stats"] = df[numeric_columns].describe().to_dict()
        
        # Statistical analysis
        if analysis_type in ["statistical", "comprehensive"]:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_columns:
                # Correlation analysis
                correlation_matrix = df[numeric_columns].corr()
                results["correlations"] = correlation_matrix.to_dict()
                
                # Outlier detection
                outliers = {}
                for col in numeric_columns:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outlier_count = len(df[(df[col] < lower_bound) | (df[col] > upper_bound)])
                    outliers[col] = outlier_count
                
                results["outliers"] = outliers
        
        # Data quality analysis
        if analysis_type == "comprehensive":
            # Missing values
            missing_values = df.isnull().sum().to_dict()
            results["missing_values"] = missing_values
            
            # Duplicate rows
            duplicate_count = df.duplicated().sum()
            results["duplicates"] = duplicate_count
            
            # Unique values analysis
            unique_values = {}
            for col in df.columns:
                unique_count = df[col].nunique()
                unique_values[col] = {
                    "unique_count": unique_count,
                    "unique_percentage": (unique_count / len(df)) * 100
                }
            results["unique_values"] = unique_values
        
        # Format output
        if output_format == "text":
            return _format_text_output(results)
        elif output_format == "detailed":
            return _format_detailed_output(results, df)
        else:
            return results
            
    except Exception as e:
        logger.error(f"Error in data analysis: {e}")
        return {"error": str(e)}

def _format_text_output(results: Dict[str, Any]) -> Dict[str, Any]:
    "Format results as text summary"
    summary = []
    
    # Dataset info
    info = results["dataset_info"]
    summary.append(f"Dataset contains {info['total_rows']} rows and {info['total_columns']} columns")
    summary.append(f"Columns: {', '.join(info['columns'])}")
    
    # Basic stats
    if "basic_stats" in results:
        summary.append("\nBasic Statistics:")
        for col, stats in results["basic_stats"].items():
            summary.append(f"  {col}: mean={stats.get('mean', 'N/A'):.2f}, std={stats.get('std', 'N/A'):.2f}")
    
    # Correlations
    if "correlations" in results:
        summary.append("\nCorrelations:")
        for col1, corr_dict in results["correlations"].items():
            for col2, corr_value in corr_dict.items():
                if col1 != col2 and abs(corr_value) > 0.5:
                    summary.append(f"  {col1} vs {col2}: {corr_value:.2f}")
    
    return {"summary": "\n".join(summary)}

def _format_detailed_output(results: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
    "Format results with additional detailed analysis"
    detailed = results.copy()
    
    # Add trend analysis for numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_columns:
        trends = {}
        for col in numeric_columns:
            if len(df) > 1:
                # Simple trend calculation (slope of linear regression)
                x = np.arange(len(df))
                y = df[col].fillna(df[col].mean())
                slope = np.polyfit(x, y, 1)[0]
                trends[col] = {
                    "trend_direction": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable",
                    "trend_strength": abs(slope)
                }
        
        detailed["trends"] = trends
    
    return detailed

def clean_data(data: List[Dict[str, Any]], 
              strategy: str = "drop", 
              fill_value: Any = None) -> List[Dict[str, Any]]:
    "
    Clean dataset by handling missing values and duplicates
    
    Args:
        data: List of dictionaries representing the dataset
        strategy: Strategy for handling missing values ("drop", "fill", "mean", "median", "mode")
        fill_value: Custom value for filling missing data (used when strategy="fill")
    
    Returns:
        Cleaned dataset
    "
    try:
        df = pd.DataFrame(data)
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        if strategy == "drop":
            df = df.dropna()
        elif strategy == "fill" and fill_value is not None:
            df = df.fillna(fill_value)
        elif strategy == "mean":
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        elif strategy == "median":
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        elif strategy == "mode":
            for col in df.columns:
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col] = df[col].fillna(mode_value[0])
        
        return df.to_dict('records')
        
    except Exception as e:
        logger.error(f"Error in data cleaning: {e}")
        return data

def generate_insights(data: List[Dict[str, Any]], 
                     target_column: str | None = None) -> Dict[str, Any]:
    "
    Generate business insights from the dataset
    
    Args:
        data: List of dictionaries representing the dataset
        target_column: Optional target column for predictive insights
    
    Returns:
        Business insights
    "
    try:
        df = pd.DataFrame(data)
        
        insights = {
            "data_quality": {},
            "patterns": [],
            "recommendations": []
        }
        
        # Data quality assessment
        total_rows = len(df)
        missing_total = df.isnull().sum().sum()
        insights["data_quality"]["completeness"] = (total_rows * len(df.columns) - missing_total) / (total_rows * len(df.columns)) * 100
        
        # Pattern detection
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_columns:
            # Detect high variance columns
            for col in numeric_columns:
                variance = df[col].var()
                if variance > df[col].mean() * 2:
                    insights["patterns"].append(f"High variance detected in {col}")
            
            # Detect potential outliers
            for col in numeric_columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                if len(outliers) > 0:
                    insights["patterns"].append(f"Outliers detected in {col} ({len(outliers)} records)")
        
        # Generate recommendations
        if insights["data_quality"]["completeness"] < 80:
            insights["recommendations"].append("Consider improving data collection to reduce missing values")
        
        if len(insights["patterns"]) > 0:
            insights["recommendations"].append("Investigate detected patterns for potential data quality issues")
        
        if target_column and target_column in df.columns:
            insights["recommendations"].append(f"Consider building predictive models using {target_column} as target")
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        return {"error": str(e)}

# Example usage function
def example_usage():
    """ Example of how to use the data analyzer skill """
    sample_data = [
        {"age": 25, "income": 50000, "score": 85},
        {"age": 30, "income": 60000, "score": 90},
        {"age": 35, "income": 70000, "score": 95},
        {"age": 40, "income": 80000, "score": 88},
        {"age": 45, "income": 90000, "score": 92},
    ]
    
    # Basic analysis
    result = analyze_dataset(sample_data, analysis_type="comprehensive")
    print("Analysis Result:", result)
    
    # Generate insights
    insights = generate_insights(sample_data, target_column="score")
    print("Insights:", insights)

if __name__ == "__main__":
    example_usage()


# --- invoke() wrapper added by batch fix ---
async def invoke(payload: dict) -> dict:
    "Entry point for skill invocation."
    import datetime as _dt
    action = payload.get("action", "analyze")
    timestamp = _dt.datetime.now().isoformat()

    actions_available = ["analyze", "clean", "insights", "get_info"]

    if action == "get_info":
        return {"result": {"name": "data-analyzer", "actions": actions_available}, "metadata": {"action": action, "timestamp": timestamp}}

    if action == "analyze":
        dataset = payload.get("dataset", [])
        if not dataset:
            return {"result": {"error": "No dataset provided"}, "metadata": {"action": action, "timestamp": timestamp}}
        result = analyze_dataset(dataset)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

    elif action == "clean":
        dataset = payload.get("dataset", [])
        result = clean_data(dataset)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

    elif action == "insights":
        dataset = payload.get("dataset", [])
        result = generate_insights(dataset)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

    else:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}


def register_skill() -> dict:
    """ Return skill metadata. """
    return {
        "name": "data_analyzer",
        "domain": "meta",
        "version": "1.0.0",
    }
