import streamlit as st
import pandas as pd
import plotly.express as px


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Palo Alto Networks Attrition Dashboard",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# LOAD DATASET
# =====================================================

file_path = r"C:\Users\aksha\Downloads\Palo Alto Networks.csv"

df = pd.read_csv(file_path)


# =====================================================
# BASIC DATA CLEANING
# =====================================================

df = df.dropna(how="all")

df = df.drop_duplicates()

df["Attrition"] = pd.to_numeric(
    df["Attrition"],
    errors="coerce"
)

df = df.dropna(
    subset=["Attrition"]
)


# =====================================================
# TITLE
# =====================================================

st.title(
    "Palo Alto Networks Employee Attrition Dashboard"
)

st.write(
    "Interactive analysis of employee attrition across "
    "departments, job roles, demographics, tenure, "
    "overtime, and business travel."
)


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Dashboard Filters")


# Department Selector

department_options = ["All"] + sorted(
    df["Department"]
    .dropna()
    .unique()
    .tolist()
)

selected_department = st.sidebar.selectbox(
    "Department",
    department_options
)


# Job Role Filter

jobrole_options = ["All"] + sorted(
    df["JobRole"]
    .dropna()
    .unique()
    .tolist()
)

selected_jobrole = st.sidebar.selectbox(
    "Job Role",
    jobrole_options
)


# Tenure Range Slider

min_years = int(
    df["YearsAtCompany"].min()
)

max_years = int(
    df["YearsAtCompany"].max()
)

selected_tenure = st.sidebar.slider(
    "Years at Company",
    min_value=min_years,
    max_value=max_years,
    value=(min_years, max_years)
)


# Overtime Filter

selected_overtime = st.sidebar.radio(
    "Overtime",
    ["All", "Yes", "No"]
)


# Business Travel Filter

travel_options = ["All"] + sorted(
    df["BusinessTravel"]
    .dropna()
    .unique()
    .tolist()
)

selected_travel = st.sidebar.selectbox(
    "Business Travel",
    travel_options
)


# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df.copy()


if selected_department != "All":

    filtered_df = filtered_df[
        filtered_df["Department"]
        == selected_department
    ]


if selected_jobrole != "All":

    filtered_df = filtered_df[
        filtered_df["JobRole"]
        == selected_jobrole
    ]


filtered_df = filtered_df[
    (
        filtered_df["YearsAtCompany"]
        >= selected_tenure[0]
    )
    &
    (
        filtered_df["YearsAtCompany"]
        <= selected_tenure[1]
    )
]


if selected_overtime != "All":

    filtered_df = filtered_df[
        filtered_df["OverTime"]
        == selected_overtime
    ]


if selected_travel != "All":

    filtered_df = filtered_df[
        filtered_df["BusinessTravel"]
        == selected_travel
    ]


# =====================================================
# MODULE 1: ATTRITION OVERVIEW
# =====================================================

st.header("1. Attrition Overview")


# =====================================================
# BASIC KPI CALCULATIONS
# =====================================================

total_employees = len(
    filtered_df
)


employees_exited = int(
    filtered_df["Attrition"].sum()
)


employees_retained = (
    total_employees
    - employees_exited
)


# =====================================================
# REQUIRED KPI 1:
# ATTRITION RATE
# =====================================================

if total_employees > 0:

    attrition_rate = (

        employees_exited
        / total_employees

    ) * 100

else:

    attrition_rate = 0


# =====================================================
# REQUIRED KPI 2:
# DEPARTMENT ATTRITION RATE
# =====================================================

if len(filtered_df) > 0:

    department_attrition_rate = (

        filtered_df["Attrition"].mean()

    ) * 100

else:

    department_attrition_rate = 0


# =====================================================
# REQUIRED KPI 3:
# ROLE ATTRITION RATE
# =====================================================

if len(filtered_df) > 0:

    role_attrition_rate = (

        filtered_df["Attrition"].mean()

    ) * 100

else:

    role_attrition_rate = 0


# =====================================================
# REQUIRED KPI 4:
# EARLY-TENURE ATTRITION
#
# Early tenure = 0–2 years
# =====================================================

early_tenure_df = filtered_df[

    filtered_df["YearsAtCompany"] <= 2

]


if len(early_tenure_df) > 0:

    early_tenure_attrition = (

        early_tenure_df["Attrition"].mean()

    ) * 100

else:

    early_tenure_attrition = 0


# =====================================================
# REQUIRED KPI 5:
# WORKLOAD ATTRITION INDEX
#
# Employees who:
# - Work overtime
# OR
# - Travel frequently
# =====================================================

workload_df = filtered_df[

    (

        filtered_df["OverTime"]
        == "Yes"

    )

    |

    (

        filtered_df["BusinessTravel"]
        == "Travel_Frequently"

    )

]


if len(workload_df) > 0:

    workload_attrition_index = (

        workload_df["Attrition"].mean()

    ) * 100

else:

    workload_attrition_index = 0


# =====================================================
# MAIN KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Employees",
    total_employees
)


col2.metric(
    "Overall Attrition Rate",
    f"{attrition_rate:.2f}%"
)


col3.metric(
    "Employees Retained",
    employees_retained
)


col4.metric(
    "Employees Exited",
    employees_exited
)


# =====================================================
# REQUIRED PROJECT KPI CARDS
# =====================================================

st.subheader(
    "Key Performance Indicators"
)


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Attrition Rate",
    f"{attrition_rate:.2f}%"
)


col2.metric(
    "Department Attrition Rate",
    f"{department_attrition_rate:.2f}%"
)


col3.metric(
    "Role Attrition Rate",
    f"{role_attrition_rate:.2f}%"
)


col4.metric(
    "Early-Tenure Attrition",
    f"{early_tenure_attrition:.2f}%"
)


col5.metric(
    "Workload Attrition Index",
    f"{workload_attrition_index:.2f}%"
)


# =====================================================
# RETAINED VS EXITED DISTRIBUTION
# =====================================================

distribution_data = pd.DataFrame({

    "Status": [

        "Retained",

        "Exited"

    ],

    "Employees": [

        employees_retained,

        employees_exited

    ]

})


fig_distribution = px.pie(

    distribution_data,

    names="Status",

    values="Employees",

    hole=0.45,

    title="Retained vs Exited Employee Distribution"

)


st.plotly_chart(

    fig_distribution,

    use_container_width=True

)


# =====================================================
# MODULE 2:
# DEPARTMENT & ROLE ANALYSIS
# =====================================================

st.header(
    "2. Department & Role Attrition Analysis"
)


# Department Attrition Rate

department_data = (

    filtered_df

    .groupby("Department")

    ["Attrition"]

    .mean()

    .reset_index()

)


department_data[
    "Attrition Rate (%)"
] = (

    department_data["Attrition"]

    * 100

)


department_data = department_data.sort_values(

    "Attrition Rate (%)",

    ascending=False

)


fig_department = px.bar(

    department_data,

    x="Department",

    y="Attrition Rate (%)",

    title="High-Risk Department Identification",

    text_auto=".2f"

)


st.plotly_chart(

    fig_department,

    use_container_width=True

)


# Department × Job Role Heatmap

heatmap_data = (

    filtered_df

    .pivot_table(

        index="Department",

        columns="JobRole",

        values="Attrition",

        aggfunc="mean"

    )

    * 100

)


fig_heatmap = px.imshow(

    heatmap_data,

    text_auto=".1f",

    aspect="auto",

    title="Department × Job Role Attrition Intensity (%)",

    labels={

        "x": "Job Role",

        "y": "Department",

        "color": "Attrition Rate (%)"

    }

)


st.plotly_chart(

    fig_heatmap,

    use_container_width=True

)


# =====================================================
# MODULE 3:
# DEMOGRAPHIC ATTRITION EXPLORER
# =====================================================

st.header(
    "3. Demographic Attrition Explorer"
)


selected_age = st.slider(

    "Select Age Range",

    min_value=int(

        df["Age"].min()

    ),

    max_value=int(

        df["Age"].max()

    ),

    value=(

        int(

            df["Age"].min()

        ),

        int(

            df["Age"].max()

        )

    )

)


demographic_df = filtered_df[

    (

        filtered_df["Age"]

        >= selected_age[0]

    )

    &

    (

        filtered_df["Age"]

        <= selected_age[1]

    )

]


col1, col2 = st.columns(2)


# Gender Analysis

with col1:

    gender_data = (

        demographic_df

        .groupby("Gender")

        ["Attrition"]

        .mean()

        .reset_index()

    )


    gender_data[
        "Attrition Rate (%)"
    ] = (

        gender_data["Attrition"]

        * 100

    )


    fig_gender = px.bar(

        gender_data,

        x="Gender",

        y="Attrition Rate (%)",

        title="Attrition Rate by Gender",

        text_auto=".2f"

    )


    st.plotly_chart(

        fig_gender,

        use_container_width=True

    )


# Education Analysis

with col2:

    education_data = (

        demographic_df

        .groupby("EducationField")

        ["Attrition"]

        .mean()

        .reset_index()

    )


    education_data[
        "Attrition Rate (%)"
    ] = (

        education_data["Attrition"]

        * 100

    )


    fig_education = px.bar(

        education_data,

        x="Attrition Rate (%)",

        y="EducationField",

        orientation="h",

        title="Attrition Rate by Education Field",

        text_auto=".2f"

    )


    st.plotly_chart(

        fig_education,

        use_container_width=True

    )


# Age Analysis

age_data = (

    demographic_df

    .groupby("Age")

    ["Attrition"]

    .mean()

    .reset_index()

)


age_data[
    "Attrition Rate (%)"
] = (

    age_data["Attrition"]

    * 100

)


fig_age = px.line(

    age_data,

    x="Age",

    y="Attrition Rate (%)",

    markers=True,

    title="Attrition Rate by Age"

)


st.plotly_chart(

    fig_age,

    use_container_width=True

)


# =====================================================
# MODULE 4:
# TENURE & WORKLOAD ANALYSIS
# =====================================================

st.header(
    "4. Tenure & Workload Analysis"
)


# Tenure Buckets

tenure_df = filtered_df.copy()


tenure_df[
    "Tenure Bucket"
] = pd.cut(

    tenure_df["YearsAtCompany"],

    bins=[

        -1,

        2,

        5,

        10,

        20,

        float("inf")

    ],

    labels=[

        "0–2 Years",

        "3–5 Years",

        "6–10 Years",

        "11–20 Years",

        "20+ Years"

    ]

)


tenure_data = (

    tenure_df

    .groupby(

        "Tenure Bucket",

        observed=False

    )

    ["Attrition"]

    .mean()

    .reset_index()

)


tenure_data[
    "Attrition Rate (%)"
] = (

    tenure_data["Attrition"]

    * 100

)


fig_tenure = px.bar(

    tenure_data,

    x="Tenure Bucket",

    y="Attrition Rate (%)",

    title="Attrition Rate by Tenure Bucket",

    text_auto=".2f"

)


st.plotly_chart(

    fig_tenure,

    use_container_width=True

)


col1, col2 = st.columns(2)


# Overtime Analysis

with col1:

    overtime_data = (

        filtered_df

        .groupby("OverTime")

        ["Attrition"]

        .mean()

        .reset_index()

    )


    overtime_data[
        "Attrition Rate (%)"
    ] = (

        overtime_data["Attrition"]

        * 100

    )


    fig_overtime = px.bar(

        overtime_data,

        x="OverTime",

        y="Attrition Rate (%)",

        title="Overtime Impact on Attrition",

        text_auto=".2f"

    )


    st.plotly_chart(

        fig_overtime,

        use_container_width=True

    )


# Business Travel Analysis

with col2:

    travel_data = (

        filtered_df

        .groupby("BusinessTravel")

        ["Attrition"]

        .mean()

        .reset_index()

    )


    travel_data[
        "Attrition Rate (%)"
    ] = (

        travel_data["Attrition"]

        * 100

    )


    fig_travel = px.bar(

        travel_data,

        x="BusinessTravel",

        y="Attrition Rate (%)",

        title="Business Travel Impact on Attrition",

        text_auto=".2f"

    )


    st.plotly_chart(

        fig_travel,

        use_container_width=True

    )


# =====================================================
# VIEW FILTERED DATASET
# =====================================================

with st.expander(
    "View Filtered Dataset"
):

    st.dataframe(

        filtered_df,

        use_container_width=True

    )