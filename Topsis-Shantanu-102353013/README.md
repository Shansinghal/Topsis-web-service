# Topsis-Shantanu-102353013

A Python package to implement the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) decision-making algorithm.

## Installation

```bash
pip install Topsis-Shantanu-102353013
```

## Usage

This package can be used via the command line.

### Command Line Interface

```bash
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

#### Arguments:
1.  **InputDataFile**: Path to the input CSV file.
    -   The first column should contain the object/alternative names (e.g., Fund Name, Model Name).
    -   From the 2nd to the last column, the file must contain **numeric** values.
2.  **Weights**: A comma-separated string of weights (e.g., "1,1,1,2").
3.  **Impacts**: A comma-separated string of impacts, either '+' or '-' (e.g., "+,+,-,+").
4.  **ResultFileName**: The name of the output CSV file to save the results.

### Example

```bash
topsis data.csv "1,1,1,1" "+,+,+,+" result.csv
```

## Output

The output file will contain the original data with two additional columns:
-   **Topsis Score**: The calculated performance score.
-   **Rank**: The rank of the alternative.

## License

This project is licensed under the MIT License.
