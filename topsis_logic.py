
import pandas as pd
import numpy as np
import os
import time

def calculate_topsis(file_path, weights, impacts):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

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
    performance_score = s_worst / (s_best + s_worst)

    # Add to original dataframe
    original_df['Topsis Score'] = performance_score
    original_df['Rank'] = performance_score.rank(ascending=False)

    # Output filename
    output_filename = f"result_{int(time.time())}.csv"
    output_path = os.path.join('outputs', output_filename)
    
    # Save result
    original_df.to_csv(output_path, index=False)
    
    return output_path
