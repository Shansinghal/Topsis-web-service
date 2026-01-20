import sys
import pandas as pd
import numpy as np

def error(msg):
    print("Error:", msg)
    sys.exit(1)

def main():
    # 1. Check number of arguments
    if len(sys.argv) != 5:
        error("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputFile>")

    input_file = sys.argv[1]
    weights = sys.argv[2].split(",")
    impacts = sys.argv[3].split(",")
    output_file = sys.argv[4]

    # 2. Read input file
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        error("Input file not found")

    # 3. Minimum 3 columns check
    if df.shape[1] < 3:
        error("Input file must contain at least three columns")

    # 4. Extract numeric data
    data = df.iloc[:, 1:]

    # 5. Check numeric values
    try:
        data = data.astype(float)
    except ValueError:
        error("Columns from 2nd to last must contain numeric values only")

    n_cols = data.shape[1]

    # 6. Weights & impacts length check
    if len(weights) != n_cols or len(impacts) != n_cols:
        error("Number of weights and impacts must match number of criteria columns")

    # 7. Validate impacts
    for imp in impacts:
        if imp not in ['+', '-']:
            error("Impacts must be either + or -")

    # Convert weights to float
    try:
        weights = np.array(weights, dtype=float)
    except:
        error("Weights must be numeric")

    # 8. Normalize
    norm = np.sqrt((data ** 2).sum())
    normalized = data / norm

    # 9. Apply weights
    weighted = normalized * weights

    # 10. Ideal best & worst
    ideal_best = []
    ideal_worst = []

    for i in range(n_cols):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # 11. Distances
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # 12. TOPSIS score
    score = dist_worst / (dist_best + dist_worst)

    # 13. Rank
    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False, method='dense').astype(int)

    # 14. Save output
    df.to_csv(output_file, index=False)
    print("TOPSIS analysis completed successfully.")

if __name__ == "__main__":
    main()
