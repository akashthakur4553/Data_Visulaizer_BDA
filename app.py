import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set Streamlit page configuration for modern look
st.set_page_config(page_title="Interactive Dashboard", layout="wide")

st.title("Interactive Data Dashboard")

# File uploader to load dataset with progress
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)", type=["csv", "xlsx"]
)

# Check for file size and progress
if uploaded_file:
    file_size = uploaded_file.size / (1024 * 1024)  # Convert to MB
    if file_size > 20:
        st.error("File size exceeds 20MB, please upload a smaller file.")
    else:
        try:
            # Read the dataset with progress indicator
            with st.spinner("Loading data..."):
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)

            st.success("Dataset uploaded successfully!")
            st.write(df.head())  # Display the first few rows of the dataset

            # Basic statistics and data info
            if st.checkbox("Show dataset info"):
                st.write(df.describe())
                st.write("Shape of the dataset:", df.shape)
                st.write("Number of missing values:", df.isnull().sum())

            # Select columns for analysis
            st.sidebar.header("Plot Customization")
            numeric_columns = df.select_dtypes(
                include=["float64", "int64"]
            ).columns.tolist()
            categorical_columns = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            # Plot selection
            plot_types = st.sidebar.multiselect(
                "Select the types of plots to include",
                [
                    "Bar Chart",
                    "Line Chart",
                    "Scatter Plot",
                    "Pie Chart",
                    "Histogram",
                    "Box Plot",
                    "Heatmap",
                    "Spider Plot",
                    "Pairplot",
                    "Violin Plot",
                    "Density Contour Plot",
                    "Bubble Chart",
                    "3D Scatter Plot",
                    "Treemap",
                    "One vs Multiple Features",
                ],
            )

            # Number of plots to include
            num_plots = st.sidebar.slider(
                "Select number of plots", min_value=1, max_value=6
            )

            # Plot customization based on user input
            if len(plot_types) > 0:
                st.subheader("Dashboard")

                plot_count = 0
                for plot_type in plot_types:
                    if plot_count >= num_plots:
                        break

                    if plot_type == "Bar Chart":
                        st.write("Bar Chart")
                        col = st.selectbox(
                            f"Select column for Bar Chart {plot_count+1}",
                            categorical_columns,
                        )
                        fig = px.bar(df, x=col)
                        st.plotly_chart(fig, use_container_width=True)

                    if plot_type == "Line Chart":
                        st.write("Line Chart")
                        col = st.selectbox(
                            f"Select column for Line Chart {plot_count+1}",
                            numeric_columns,
                        )
                        fig = px.line(df, y=col)
                        st.plotly_chart(fig, use_container_width=True)

                    if plot_type == "Scatter Plot":
                        st.write("Scatter Plot")
                        x_col = st.selectbox(
                            f"Select X-axis for Scatter Plot {plot_count+1}",
                            numeric_columns,
                        )
                        y_col = st.selectbox(
                            f"Select Y-axis for Scatter Plot {plot_count+1}",
                            numeric_columns,
                        )
                        fig = px.scatter(df, x=x_col, y=y_col)
                        st.plotly_chart(fig, use_container_width=True)

                    if plot_type == "Pie Chart":
                        st.write("Pie Chart")
                        col = st.selectbox(
                            f"Select column for Pie Chart {plot_count+1}",
                            categorical_columns,
                        )
                        fig = px.pie(df, names=col)
                        st.plotly_chart(fig, use_container_width=True)

                    if plot_type == "Histogram":
                        st.write("Histogram")
                        col = st.selectbox(
                            f"Select column for Histogram {plot_count+1}",
                            numeric_columns,
                        )
                        fig = px.histogram(df, x=col)
                        st.plotly_chart(fig, use_container_width=True)

                    if plot_type == "Box Plot":
                        st.write("Box Plot")
                        col = st.selectbox(
                            f"Select column for Box Plot {plot_count+1}",
                            numeric_columns,
                        )
                        fig = px.box(df, y=col)
                        st.plotly_chart(fig, use_container_width=True)

                    # Modern and Advanced Plots
                    if plot_type == "Heatmap":
                        st.write("Heatmap")
                        corr = df.corr()
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                        st.pyplot(fig)

                    # Add more plot types as needed

                    # One vs Multiple Features
                    if plot_type == "One vs Multiple Features":
                        st.write("One Feature vs Multiple Features")

                        primary_feature = st.selectbox(
                            f"Select primary feature for comparison {plot_count+1}",
                            numeric_columns + categorical_columns,
                        )

                        comparison_features = st.multiselect(
                            f"Select features to compare with {primary_feature}",
                            numeric_columns + categorical_columns,
                        )

                        if len(comparison_features) > 0:
                            for feature in comparison_features:
                                st.write(f"Comparison: {primary_feature} vs {feature}")

                                # User selects plot type for comparison
                                plot_choice = st.selectbox(
                                    f"Choose plot type for {primary_feature} vs {feature}",
                                    [
                                        "Scatter Plot",
                                        "Bar Chart",
                                        "Box Plot",
                                        "Line Chart",
                                        "Heatmap",
                                        "Spider Plot",
                                        "Violin Plot",
                                    ],
                                    key=f"{primary_feature}_{feature}",
                                )

                                if (
                                    plot_choice == "Scatter Plot"
                                    and primary_feature in numeric_columns
                                    and feature in numeric_columns
                                ):
                                    fig = px.scatter(df, x=primary_feature, y=feature)
                                    st.plotly_chart(fig, use_container_width=True)

                                elif (
                                    plot_choice == "Bar Chart"
                                    and primary_feature in categorical_columns
                                    and feature in numeric_columns
                                ):
                                    fig = px.bar(df, x=primary_feature, y=feature)
                                    st.plotly_chart(fig, use_container_width=True)

                                elif (
                                    plot_choice == "Box Plot"
                                    and primary_feature in numeric_columns
                                    and feature in categorical_columns
                                ):
                                    fig = px.box(df, y=primary_feature, x=feature)
                                    st.plotly_chart(fig, use_container_width=True)

                                elif (
                                    plot_choice == "Line Chart"
                                    and primary_feature in numeric_columns
                                    and feature in numeric_columns
                                ):
                                    fig = px.line(df, x=primary_feature, y=feature)
                                    st.plotly_chart(fig, use_container_width=True)

                                elif (
                                    plot_choice == "Heatmap"
                                    and primary_feature in numeric_columns
                                    and feature in numeric_columns
                                ):
                                    st.write(
                                        "Heatmap between selected features not supported in this case."
                                    )

                                elif plot_choice == "Spider Plot":
                                    fig = go.Figure()
                                    categories = [primary_feature, feature]
                                    fig.add_trace(
                                        go.Scatterpolar(
                                            r=[
                                                df[primary_feature].mean(),
                                                df[feature].mean(),
                                            ],
                                            theta=categories,
                                            fill="toself",
                                            name=f"{primary_feature} vs {feature}",
                                        )
                                    )
                                    fig.update_layout(
                                        polar=dict(radialaxis=dict(visible=True))
                                    )
                                    st.plotly_chart(fig, use_container_width=True)

                                elif (
                                    plot_choice == "Violin Plot"
                                    and primary_feature in numeric_columns
                                    and feature in categorical_columns
                                ):
                                    fig = px.violin(
                                        df,
                                        y=primary_feature,
                                        x=feature,
                                        box=True,
                                        points="all",
                                    )
                                    st.plotly_chart(fig, use_container_width=True)

                                else:
                                    st.warning(
                                        f"Plot type not supported for {primary_feature} vs {feature}."
                                    )

                    plot_count += 1

            else:
                st.warning("Please select at least one plot type to display.")

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Awaiting dataset to be uploaded.")
