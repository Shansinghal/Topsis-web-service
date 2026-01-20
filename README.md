# TOPSIS-Based Decision Support System

## Project Description
This project implements the **TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) method to rank various funds based on multiple criteria. The goal is to identify the best fund by finding the one closest to the ideal positive solution and farthest from the ideal negative solution.

## Live Demo
Check out the live web service here: [TOPSIS Web Service](https://topsis-web-service-vzxs.onrender.com/)

## Methodology

The TOPSIS method follows these steps:

1. **Data Preprocessing**  
The dataset is loaded, and non-numeric columns (such as fund or alternative names) are separated from numeric criteria.

2. **Normalization**  
The decision matrix is normalized using vector normalization to handle different units of criteria:
r_ij = x_ij / sqrt( Σ(i=1 to m) (x_ij)^2 )


3. **Weighted Normalization**  
Each criterion is multiplied by its corresponding weight. In this assignment, equal weights were used:
v_ij = w_j × r_ij


4. **Ideal Solutions**
- **Positive Ideal Solution (PIS)**: Best values for each criterion  
  (Maximum for benefit criteria, Minimum for cost criteria)
- **Negative Ideal Solution (NIS)**: Worst values for each criterion  
  (Minimum for benefit criteria, Maximum for cost criteria)

5. **Separation Measures**  
The Euclidean distance of each alternative from the PIS (S⁺) and NIS (S⁻) is calculated.

6. **TOPSIS Score**  
The relative closeness to the ideal solution is computed as:
P_i = S_i⁻ / (S_i⁺ + S_i⁻)


7. **Ranking**  
Alternatives are ranked based on their TOPSIS scores in descending order.


## Result Table
The final output includes the Topsis Score and Rank for each fund. Below is a snapshot of the results (illustrative):

| Fund Name | Topsis Score | Rank |
| :--- | :--- | :--- |
| M1 | 0.534 | 4.0 |
| M2 | 0.490 | 6.0 |
| M3 | 0.448 | 8.0 |
| M4 | 0.638 | 2.0 |
| M5 | 0.570 | 3.0 |
| M6 | 0.518 | 5.0 |
| M7 | 0.485 | 7.0 |
| M8 | 0.675 | 1.0 |

*(Note: Actual values depend on the specific weights and impacts used in the notebook)*

## Result Graph
A bar chart is generated in the notebook to visualize the comparative performance of each fund. The fund with the highest bar represents the best alternative.

## Usage
1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    ```
2.  **Install dependencies**:
    ```bash
    pip install pandas numpy matplotlib
    ```
3.  **Run the Notebook**:
    Open `topsis_assignment.ipynb` in Jupyter Notebook, JupyterLab, or VS Code and execute the cells sequentially.
