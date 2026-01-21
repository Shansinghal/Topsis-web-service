
import pandas as pd
import numpy as np
import os
import time

def calculate_topsis_score(df, weights, impacts):
    """
    Core TOPSIS calculation logic.
    Args:
        df (pd.DataFrame): The input dataframe.
        weights (list): List of weights.
        impacts (list): List of impacts ('+' or '-').
    Returns:
        pd.DataFrame: The dataframe with 'Topsis Score' and 'Rank' added.
    """
    # Drop columns that are not numeric for calculation (but keep them for output)
    original_df = df.copy()
    
    # Select only numeric columns
    df_numeric = df.select_dtypes(include=[np.number])
    
    if df_numeric.shape[1] < 2:
         raise Exception("Input file must contain at least 2 numeric columns.")

    if len(weights) != df_numeric.shape[1]:
        raise Exception(f"Number of weights ({len(weights)}) does not match number of numeric columns ({df_numeric.shape[1]}).")
    
    if len(impacts) != df_numeric.shape[1]:
        raise Exception(f"Number of impacts ({len(impacts)}) does not match number of numeric columns ({df_numeric.shape[1]}).")

    if not all(i in ['+', '-'] for i in impacts):
         raise Exception("Impacts must be either '+' or '-'.")

    # Vector Normalization
    normalized_df = df_numeric.copy()
    rss = np.sqrt((df_numeric**2).sum())
    
    # Avoid division by zero
    rss[rss == 0] = 1 
    
    normalized_df = normalized_df.div(rss)

    # Weighted Normalization
    weighted_df = normalized_df.mul(weights)

    # Ideal Best and Ideal Worst
    ideal_best = []
    ideal_worst = []

    for i, col in enumerate(weighted_df.columns):
        if impacts[i] == '+':
            ideal_best.append(weighted_df[col].max())
            ideal_worst.append(weighted_df[col].min())
        else:
            ideal_best.append(weighted_df[col].min())
            ideal_worst.append(weighted_df[col].max())

    # Euclidean Distance
    s_best = np.sqrt(((weighted_df - ideal_best)**2).sum(axis=1))
    s_worst = np.sqrt(((weighted_df - ideal_worst)**2).sum(axis=1))

    # Performance Score
    # Handle division by zero if s_best + s_worst is 0
    total_distance = s_best + s_worst
    performance_score = np.divide(s_worst, total_distance, out=np.zeros_like(s_worst), where=total_distance!=0)

    # Add to original dataframe
    original_df['Topsis Score'] = performance_score
    original_df['Rank'] = performance_score.rank(ascending=False)
    
    return original_df

def calculate_topsis(file_path, weights, impacts, output_dir='outputs'):
    """
    Wrapper for file handling and TOPSIS calculation.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

    result_df = calculate_topsis_score(df, weights, impacts)

    # Output filename
    output_filename = f"result_{int(time.time())}.csv"
    
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Save result
    result_df.to_csv(output_path, index=False)
    
    return output_path
