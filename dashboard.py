
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Web Scraper",
    layout="wide"
)

st.title("AI-Powered Web Scraper")
st.subheader("Book Data Analysis Dashboard")

try:
    df = pd.read_csv("books.csv")

    # Convert price to numbers
    df["Price (£)"] = pd.to_numeric(
        df["Price (£)"], errors="coerce"
    )

    # Search filter
    search_text = st.text_input("Search books by title")

    # Price filter
    min_price = float(df["Price (£)"].min())
    max_price = float(df["Price (£)"].max())

    price_range = st.slider(
        "Filter by price (£)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )

    # Rating filter
    rating_options = ["One", "Two", "Three", "Four", "Five"]

    selected_ratings = st.multiselect(
        "Filter by rating",
        options=rating_options,
        default=rating_options
    )

    # Apply filters
    filtered_df = df.copy()

    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(
            search_text, case=False, na=False
        )
    ]

    filtered_df = filtered_df[
        (filtered_df["Price (£)"] >= price_range[0]) &
        (filtered_df["Price (£)"] <= price_range[1])
    ]

    filtered_df = filtered_df[
        filtered_df["Rating"].isin(selected_ratings)
    ]

    # Display filtered books
    st.subheader("Filtered Book Data")
    st.dataframe(filtered_df, use_container_width=True)

    # Metrics
    st.subheader("Filtered Data Analysis")

    if not filtered_df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("Books Found", len(filtered_df))

        col2.metric(
            "Average Price (£)",
            f"£{filtered_df['Price (£)'].mean():.2f}"
        )

        col3.metric(
            "Highest Price (£)",
            f"£{filtered_df['Price (£)'].max():.2f}"
        )
    else:
        st.warning("No books match your filters.")

    # Chart
    if not filtered_df.empty:
        st.subheader("Book Price Chart")

        fig, ax = plt.subplots()

        ax.bar(
            filtered_df["Title"],
            filtered_df["Price (£)"]
        )

        ax.set_xlabel("Book Title")
        ax.set_ylabel("Price (£)")
        ax.set_title("Book Prices")
        plt.xticks(rotation=90)
        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    # Download filtered data
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Data CSV",
        data=csv,
        file_name="filtered_books.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("books.csv not found. Run main.py first.")

except Exception as e:
    st.error(f"An error occurred: {e}")
