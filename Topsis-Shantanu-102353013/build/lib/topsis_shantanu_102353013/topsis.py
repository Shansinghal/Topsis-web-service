import sys
import pandas as pd
import numpy as np
import os

def check_validity(input_file, weights, impacts):
    # Check if file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError("Input file not found.")

    # Read the data
    try:
        df = pd.read_csv(input_file)
    except Exception:
        raise Exception("Could not read input file. Ensure it is a valid csv.")

    # Check number of columns
    if df.shape[1] < 3:
        raise Exception("Input file must contain at least 3 columns.")

    # Numeric check
    df_numeric = df.iloc[:, 1:]
    if not np.issubdtype(df_numeric.dtypes.values.all(), np.number):
         # Try forcing to numeric to see if any non-numeric values exist
         try:
            df_numeric = df_numeric.astype(float)
         except ValueError:
            raise Exception("From 2nd to last column, all values must be numeric.")

    # Weights and impacts length check
    if len(weights) != df_numeric.shape[1]:
        raise Exception("Number of weights must match the number of numeric columns.")
        
    if len(impacts) != df_numeric.shape[1]:
        raise Exception("Number of impacts must match the number of numeric columns.")

    # Impacts validation
    if not all(i in ['+', '-'] for i in impacts):
        raise Exception("Impacts must be either '+' or '-'.")
        
    return df, df_numeric

def topsis(df, df_numeric, weights, impacts, result_file):
    
    normalized_df = df_numeric.copy()
    
    # Vector Normalization
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

    # Avoid division by zero
    total_score = s_best + s_worst
    # if any total_score is 0, handle it (though unlikely with S+ and S-)
    
    performance_score = s_worst / total_score

    df['Topsis Score'] = performance_score
    df['Rank'] = performance_score.rank(ascending=False)

    df.to_csv(result_file, index=False)
    print(f"Result file saved to {result_file}")

def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        print('Example: topsis data.csv "1,1,1,2" "+,+,-,+" result.csv')
        sys.exit(1)

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    result_file = sys.argv[4]

    try:
        weights = [float(w) for w in weights_str.split(',')]
        impacts = impacts_str.split(',')
        
        df, df_numeric = check_validity(input_file, weights, impacts)
        topsis(df, df_numeric, weights, impacts, result_file)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
