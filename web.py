# Importing the dependencies
import spacy
import streamlit as st
from spacy.matcher import PhraseMatcher
from streamlit_option_menu import option_menu
import pdfplumber 
import time
import requests
from bs4 import BeautifulSoup
import tensorflow as tf
import transformers
from transformers import T5Tokenizer,TFT5ForConditionalGeneration

pretrained_model='t5-base'
tokenizer=T5Tokenizer.from_pretrained(pretrained_model)
model=TFT5ForConditionalGeneration.from_pretrained(pretrained_model)
    

# Loading the model
nlp=spacy.load("en_core_web_sm")

# Initializing the PhraseMatcher
matcher=PhraseMatcher(vocab=nlp.vocab,attr='Lower')

# Defining the Risc_Keywords 
risky_keywords = {
    "Data Privacy Risk": [
        "privacy policy", "personal data", "GDPR", "data breach", "data sharing",
        "data collection", "data processing", "tracking", "cookies", "compliance",
        "third-party access", "data retention", "transfer of data", "cross-border data",
        "confidential information", "CCPA", "data security", "encryption", "processing activities",
        "data collection", "data sharing", "privacy", "confidentiality", "personal data",
        "data protection", "third-party access", "user data"
    ],
    "Liability Risk": [
        "limitation of liability", "no liability", "indemnification", "hold harmless",
        "third-party claims", "no responsibility", "exclusion of liability",
        "indirect damages", "consequential damages", "loss of profit", "liability cap",
        "liquidated damages", "liability", "damages", "indemnify", "indemnification",
        "consequential damages", "no responsibility",
         "compensation", "not liable","disclaimer", "exclusions", "liability cap"
    ],
    "Termination Risk": [
        "termination for convenience", "immediate termination", "without notice",
        "early termination", "suspend services", "discontinue", "cancellation",
        "non-renewal", "renewal terms", "automatic renewal", "exit fees", "terminate",
        "termination", "without notice", "breach", "suspension", "cancel","immediate termination",
        "suspend", "discontinue", "termination rights", "breach","termination for cause",
        "termination for convenience"
    ],
    "Intellectual Property Risk": [
        "intellectual property", "ownership", "license to use", "infringement",
        "IP rights", "proprietary information", "trademark", "patent",
        "copyright", "assignment of rights", "license restrictions"
    ],
    "Payment or Financial Risk": [
        "non-refundable", "late payment", "interest on late payment",
        "price increase", "additional charges", "fees", "billing", "subscription fees",
        "taxes", "payment terms", "currency exchange", "pricing changes",
        "overdue payment", "credit risk", "surcharges", "charges", "remuneration", "penalty", "non-refundable"
    ],
    "Service Level Agreement (SLA) Risk": [
        "no SLA", "uptime", "downtime", "service credits", "performance penalties",
        "service interruptions", "response time", "service level agreement",
        "failure to perform", "failure of service", "performance guarantee", "reliability"
    ],
    "Governing Law and Jurisdiction Risk": [
        "jurisdiction", "governing law", "dispute resolution", "arbitration",
        "mediation", "legal venue", "applicable law", "court", "choice of law",
        "enforceability", "exclusive jurisdiction", "venue", "legal compliance"
    ],
    "Force Majeure Risk": [
        "force majeure", "unforeseen events", "acts of God", "natural disaster",
        "pandemic", "war", "civil unrest", "labor strike", "riots", "excuse from performance",
        "failure of suppliers", "economic downturn", "government regulations"
    ],
    "Confidentiality Risk": [
        "disclosure", "non-disclosure", "confidentiality agreement", "proprietary information",
        "breach of confidentiality", "NDA", "sensitive data", "unauthorized access",
        "confidential information", "confidential", "non-disclosure", "privacy", "proprietary information",
        "trade secret"
    ],
    "Warranty Risk": [
        "warranty", "warranties", "guarantee", "disclaimer", "as is", "merchantability"
    ],
    "Third-Party Obligations Risk": [
        "subcontractors", "third-party services", "outsourcing", "affiliates", "third-party vendors"
    ],
    "Compliance Risk": [
        "compliance", "regulatory requirements", "legal obligations", "audit", "reporting requirements"
    ],
    "Indemnity Risk": [
        "indemnity", "indemnification", "hold harmless", "defend", "third-party claims","claims", "legal fees"
    ],
    "Modification of Terms Risk": [
        "modify terms", "change terms", "update policies","amend", "notification of changes", "without prior notice",
        "at any time"
    ],
    "Auto-Renewal Risk": [
        "auto-renew", "automatic renewal", "renewal terms", "continuous subscription"
    ],
    "Usage Restrictions Risk": [
        "prohibited uses", "restrictions", "unauthorized access", "no commercial use", "user conduct"
    ],
    "License Scope Risk": [
        "Non-transferable", "revocable", "limited license"
    ],
    "Age Restrictions Risk": [
        "minimum age", "age requirement", "must be at least"
    ],
    "Prohibited Users Risk": [
        "prohibited from using", "restricted access", "banned users"
    ],
    "Geographic Restrictions Risk": [
        "geographic eligibility", "restricted countries"
    ]
}

# Defining the coreeponding causes for the keywords
causes = {
    "DATA PRIVACY RISK": [
        "Data privacy risk include inadequate data protection measures, unauthorized access, lack of user consent, data breaches, and non-compliance with privacy regulations, leading to the exposure of sensitive personal information."
    ],
    "LIABILITY RISK": [
        "Liability risk arises when companies limit their responsibility for damages, losses, or legal claims through clauses that cap or exclude liability for indirect, incidental, or consequential damages, shifting significant financial and legal burdens onto the user."
    ],
    "TERMINATION RISK": [
        "Termination clauses that allow a company to end a contract for vague reasons like sole discretion or without clear cause create uncertainty for the user, potentially leading to unexpected service disruptions or financial losses."
    ],
    "INTELLECTUAL PROPERTY RISK": [
        "Intellectual property risk arises when users unknowingly infringe on proprietary rights, fail to properly license, misuse copyrighted material, or violate patents and trademarks associated with the service."
    ],
    "PAYMENT OR FINANCIAL RISK": [
        "Payment or financial risk is caused by clauses that allow for unexpected price changes, additional fees, unclear billing practices, or penalties for late payments, which can lead to unforeseen financial obligations for the user."
    ],
    "SERVICE LEVEL AGREEMENT (SLA) RISK": [
        "Causes of Service Level Agreement (SLA) risk include unclear performance metrics, lack of defined penalties for non-compliance, inadequate service availability guarantees, ambiguous response times for issues, and insufficient monitoring or reporting mechanisms, all of which can lead to unmet expectations and disputes between the service provider and the client."
    ],
    "GOVERNING LAW AND JURISDICTION RISK": [
        "The governing law or jurisdiction risk arises when disputes must be settled in a legal system unfamiliar to the user, potentially leading to higher legal costs, delays, and disadvantageous rulings, particularly if the jurisdiction is outside the user's home country, such as requiring Indian businesses to litigate in foreign courts."
    ],
    "FORCE MAJEURE RISK": [
        "Force majeure risk can be caused by unforeseen events or circumstances beyond the control of the parties involved, such as natural disasters, war, terrorism, pandemics, labor strikes, government actions, or other disruptions that prevent the fulfillment of contractual obligations."
    ],
    "CONFIDENTIALITY RISK": [
        "Confidentiality risk arises from inadequate data protection measures, unauthorized access, mishandling of sensitive information, lack of employee training on data privacy, and unclear contractual obligations regarding the safeguarding of proprietary or personal data."
    ],
    "WARRANTY RISK": [
        "Warranty Risk refer to circumstances or events that may lead to a breach of warranty, such as misrepresentations about product quality or performance, failure to disclose defects, or changes in regulatory standards, potentially resulting in financial loss or legal disputes for the buyer."
    ],
    "THIRD-PARTY OBLIGATIONS RISK": [
        "Causes of third-party obligations risk arise when a company relies on external vendors or partners to fulfill contractual responsibilities, potentially leading to compliance issues, service interruptions, or liability due to the third parties' failure to meet their commitments."
    ],
    "COMPLIANCE RISK": [
        "Compliance risk can arise from factors such as inadequate understanding of regulations, failure to implement effective internal controls, lack of employee training, insufficient monitoring of compliance activities, changes in laws or regulations, and operational complexities that hinder adherence to legal requirements."
    ],
    "INDEMNITY RISK": [
        "Indemnity risk arises when a user is held responsible for legal claims, losses, or damages resulting from their actions or use of a service, potentially leading to significant financial liabilities or legal costs."
    ],
    "MODIFICATION OF TERMS RISK": [
        "The risk of modification of terms arises from a company's unilateral right to change the agreement at any time without prior notice, which can lead to unexpected obligations or service disruptions for users."
    ],
    "AUTO-RENEWAL RISK": [
        "Auto-renewal risk arises when users are automatically charged for a subscription or service without explicit consent or awareness, potentially leading to unexpected financial obligations and difficulties in cancellation."
    ],
    "USAGE RESTRICTIONS RISK": [
        "Usage restrictions risk can arise from factors such as age limitations, legal capacity requirements, compliance with regional laws, prohibited user designations, and geographic constraints that collectively limit who can access and utilize a service."
    ],
    "LICENSE SCOPE RISK": [
        "The causes of license scope risk include restrictive licensing terms that limit the user's ability to transfer, share, or use the software freely, as well as the potential for unilateral changes or revocation of the license by the provider without prior notice or consent."
    ],
    "AGE RESTRICTIONS RISK": [
        "Age restrictions risk arises from the need to protect minors from potential harm or liability associated with using certain services, ensuring compliance with legal regulations that require users to meet a minimum age threshold."
    ],
    "PROHIBITED USERS RISK": [
        "The risk of prohibited users arises from factors such as prior violations of terms, legal restrictions (such as sanctions or criminal records), non-compliance with age or eligibility requirements, or geographical limitations that disqualify certain individuals or entities from accessing the service."
    ],
    "GEOGRAPHIC RESTRICTIONS RISK": [
        "Geographic restrictions risk arises from varying legal, regulatory, and compliance requirements across different regions, which may limit access to the service based on the user's location or expose the company to legal liabilities in jurisdictions where it is not authorized to operate."
    ]
}

# Adding words to matcher (adding pattrens)
for risc_category,words in risky_keywords.items():
    w=[nlp(word) for word in words]
    matcher.add(risc_category.upper(),w)
    
# Function for finding the summary of the text
def finding_summary(t):
    tokenized_text=tokenizer(t,padding=True,Truncation=True,return_tensors="tf")
    generated_ids=model.generate(tokenized_text['input_ids'],max_length=1000, num_beams=4,early_stopping=True)
    generated_summary=tokenizer.decode(generated_ids[0],skip_special_tokens=True)
    return generated_summary
    
    
# Function for text analysis
def text_analysis(text):
    
    doc=nlp(text)
    matches=matcher(doc)
    matched_categiries=[]
    
    if(matches):
        for match_id,start,end in matches:
            found_category=nlp.vocab.strings[match_id]
            if found_category not in matched_categiries:
                matched_categiries.append(found_category)
                matched_word=doc[start:end]
                
                summary=finding_summary(text)
                
                with st.expander(f"Risc Category: {found_category.upper()}"):
                    st.write(f"Sentence: {text}")
                    st.write(f"Summary: {summary}")
                    st.write(f"Matched Text: {matched_word}")
                    st.write(f"Cause: {causes[found_category.upper()][0]}")
    

# Title for 1st page
st.title('Terms and conditions RisK Analyzer')

# For sidebar menu
with st.sidebar:
    selected=option_menu("Choose an option to upload",['PDF','URL','TEXT'],icons=['file-earmark-pdf-fill','link','chat-square-text-fill'])

# If PDF option is selected
if(selected=='PDF'):
    uploaded_file=st.file_uploader('Choose your .pdf file',type="pdf")
    
    if(st.button('Analyze T&C')):
        if(uploaded_file!=None):
            with pdfplumber.open(uploaded_file) as pdf:
                text=""
                
                with st.spinner("Analyzing T&C...."):
                    time.sleep(1)
                    
                for page,context in enumerate(pdf.pages):
                    text=context.extract_text()
                    splitte=text.split(".")
                    
                    for j in splitte:
                        if not j.endswith("."):
                            j+="."
                        text_analysis(j)
                        
        else:
            st.info("Please Upload the .pdf file to Analyze")
            
# If TEXT option is selected
if(selected=='TEXT'):
    txt=st.text_area("Enter the Terms and Conditions",height=175)
    if(st.button('Analyze T&C')):
        if(txt!=''):
            with st.spinner('Analyzing T&C...'):
                time.sleep((1))
            splitted=txt.split(".")
            for i in splitted:
                if not i.endswith("."):
                    i+="."
                    
                text_analysis(i)
            
        else:
            st.info('Please Enter the Terms and Conditions to Analyze')
    
# If URL option is selected
if(selected=='URL'):
    link=st.text_input("Enter the URL link")
    st.write(link)
    if(st.button('Analyze T&C')):
        if(link):
            res=requests.get(link)
            html_content=res.content
            soup=BeautifulSoup(html_content,'html.parser')
            
            for element in soup.find_all(["p", "h1", "h2", "h3"]):
                extracted_element=element.get_text().strip()
                
                if extracted_element and not extracted_element.endswith("."):
                    extracted_element+='.'
                    
                text_analysis(extracted_element)
            
        else:
            st.info('PLease Enter the URL link to analyze')
