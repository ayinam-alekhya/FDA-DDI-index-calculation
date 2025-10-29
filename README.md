# 💊 FDA DDI Index Calculation — Flask Web Application

This project is a **Flask-based web application** designed to evaluate **Acute Kidney Injury (AKI)** risks associated with **drug-drug interactions (DDI)**.  
It allows healthcare professionals and researchers to **upload Excel datasets**, perform **Reporting Odds Ratio (ROR)** and **Association Rule Mining (Apriori)** analyses, and compute a **Drug-Drug Interaction (DDI) Index** to understand how drug combinations may contribute to AKI.

---

## 📚 Overview

**Goal:**  
To create a web tool that identifies and quantifies the risk of Acute Kidney Injury (AKI) due to individual drugs and their combinations.

**Core Features:**
- Upload Excel files containing drug-reaction data
- Perform **ROR calculations** to evaluate associations
- Generate **association rules** using the **Apriori algorithm**
- Compute **Drug-Drug Interaction (DDI) Index**
- Present results (AKI counts, ROR values, DDI insights) in an interactive web interface

**Technologies Used:**
- **Flask** (Python web framework)
- **Pandas** for data analysis
- **NumPy** for numerical operations
- **HTML/CSS (Jinja2)** for frontend templates
- **Excel uploads (XLS/XLSX)** for input data

---

## 🧩 Project Structure

```
FDA_DDI_INDEX/
├── main.py                       # Flask application (core backend logic)
├── static/                       # CSS & static assets
│   └── styles.css
├── templates/                    # HTML templates rendered by Flask
│   ├── final.html
│   ├── index.html
│   ├── result.html
│   └── select_drug.html
├── uploads/                      # Folder for uploaded Excel files
│   ├── AKI_cases.xlsx
│   ├── arules.xlsx
│   ├── filtered_records_1.xlsx
│   └── Vancomycin_vancocin.xlsx
├── modules.xml / workspace.xml    # IDE configurations (ignore in Git)
├── FDA_DDI_index_calculation.pdf  # Project documentation paper
└── .gitignore                     # Ignored files and directories
```

---

## ⚙️ How It Works

### 1️⃣ Upload Excel Data
Users upload an `.xlsx` or `.xls` file containing columns such as:
- **Reactions**
- **Suspect Product Active Ingredients**
- **Suspect Product Names**
- **Concomitant Product Names**

### 2️⃣ Data Preprocessing
- Combines relevant columns into a unified `Combined Column`
- Converts text to lowercase for consistent matching

### 3️⃣ Drug Selection
- Users can choose up to **3 drugs** from the dataset
- The system generates all **possible combinations** and **permutations**

### 4️⃣ Filtering & Analysis
- Filters data to cases related to **Acute Kidney Injury (AKI)**
- Calculates:
  - Total AKI cases
  - AKI cases linked to each drug
  - Non-AKI cases
  - Cross-drug combinations

### 5️⃣ ROR Calculation
The **Reporting Odds Ratio (ROR)** is calculated as:

```
ROR = (n12 × n21) / (n22 × n11)
```
Where:
- `n11` = drug A alone with AKI  
- `n12` = drug A alone without AKI  
- `n21` = drug A + other compounds with AKI  
- `n22` = drug A + other compounds without AKI  

A higher ROR implies a stronger association between the drug and AKI.

### 6️⃣ Association Rule Mining
Uses the **Apriori algorithm** to discover patterns in drug usage and AKI occurrence.  
Generates rules like:
> “If drug A and drug B are taken together → higher likelihood of AKI.”

### 7️⃣ DDI Index
The **Drug-Drug Interaction Index** quantifies the interaction strength:
```
DDI Index = lift(drugA + drugB → AKI) / lift(drugA → AKI)
```
A higher DDI Index indicates a stronger synergistic effect.

---

## 🚀 Run the Application Locally

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/ayinam-alekhya/FDA-DDI-index-calculation.git
cd FDA-DDI-index-calculation

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install flask pandas numpy openpyxl
```

### Run the Flask App
```bash
python main.py
```
Then open your browser and visit:
```
http://127.0.0.1:5000/
```

---

## 🧪 Example Workflow

1. Open the app in your browser.  
2. Upload an Excel file with drug-reaction data.  
3. Select 1–3 drugs for analysis.  
4. View the generated results:
   - AKI and non-AKI case counts
   - ROR values
   - Association rules
   - DDI Index

---

## 📊 Output and Visualization

- Displays total AKI cases, ROR scores, and DDI index values.
- Presents summarized association rules in a readable format.
- Allows users to download or visualize results interactively.

---

## 📄 Reference Paper

For complete project documentation and methodology, see:  
📘 [`FDA DDI index calculation.pdf`](./FDA%20DDI%20index%20calculation.pdf)

---

## 👩‍💻 Contributors
- **Alekhya Ayinam** — Backend Development, Flask Integration, Data Analysis  
- **Bhavya Reddy Seerapu** — Frontend and Flask Template Design  
- **Vamsi Kummaragunta** — Data Analysis and Documentation  

---

## 🧭 Future Enhancements
- Integration of external APIs (e.g., OpenFDA) for live data retrieval  
- Interactive visualizations for AKI correlations  
- Improved UI/UX and responsive design  
- Expanded analysis for broader adverse drug reactions

---

## 🩺 Summary
This project delivers a practical and data-driven solution to analyze **drug-drug interactions** and their **potential AKI risks**.  
It combines statistical rigor (ROR) with machine learning (Apriori algorithm) in a lightweight Flask web interface—empowering healthcare professionals and researchers to make safer, data-informed medication decisions.
