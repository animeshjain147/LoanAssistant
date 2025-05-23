import streamlit as st
import google.generativeai as genai
from googletrans import Translator
from datetime import datetime, date
import math

# Configure Google Generative AI
API_KEY = "AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Translator
translator = Translator()

# Function to get AI response
def get_ai_response(prompt, language="en"):
    try:
        response = model.generate_content(prompt)
        if response.text:
            translated_response = translate_text(response.text, language)
            return translated_response
        return "Error: No response from the AI model."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to translate text
def translate_text(text, dest_language="en"):
    try:
        if text.strip():  # Ensure text is not empty
            translated_text = translator.translate(text, dest=dest_language).text
            return translated_text
        return "No text provided for translation."
    except Exception as e:
        return f"Translation Error: {str(e)}"

# Function to calculate EMI
def calculate_emi(loan_amount, interest_rate, tenure):
    # Convert interest rate from percentage to monthly decimal
    monthly_interest_rate = (interest_rate / 12) / 100
    # Convert tenure from years to months
    tenure_months = tenure * 12
    # EMI formula
    emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure_months) / ((1 + monthly_interest_rate) ** tenure_months - 1)
    return emi

# Function to generate EMI details
def generate_emi_details(loan_amount, interest_rate, tenure, language_code):
    emi = calculate_emi(loan_amount, interest_rate, tenure)
    total_payment = emi * tenure * 12
    total_interest = total_payment - loan_amount

    emi_details = (
        f"EMI: ₹{emi:.2f}\n"
        f"Total Interest Payable: ₹{total_interest:.2f}\n"
        f"Total Payment (Principal + Interest): ₹{total_payment:.2f}"
    )
    return translate_text(emi_details, language_code)

# Function to check loan sanction eligibility (multilingual)
def check_loan_sanction(income, loan_amount, tenure, language_code):
    if income <= 0 or loan_amount <= 0 or tenure <= 0:
        return translate_text("Insufficient data provided.", language_code)
    if loan_amount > income * tenure * 12 * 0.5:
        return translate_text("Loan amount is too high relative to income and tenure.", language_code)
    if income < 20000:
        return translate_text("Income is below the minimum threshold.", language_code)
    return translate_text("Loan can likely be sanctioned.", language_code)

# Function to display loan application guidance
def display_loan_guidance(language_code):
    guidance_prompt = f"Provide a brief guide on the loan application process, including required documents, in {language_code}."
    guidance_response = get_ai_response(guidance_prompt, language_code)
    st.sidebar.write(translate_text("**Loan Application Guidance:**", language_code))
    st.sidebar.write(guidance_response)

# Function to display financial literacy tips
def display_financial_tips(language_code):
    tips_prompt = f"Provide a simple financial literacy tip, such as saving strategies or tips on improving credit scores, in {language_code}."
    tips_response = get_ai_response(tips_prompt, language_code)
    st.sidebar.write(translate_text("**Financial Literacy Tip:**", language_code))
    st.sidebar.write(tips_response)

# Streamlit App
def main():
    st.set_page_config(page_title="Multilingual Loan Advisor", page_icon="🏠")
    st.title(translate_text("SBI Home Loan Application Form 🏠", "en"))

    # Language selection
    languages = {
        "English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr", "German": "de",
        "Chinese (Simplified)": "zh-CN", "Arabic": "ar", "Russian": "ru", "Japanese": "ja",
        "Portuguese": "pt", "Italian": "it", "Korean": "ko"
    }
    selected_language = st.selectbox(translate_text("Select Language:", "en"), list(languages.keys()))
    language_code = languages[selected_language]

    st.write(translate_text("Fill out the form below to apply for a home loan. For assistance, ask our AI assistant!", language_code))

    # AI Loan Assistant in Sidebar
    st.sidebar.title(translate_text("AI Loan Assistant 🤖", language_code))
    user_query = st.sidebar.text_input(translate_text("Ask me anything about the loan process:", language_code))
    if user_query:
        english_query = translate_text(user_query, "en")
        ai_response = get_ai_response(f"You are a loan advisor. Help the user with their query: {english_query}", language_code)
        st.sidebar.write(translate_text("AI Assistant Response:", language_code))
        st.sidebar.write(ai_response)

        # Loan Application Guidance
        if any(keyword in user_query.lower() for keyword in ["apply loan", "loan application", "documents"]):
            display_loan_guidance(language_code)

        # Financial Literacy Tips
        if any(keyword in user_query.lower() for keyword in ["financial tips", "saving", "credit score"]):
            display_financial_tips(language_code)

        # EMI Calculation
        if "emi" in user_query.lower() or "loan calculator" in user_query.lower():
            st.sidebar.write(translate_text("**EMI Calculation:**", language_code))
            loan_amount = st.sidebar.number_input(translate_text("Loan Amount (in INR):", language_code), min_value=0)
            interest_rate = st.sidebar.number_input(translate_text("Interest Rate (%):", language_code), min_value=0.0)
            tenure = st.sidebar.number_input(translate_text("Loan Tenure (in years):", language_code), min_value=1)
            if loan_amount > 0 and interest_rate > 0 and tenure > 0:
                emi_details = generate_emi_details(loan_amount, interest_rate, tenure, language_code)
                st.sidebar.write(emi_details)

    # Loan Application Form
    with st.form("loan_form"):
        st.header(translate_text("Applicant Details", language_code))
        name = st.text_input(translate_text("Full Name:", language_code), placeholder=translate_text("Enter your full name", language_code))
        
        # Custom Date Range for Date of Birth
        min_dob = date(1900, 1, 1)  # Minimum date: January 1, 1900
        max_dob = date.today()  # Maximum date: Today
        dob = st.date_input(
            translate_text("Date of Birth:", language_code),
            min_value=min_dob,
            max_value=max_dob,
            value=date(1990, 1, 1)  # Default date: January 1, 1990
        )
        
        mobile = st.text_input(translate_text("Mobile Number:", language_code), placeholder=translate_text("Enter your mobile number", language_code))
        email = st.text_input(translate_text("Email:", language_code), placeholder=translate_text("Enter your email", language_code))
        pan = st.text_input(translate_text("PAN Number:", language_code), placeholder=translate_text("Enter your PAN number", language_code))
        aadhaar = st.text_input(translate_text("Aadhaar Number:", language_code), placeholder=translate_text("Enter your Aadhaar number", language_code))
        marital_status = st.selectbox(translate_text("Marital Status:", language_code), ["Single", "Married", "Divorced", "Widowed"])
        gender = st.selectbox(translate_text("Gender:", language_code), ["Male", "Female", "Third Gender"])

        st.header(translate_text("Residential Details", language_code))
        residential_address = st.text_area(translate_text("Residential Address:", language_code), placeholder=translate_text("Enter your residential address", language_code))
        permanent_address = st.text_area(translate_text("Permanent Address:", language_code), placeholder=translate_text("Enter your permanent address", language_code))
        same_as_residential = st.checkbox(translate_text("Permanent address is the same as residential address", language_code))

        st.header(translate_text("Employment Details", language_code))
        occupation = st.selectbox(translate_text("Occupation:", language_code), ["Salaried", "Self-Employed", "Business", "Retired", "Other"])
        if occupation == "Salaried":
            employer_name = st.text_input(translate_text("Employer Name:", language_code), placeholder=translate_text("Enter your employer's name", language_code))
            monthly_income = st.number_input(translate_text("Monthly Income (in INR):", language_code), min_value=0)
        elif occupation == "Self-Employed" or occupation == "Business":
            business_name = st.text_input(translate_text("Business Name:", language_code), placeholder=translate_text("Enter your business name", language_code))
            annual_income = st.number_input(translate_text("Annual Income (in INR):", language_code), min_value=0)

        st.header(translate_text("Loan Details", language_code))
        loan_amount = st.number_input(translate_text("Requested Loan Amount (in INR):", language_code), min_value=0)
        loan_purpose = st.selectbox(translate_text("Purpose of Loan:", language_code), ["Purchase of Plot", "Purchase of House/Flat", "Construction", "Renovation", "Takeover of Loan"])
        tenure = st.slider(translate_text("Loan Tenure (in years):", language_code), min_value=1, max_value=30)

        submitted = st.form_submit_button(translate_text("Submit Application", language_code))
        if submitted:
            if not name or not mobile or not email or not pan or not aadhaar:
                st.error(translate_text("Please fill in all required fields.", language_code))
            else:
                st.success(translate_text("Application Submitted Successfully!", language_code))
                applicant_data_string = f"Name: {name}, Date of Birth: {dob}, Mobile: {mobile}, Email: {email}, PAN: {pan}, Aadhaar: {aadhaar}, Marital Status: {marital_status}, Gender: {gender}, Residential Address: {residential_address}, Permanent Address: {permanent_address if not same_as_residential else residential_address}, Occupation: {occupation}, Employer Name: {employer_name if occupation == 'Salaried' else business_name}, Income: {monthly_income if occupation == 'Salaried' else annual_income}, Loan Amount: {loan_amount}, Loan Purpose: {loan_purpose}, Tenure: {tenure} years."
                st.write(translate_text(applicant_data_string, language_code))

                st.write(translate_text("**Loan Sanction Check:**", language_code))
                if occupation == "Salaried":
                    sanction_result = check_loan_sanction(monthly_income, loan_amount, tenure, language_code)
                else:
                    sanction_result = check_loan_sanction(annual_income / 12, loan_amount, tenure, language_code)
                st.write(sanction_result)

                st.write(translate_text("**AI Eligibility Check:**", language_code))
                eligibility_prompt = f"Based on the following details, is the applicant eligible for a home loan? {applicant_data_string}"
                eligibility_response = get_ai_response(eligibility_prompt, language_code)
                st.write(eligibility_response)

if __name__ == "__main__":
    main()
