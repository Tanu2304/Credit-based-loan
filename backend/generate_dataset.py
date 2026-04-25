import pandas as pd
import numpy as np

np.random.seed(42)
N = 1000

employment = np.random.choice(["Salaried","Self-Employed","Business"], N, p=[0.55,0.30,0.15])
education  = np.random.choice(["Graduate","Postgraduate","Undergraduate"], N, p=[0.50,0.30,0.20])
gender     = np.random.choice(["Male","Female"], N, p=[0.65,0.35])
marital    = np.random.choice(["Married","Single"], N, p=[0.60,0.40])
loan_purpose = np.random.choice(["Home","Education","Personal","Business"], N)
property_area = np.random.choice(["Urban","Semi-Urban","Rural"], N, p=[0.40,0.35,0.25])
employer_cat  = np.random.choice(["Govt","Private","Self"], N, p=[0.25,0.55,0.20])

income      = np.random.randint(20000, 200000, N)
co_income   = np.random.randint(0, 80000, N)
age         = np.random.randint(21, 60, N)
dependents  = np.random.randint(0, 5, N)
credit_score= np.random.randint(300, 900, N)
exist_loans = np.random.randint(0, 5, N)
dti_ratio   = np.round(np.random.uniform(0.05, 0.65, N), 2)
savings     = np.random.randint(5000, 500000, N)
collateral  = np.random.randint(0, 2000000, N)
loan_amount = np.random.randint(50000, 5000000, N)
loan_term   = np.random.choice([12,24,36,48,60,84,120,180,240,360], N)

approved = (
    (credit_score > 650) &
    (dti_ratio < 0.40) &
    (income > loan_amount / (loan_term * 3)) &
    (exist_loans < 3)
).astype(int)
noise_idx = np.random.choice(N, size=int(N*0.08), replace=False)
approved[noise_idx] = 1 - approved[noise_idx]

df = pd.DataFrame({
    "Applicant_ID":      [f"APP{str(i).zfill(4)}" for i in range(N)],
    "Applicant_Income":  income,
    "Coapplicant_Income": co_income,
    "Employment_Status": employment,
    "Age":               age,
    "Marital_Status":    marital,
    "Dependents":        dependents,
    "Credit_Score":      credit_score,
    "Existing_Loans":    exist_loans,
    "DTI_Ratio":         dti_ratio,
    "Savings":           savings,
    "Collateral_Value":  collateral,
    "Loan_Amount":       loan_amount,
    "Loan_Term":         loan_term,
    "Loan_Purpose":      loan_purpose,
    "Property_Area":     property_area,
    "Education_Level":   education,
    "Gender":            gender,
    "Employer_Category": employer_cat,
    "Loan_Approved":     approved
})

df.to_csv("loan_data.csv", index=False)
print(f"Dataset created: {len(df)} rows | Approval rate: {approved.mean()*100:.1f}%")
