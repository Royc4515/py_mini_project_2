# MiniProject 2: Event-Related Potential (ERP) Analysis

## Overview
This project calculates the **Event-Related Potential (ERP)** for finger movements using ECoG (Electrocorticography) data. It implements a robust pipeline to align continuous brain signals with discrete movement events, averaging them to reveal the characteristic brain response for each of the five fingers.

## Project Structure
* **`src/erp.py`**: Core logic. Implements `calc_mean_erp` using vectorized NumPy operations for signal averaging.
* **`main.py`**: Execution script. Handles file I/O, validation, and visualization.
* **`mini_project_2_data/`**: Directory for input CSV files.

## Methodology
The analysis follows the strict logic defined in the course specifications:
1.  **Windowing**: Extracts a time block from **-200ms to +1000ms** relative to movement onset.
2.  **Filtering**: Validates trial indices to ensure they fall within recording bounds.
3.  **Averaging**: Groups valid trials by finger ID (1-5) and computes the mean signal across trials.
4.  **Output**: Generates a `5x1201` matrix (`fingers_erp_mean`) and visualizes the ERP waveforms.

## How to Run
python main.py

### Prerequisites
* Python 3.8+
* NumPy, Pandas, Matplotlib

### Installation
```bash
pip install numpy pandas matplotlib
