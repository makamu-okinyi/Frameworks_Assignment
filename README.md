CORD-19 Data Analysis Project
📋 Project Overview
This project provides a comprehensive analysis of the CORD-19 (COVID-19 Open Research Dataset) metadata, exploring patterns in COVID-19 research publications through data exploration, visualization, and an interactive web application.

Project Type: Data Analysis & Visualization
Domain: Healthcare Research, Bibliometrics
Technologies: Python, Pandas, Streamlit, Matplotlib, Seaborn
Dataset: CORD-19 Metadata (COVID-19 research papers)metadata.csv

🎯 Objectives
Perform exploratory data analysis on COVID-19 research metadata

Identify trends in publication patterns over time

Analyze journal distribution and research sources

Extract key themes from paper titles using text analysis

Create an interactive web application for data exploration

📊 Dataset Information
The CORD-19 dataset contains metadata for COVID-19 and coronavirus-related research papers. Key columns include:

title: Paper title

abstract: Paper abstract

authors: Author list

journal: Publication journal

publish_time: Publication date

source_x: Data source

doi: Digital Object Identifier

🏗️ Project Structure
Reflection and Documentation
1. Project Overview

This project explored the CORD-19 dataset, a collection of COVID-19 research papers. The goal was to perform data cleaning, analysis, and visualization using Python and Streamlit. The main objectives were to understand data trends, identify the most active research sources, and build an interactive app for exploring the dataset.

2. Data Cleaning and Preparation

The dataset initially contained several missing values and inconsistent date formats.
To prepare it for analysis:

Columns with more than 70% missing values were removed.

The last_updated column was converted into a datetime format for easier time-based analysis.

A new column, year, was extracted from last_updated to study trends over time.

The title word count was computed for each paper to analyze patterns in research titles.

This preprocessing step ensured that the dataset was consistent and ready for visualization.

3. Analysis and Visualization

Using matplotlib, several insights were obtained:

📈 Publications by Year: A bar chart revealed publication surges during specific pandemic phases, showing how research output evolved.

🏢 Top Source Organizations: Another chart highlighted which institutions or publishers contributed the most papers, emphasizing the collaborative nature of COVID-19 research.

☁️ Word Cloud: Common keywords in paper titles, such as virus, pandemic, health, and model, visually summarized the dataset’s research focus.

The app provided a year range filter, enabling interactive exploration of publication trends.

4. Streamlit Application

The final deliverable was an interactive Streamlit app (cord19_app.py) that:

Displays sample data tables.

Filters publications by year.

Visualizes trends and top contributors.

Generates a real-time word cloud of paper titles.

Provides summary statistics such as total papers and average title length.

This app allows both researchers and the public to explore the dataset dynamically without needing programming skills.

5. Reflection and Learning Outcomes

Throughout the project, I gained hands-on experience with:

Pandas for data cleaning and transformation.

Matplotlib and WordCloud for visualization.

Streamlit for creating interactive dashboards.

I learned the importance of data preprocessing, since raw data often contains inconsistencies that can mislead analysis.
The process of linking Python analysis with a web interface also deepened my understanding of how data science and web technologies intersect.

This project strengthened my confidence in:

Writing clean, modular Python code.

Turning data into visual insights.

Deploying lightweight, interactive web apps for real-world datasets.

6. Conclusion

The CORD-19 Data Explorer successfully transformed a complex research dataset into an accessible visualization tool.
It demonstrated how data science and web development can merge to support knowledge discovery — a vital skill in modern technology and research environments.

Consult Streamlit documentation for application issues

Note: This project demonstrates a complete data science workflow from raw data to interactive application, showcasing skills in data analysis, visualization, and web development using Python ecosystem tools.

