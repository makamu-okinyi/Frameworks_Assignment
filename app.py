import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Set page config 
st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

# ======== DATA LOADING ========
@st.cache_data
def load_data():
    
    file_path = 'CORD19 datasets - Sheet 1.csv' 
    
    # Load  data
    df_clean = pd.read_csv(CORD19 datasets - Sheet 1.csv)
  
    
    return df_clean

# Load the data
try:
    df_clean = load_data()
    st.success(f"✅ Loaded CORD-19 data with {len(df_clean)} papers!")
except FileNotFoundError:
    st.warning("⚠️ Data file not found. Using sample data instead.")
    df_clean = create_sample_data()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.warning("⚠️ Using sample data instead.")
    df_clean = create_sample_data()
# ======== END DATA LOADING ========

def create_streamlit_app():
 
    st.title("📊 CORD-19 Dataset Explorer")
    st.write("Interactive exploration of COVID-19 research papers metadata")
    
    # Sidebar for filters
    st.sidebar.header("Filters")
    
    # Year filter
    available_years = sorted(df_clean['year'].dropna().unique())
    if available_years:
        selected_years = st.sidebar.slider(
            "Select Year Range",
            min_value=int(min(available_years)),
            max_value=int(max(available_years)),
            value=(int(min(available_years)), int(max(available_years)))
        )
    else:
        selected_years = (2019, 2022)
        st.sidebar.warning("No year data available")
    
    # Source organization filter
    all_organizations = df_clean['source_organization'].dropna().unique()
    selected_orgs = st.sidebar.multiselect(
        "Filter by Organization",
        options=all_organizations,
        default=all_organizations[:5] if len(all_organizations) > 5 else all_organizations
    )
    
    # License filter
    all_licenses = df_clean['license'].dropna().unique()
    selected_licenses = st.sidebar.multiselect(
        "Filter by License",
        options=all_licenses,
        default=all_licenses
    )
    
    # Filter data based on selection
    filtered_df = df_clean[
        (df_clean['year'] >= selected_years[0]) & 
        (df_clean['year'] <= selected_years[1]) &
        (df_clean['source_organization'].isin(selected_orgs)) &
        (df_clean['license'].isin(selected_licenses))
    ]
    
    # Reset index for display
    filtered_df = filtered_df.reset_index(drop=True)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Overview")
        
        # Key metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Total Papers", len(filtered_df))
        with metric_col2:
            st.metric("Years Covered", f"{selected_years[0]} - {selected_years[1]}")
        with metric_col3:
            st.metric("Filtered Organizations", len(selected_orgs))
        
        # Publications by year chart
        st.subheader("Publications by Year")
        if not filtered_df.empty:
            yearly_counts = filtered_df['year'].value_counts().sort_index()
            st.bar_chart(yearly_counts)
        else:
            st.info("No data available for the selected filters")
    
    with col2:
        st.subheader("Top Source Organizations")
        if not filtered_df.empty:
            org_counts = filtered_df['source_organization'].value_counts().head(10)
            st.dataframe(org_counts, use_container_width=True)
        else:
            st.info("No organizations data available")
        
        # Word cloud
        st.subheader("Paper Titles Word Cloud")
        if not filtered_df.empty:
            titles_text = ' '.join(filtered_df['paper_title'].dropna().astype(str))
            if titles_text.strip():
                wordcloud = WordCloud(
                    width=400, 
                    height=200, 
                    background_color='white',
                    colormap='viridis',
                    max_words=50
                ).generate(titles_text)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("No title data available for word cloud")
        else:
            st.info("No data available for word cloud")
    
    # Sample data with expandable details
    st.subheader("Sample Papers")
    if not filtered_df.empty:
        display_columns = ['paper_title', 'year', 'source_organization', 'license']
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        
        sample_data = filtered_df[available_columns].head(10)
        st.dataframe(sample_data, use_container_width=True)
        
        # Show detailed view for selected paper
        if len(sample_data) > 0:
            st.subheader("Paper Details")
            selected_index = st.selectbox(
                "Select a paper to view details:",
                options=range(len(sample_data)),
                format_func=lambda x: f"{sample_data.iloc[x]['paper_title'][:80]}..." if len(sample_data.iloc[x]['paper_title']) > 80 else sample_data.iloc[x]['paper_title']
            )
            
            selected_paper = filtered_df.iloc[selected_index]
            with st.expander("View Paper Details", expanded=False):
                for col in filtered_df.columns:
                    if pd.notna(selected_paper[col]):
                        st.write(f"**{col.replace('_', ' ').title()}:** {selected_paper[col]}")
    else:
        st.info("No papers available for the selected filters")
    
    # Additional statistics
    st.subheader("Additional Statistics")
    if not filtered_df.empty:
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            if 'description_word_count' in filtered_df.columns:
                avg_word_count = filtered_df['description_word_count'].mean()
                st.metric("Avg Description Words", f"{avg_word_count:.1f}")
            else:
                st.metric("Papers Count", len(filtered_df))
        
        with col4:
            unique_orgs = filtered_df['source_organization'].nunique()
            st.metric("Unique Organizations", unique_orgs)
        
        with col5:
            papers_with_license = filtered_df['license'].notna().sum()
            st.metric("Papers with License", papers_with_license)
        
        with col6:
            recent_year_count = filtered_df[filtered_df['year'] == selected_years[1]]['year'].count()
            st.metric(f"Papers in {selected_years[1]}", recent_year_count)
    
    # Data export
    st.sidebar.header("Data Export")
    if st.sidebar.button("Download Filtered Data as CSV"):
        csv = filtered_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"cord19_filtered_{selected_years[0]}_{selected_years[1]}.csv",
            mime="text/csv"
        )

def create_sample_data():
    """Create sample data for demonstration"""
    import numpy as np
    
    np.random.seed(42)
    n_samples = 1000
    
    sample_data = {
        'paper_title': [f'COVID-19 Research Paper {i}' for i in range(n_samples)],
        'year': np.random.choice([2019, 2020, 2021, 2022], n_samples, p=[0.1, 0.3, 0.4, 0.2]),
        'source_organization': np.random.choice([
            'WHO', 'CDC', 'The Lancet', 'Nature', 'Science', 
            'BMJ', 'JAMA', 'NEJM', 'Elsevier', 'Springer'
        ], n_samples),
        'license': np.random.choice([
            'CC BY', 'CC BY-NC', 'CC BY-ND', 'CC BY-NC-ND', 'CC0'
        ], n_samples, p=[0.3, 0.2, 0.1, 0.1, 0.3]),
        'description_word_count': np.random.randint(50, 500, n_samples)
    }
    
    return pd.DataFrame(sample_data)

# Run the Streamlit app
if __name__ == "__main__":
    create_streamlit_app()
