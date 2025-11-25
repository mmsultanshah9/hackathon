import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

st.title("📊 Banggood Data Analysis Dashboard")

st.write("Upload the cleaned CSV file to start analysis.")

df = pd.read_csv("cleaned_replaced_banggood.csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # --- Data Preparation ---
    df['main_category'] = df['category_url'].apply(
        lambda x: re.search(r'Wholesale-(.*?)-c-\d+', x).group(1)
        if re.search(r'Wholesale-(.*?)-c-\d+', x) else 'Other'
    )

    df['value_metric'] = df['rating'] / np.log1p(df['price_pkr'])

    st.success("Data Preparation Complete")

    st.write("### Unique Categories Found:")
    st.write(df['main_category'].unique())

    # -------------------------------
    # Analysis 1 – Price Distribution
    # -------------------------------
    st.header("1. Price Distribution per Category")

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='main_category', y=np.log1p(df['price_pkr']), data=df, palette='pastel', ax=ax1)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)

    # -------------------------------
    # Analysis 2 – Rating vs Price
    # -------------------------------
    st.header("2. Rating vs Log-Price (Scatter Plot)")

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='rating', y=np.log1p(df['price_pkr']), data=df, alpha=0.6, ax=ax2)
    ax2.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig2)

    # -------------------------------
    # Analysis 3 – Top 5 Reviewed Products
    # -------------------------------
    st.header("3. Top 5 Reviewed Products")

    top_reviewed = df.sort_values(by="reviews", ascending=False).head(5)

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="reviews", y="product_name", data=top_reviewed, palette="magma", ax=ax3)
    st.pyplot(fig3)

    # -------------------------------
    # Analysis 4 – Best Value Metric per Category
    # -------------------------------
    st.header("4. Best Value Metric per Category")

    best_value_products = df.loc[df.groupby("main_category")["value_metric"].idxmax()]
    best_value_products = best_value_products.sort_values(by="value_metric", ascending=False)

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='main_category', y='value_metric', data=best_value_products, palette='viridis', ax=ax4)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4)

    # -------------------------------
    # Analysis 5 – Correlation Matrix
    # -------------------------------
    st.header("5. Correlation Matrix (Price, Rating, Reviews)")

    numerical_df = df[['price_pkr', 'rating', 'reviews']]
    correlation_matrix = numerical_df.corr()

    fig5, ax5 = plt.subplots(figsize=(7, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax5)
    st.pyplot(fig5)

else:
    st.warning("Please upload a CSV file to continue.")

