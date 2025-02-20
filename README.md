# Terms and Conditions Risk Analyzer

## Overview
The **Terms and Conditions Risk Analyzer** is a web-based tool designed to help businesses and individuals analyze Terms and Conditions (T&Cs) to identify potential risks. The tool leverages **Natural Language Processing (NLP)** and **keyword matching** to scan legal contracts for critical clauses that may introduce **legal, financial, or operational risks** for the user.

Additionally, it provides a **summarization feature** to generate a concise summary of the T&Cs, highlighting key aspects without requiring users to read the full contract.

## Features

### 🔹 Multiple Input Formats:
- **📄 PDF Upload**: Upload a PDF version of the terms and conditions.
- **🔗 URL Input**: Provide a URL link to a webpage containing the terms and conditions.
- **📋 Text Input**: Directly paste the text of the terms and conditions.

### 🔹 Risk Categorization:
The tool identifies and categorizes risks into the following categories:

-  **Data Privacy Risk**
-  **Liability Risk**
-  **Termination Risk**
-  **Intellectual Property Risk**
-  **Payment or Financial Risk**
-  **Service Level Agreement (SLA) Risk**
-  **Governing Law and Jurisdiction Risk**
-  **Force Majeure Risk**
-  **Confidentiality Risk**
-  **Warranty Risk**
-  **Third-Party Obligations Risk**
-  **Compliance Risk**
-  **Indemnity Risk**
-  **Modification of Terms Risk**
-  **Auto-Renewal Risk**
-  **Usage Restrictions Risk**
-  **License Scope Risk**
-  **Age Restrictions Risk**
-  **Prohibited Users Risk**
-  **Geographic Restrictions Risk**

### 🔹 Interactive UI:
- **Sidebar** for input options: Upload PDF, enter URL, or paste text.
- **Expandable sections** explain detected risk categories, causes and the summary of the text.
- **Highlighted matched text** for better risk visualization.

### 🔹 Keyword Matching with NLP:
- Uses **spaCy's PhraseMatcher** to detect risk-related keywords and phrases.
- Provides **explanations** for identified risks and highlights the **exact phrases** that triggered the detection.

### 🔹 Summarization Feature:
- Uses fine-tuned transformer model to generate a **concise summary** of the Terms and Conditions.
- Extracts key points without requiring users to read the entire document.

### 🔹 Performance Optimization:
- **Fast text extraction** from PDFs and web pages using **pdfplumber** and **BeautifulSoup**.
- **Streamlit-powered UI** for a **user-friendly** experience.

---

## Example Usage
1. Choose an option from the sidebar:
   - **PDF**: Upload a PDF containing the SaaS Terms and Conditions.
   - **URL**: Enter the URL of a webpage with the SaaS Terms and Conditions.
   - **Text**: Paste the Terms and Conditions in the provided text area.
2. Click on the "Analyze T&C" button to start the analysis.
3. The tool will:
   - **Identify risk categories** and causes.
   - **Highlight matched text** for each risk.
   - **Provide a summary** of the Terms and Conditions.
