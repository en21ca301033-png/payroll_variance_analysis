import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Payroll Analysis App", layout="wide")

# Sidebar - Upload file
st.sidebar.title("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

# Load default or uploaded dataset
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.sidebar.info("Using default dataset")
    df = load_data("PAYROLL_CLEANED.xlsx")

# Sidebar Filters
st.sidebar.title("Filters")

if 'GENDER' in df.columns:
    gender_filter = st.sidebar.multiselect("Select Gender", df['GENDER'].unique(), default=df['GENDER'].unique())
    df = df[df['GENDER'].isin(gender_filter)]

if 'DEPARTMENT_TITLE' in df.columns:
    dept_filter = st.sidebar.multiselect("Select Department", df['DEPARTMENT_TITLE'].unique(), default=df['DEPARTMENT_TITLE'].unique())
    df = df[df['DEPARTMENT_TITLE'].isin(dept_filter)]

# Tabs
kpi_tab, viz_tab, analysis_tab = st.tabs(["KPI Dashboard", "Visualizations", "Analysis"])

# KPI TAB
with kpi_tab:
    st.title("Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Employees", len(df))
    col2.metric("Average Salary", round(df['TOTAL_PAY'].mean(), 2))
    col3.metric("Max Salary", df['TOTAL_PAY'].max())

    col4, col5 = st.columns(2)
    col4.metric("Total Overtime Pay", df['OVERTIME_PAY'].sum())
    col5.metric("Total Benefit Pay", df['BENEFIT_PAY'].sum())

# VISUALIZATION TAB
with viz_tab:
    st.title("Visualizations")

    # Salary Distribution
    st.subheader("Salary Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['TOTAL_PAY'], kde=True, ax=ax)
    st.pyplot(fig)

    # Gender vs Salary
    st.subheader("Gender vs Total Pay")
    fig, ax = plt.subplots()
    sns.boxplot(x='GENDER', y='TOTAL_PAY', data=df, ax=ax)
    st.pyplot(fig)

    # Job Title Avg Salary
    st.subheader("Top 10 Job Titles by Avg Salary")
    job_salary = df.groupby('JOB_TITLE')['TOTAL_PAY'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    job_salary.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Department Salary
    st.subheader("Department-wise Salary")
    fig, ax = plt.subplots()
    sns.barplot(x='DEPARTMENT_TITLE', y='TOTAL_PAY', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Employment Type Pie
    st.subheader("Employment Type Distribution")
    fig, ax = plt.subplots()
    df['EMPLOYMENT_TYPE'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

    # Scatter Plot
    st.subheader("Benefit Pay vs Total Pay")
    fig, ax = plt.subplots()
    sns.scatterplot(x='BENEFIT_PAY', y='TOTAL_PAY', data=df, ax=ax)
    st.pyplot(fig)

# ANALYSIS TAB
with analysis_tab:
    st.title("Insights & Analysis")

    st.subheader("Top 5 Highest Paid Employees")
    top5 = df.nlargest(5, 'TOTAL_PAY')
    st.dataframe(top5)

    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(numeric_only=True), annot=True, ax=ax)
    st.pyplot(fig)

    st.subheader("Most Common Job Titles")
    common_jobs = df['JOB_TITLE'].value_counts().head(10)
    st.bar_chart(common_jobs)

    st.subheader("Department vs Employment Type Salary")
    pivot = df.pivot_table(values='TOTAL_PAY', index='DEPARTMENT_TITLE', columns='EMPLOYMENT_TYPE', aggfunc='mean')
    st.dataframe(pivot)

# Footer
st.markdown("---")
st.markdown("Developed for Payroll Analysis Project")
