import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Payroll Analysis App", layout="wide")

# Upload file
st.sidebar.title("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

@st.cache_data
def load_data(file):
    return pd.read_excel(file)

if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data("PAYROLL_CLEANED.xlsx")

# Filters
st.sidebar.title("Filters")
if 'GENDER' in df.columns:
    gender = st.sidebar.multiselect("Gender", df['GENDER'].unique(), default=df['GENDER'].unique())
    df = df[df['GENDER'].isin(gender)]

if 'DEPARTMENT_TITLE' in df.columns:
    dept = st.sidebar.multiselect("Department", df['DEPARTMENT_TITLE'].unique(), default=df['DEPARTMENT_TITLE'].unique())
    df = df[df['DEPARTMENT_TITLE'].isin(dept)]

# Tabs
kpi_tab, viz_tab = st.tabs(["KPI Dashboard", "All 13 Analysis"])

# KPI
with kpi_tab:
    st.title("KPI Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(df))
    col2.metric("Average Salary", round(df['TOTAL_PAY'].mean(),2))
    col3.metric("Max Salary", df['TOTAL_PAY'].max())

# ALL QUESTIONS
with viz_tab:
    st.title("All 13 Business Questions Analysis")

    # 1 Salary Distribution
    st.subheader("1. Salary Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['TOTAL_PAY'], kde=True, ax=ax)
    st.pyplot(fig)

    # 2 Gender vs Salary
    st.subheader("2. Gender-wise Salary Comparison")
    fig, ax = plt.subplots()
    sns.boxplot(x='GENDER', y='TOTAL_PAY', data=df, ax=ax)
    st.pyplot(fig)

    # 3 Highest Paying Job Titles
    st.subheader("3. Highest Paying Job Titles")
    job_salary = df.groupby('JOB_TITLE')['TOTAL_PAY'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    job_salary.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # 4 Department Salary
    st.subheader("4. Department-wise Salary")
    fig, ax = plt.subplots()
    sns.barplot(x='DEPARTMENT_TITLE', y='TOTAL_PAY', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # 5 Employment Type Distribution
    st.subheader("5. Employment Type Distribution")
    fig, ax = plt.subplots()
    df['EMPLOYMENT_TYPE'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

    # 6 Top 5 Highest Paid Employees
    st.subheader("6. Top 5 Highest Paid Employees")
    top5 = df.nlargest(5, 'TOTAL_PAY')
    fig, ax = plt.subplots()
    sns.barplot(x='TOTAL_PAY', y='JOB_TITLE', data=top5, ax=ax)
    st.pyplot(fig)

    # 7 Benefit vs Total Pay
    st.subheader("7. Benefit Pay vs Total Pay")
    fig, ax = plt.subplots()
    sns.scatterplot(x='BENEFIT_PAY', y='TOTAL_PAY', data=df, ax=ax)
    st.pyplot(fig)

    # 8 Ethnicity Distribution
    st.subheader("8. Ethnicity Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='ETHNICITY', data=df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 9 Overtime by Gender
    st.subheader("9. Overtime by Gender")
    fig, ax = plt.subplots()
    sns.barplot(x='GENDER', y='OVERTIME_PAY', data=df, ax=ax)
    st.pyplot(fig)

    # 10 Full-time vs Part-time Salary
    st.subheader("10. Full-time vs Part-time Salary")
    fig, ax = plt.subplots()
    sns.boxplot(x='EMPLOYMENT_TYPE', y='TOTAL_PAY', data=df, ax=ax)
    st.pyplot(fig)

    # 11 Correlation Matrix
    st.subheader("11. Correlation Matrix")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(numeric_only=True), annot=True, ax=ax)
    st.pyplot(fig)

    # 12 Most Common Job Titles
    st.subheader("12. Most Common Job Titles")
    common_jobs = df['JOB_TITLE'].value_counts().head(10)
    fig, ax = plt.subplots()
    common_jobs.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # 13 Department vs Employment Type Salary
    st.subheader("13. Department vs Employment Type Salary")
    pivot = df.pivot_table(values='TOTAL_PAY', index='DEPARTMENT_TITLE', columns='EMPLOYMENT_TYPE', aggfunc='mean')
    st.dataframe(pivot)

st.markdown("---")
st.markdown("Payroll Analysis Streamlit App")