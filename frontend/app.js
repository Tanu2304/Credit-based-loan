const API_URL = "http://127.0.0.1:5000";

document.getElementById("loanForm").addEventListener("submit", async(e) => {
    e.preventDefault();
    const btn = document.getElementById("submitBtn");
    btn.disabled = true;
    btn.textContent = "⏳ Analyzing...";
    document.getElementById("errorBox").style.display = "none";
    document.getElementById("resultCard").style.display = "none";

    const getVal = (id) => {
        const el = document.getElementById(id);
        return el.tagName === "SELECT" ? el.value : parseFloat(el.value);
    };

    const payload = {
        Applicant_Income: getVal("Applicant_Income"),
        Coapplicant_Income: getVal("Coapplicant_Income"),
        Employment_Status: getVal("Employment_Status"),
        Age: getVal("Age"),
        Marital_Status: getVal("Marital_Status"),
        Dependents: getVal("Dependents"),
        Credit_Score: getVal("Credit_Score"),
        Existing_Loans: getVal("Existing_Loans"),
        DTI_Ratio: getVal("DTI_Ratio"),
        Savings: getVal("Savings"),
        Collateral_Value: getVal("Collateral_Value"),
        Loan_Amount: getVal("Loan_Amount"),
        Loan_Term: getVal("Loan_Term"),
        Loan_Purpose: getVal("Loan_Purpose"),
        Property_Area: getVal("Property_Area"),
        Education_Level: getVal("Education_Level"),
        Gender: getVal("Gender"),
        Employer_Category: getVal("Employer_Category")
    };

    try {
        const res = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        const badge = document.getElementById("resultBadge");
        badge.textContent = data.prediction === "Approved" ? "✅ LOAN APPROVED" : "❌ LOAN REJECTED";
        badge.className = "result-badge " + (data.prediction === "Approved" ? "approved-badge" : "rejected-badge");

        document.getElementById("confFill").style.width = data.approved_probability + "%";
        document.getElementById("confLabel").textContent = data.approved_probability.toFixed(1) + "% approval probability";
        document.getElementById("approvedProb").textContent = data.approved_probability + "%";
        document.getElementById("rejectedProb").textContent = data.rejected_probability + "%";

        const list = document.getElementById("factorList");
        list.innerHTML = "";
        (data.top_factors || []).forEach(f => {
            const li = document.createElement("li");
            li.textContent = f.replace(/_/g, " ");
            list.appendChild(li);
        });

        document.getElementById("resultCard").style.display = "block";
        document.getElementById("resultCard").scrollIntoView({ behavior: "smooth" });

    } catch (err) {
        const eb = document.getElementById("errorBox");
        eb.textContent = "⚠️ Error: " + err.message + ". Make sure Flask server is running on port 5000.";
        eb.style.display = "block";
    } finally {
        btn.disabled = false;
        btn.textContent = "🤖 Predict Loan Approval";
    }
});