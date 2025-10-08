import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_style('whitegrid')
pd.set_option('display.max_columns', None)

def load_and_explore_data(file_path):
    """Load data and perform initial exploration"""
    df = pd.read_csv(file_path)
    
    print("=== DATASET EXPLORATION ===")
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumn names: {df.columns.tolist()}")
    print(f"\nData types:\n{df.dtypes}")
    
    # Check for missing values
    missing_data = df.isnull().sum()
    missing_percentage = (missing_data / len(df)) * 100
    print(f"\nMissing values (>0%):")
    print(missing_percentage[missing_percentage > 0].sort_values(ascending=False))
    
    # Basic statistics for numerical columns
    print("\nBasic statistics for numerical columns:")
    print(df.describe())
    
    return df

def clean_data(df):
    """Clean and preprocess the dataset"""
    df_clean = df.copy()
    
    # Drop columns with more than 50% missing values
    missing_percentage = (df_clean.isnull().sum() / len(df_clean)) * 100
    cols_to_drop = missing_percentage[missing_percentage > 50].index
    df_clean.drop(columns=cols_to_drop, inplace=True)
    print(f"\nDropped columns (>50% missing): {cols_to_drop.tolist()}")
    print(f"Remaining columns: {df_clean.columns.tolist()}")
    
    # Fill missing values
    if 'author_list' in df_clean.columns:
        df_clean['author_list'] = df_clean['author_list'].fillna('Unknown')
    
    # Extract year from date columns
    date_columns = ['last_updated', 'publication_date', 'date']
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[f'{col}_year'] = df_clean[col].apply(extract_year)
    
    # Create word count features
    text_columns = ['description', 'paper_title', 'abstract']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[f'{col}_word_count'] = df_clean[col].apply(get_word_count)
    
    print(f"\nCleaned dataset info:")
    print(f"Rows: {df_clean.shape[0]}, Columns: {df_clean.shape[1]}")
    
    return df_clean

def extract_year(date_str):
    """Extract year from various date formats"""
    try:
        if pd.isna(date_str):
            return None
        if isinstance(date_str, str):
            year_match = re.search(r'(\d{4})', str(date_str))
            if year_match:
                year = int(year_match.group(1))
                # Basic validation for reasonable years
                if 1900 <= year <= 2024:
                    return year
        return None
    except:
        return None

def get_word_count(text):
    """Count words in text"""
    if pd.isna(text):
        return 0
    if isinstance(text, str):
        return len(text.split())
    return 0

def analyze_data(df):
    """Perform comprehensive data analysis"""
    print("\n" + "="*50)
    print("COMPREHENSIVE DATA ANALYSIS")
    print("="*50)
    
    # Year analysis
    year_cols = [col for col in df.columns if 'year' in col]
    for year_col in year_cols:
        if year_col in df.columns:
            year_counts = df[year_col].value_counts().sort_index()
            print(f"\n📊 Papers by {year_col}:")
            print(year_counts)
            print(f"Year range: {df[year_col].min()} - {df[year_col].max()}")
    
    # Source organization analysis
    if 'source_organization' in df.columns:
        source_counts = df['source_organization'].value_counts().head(15)
        print(f"\n🏢 Top 15 source organizations:")
        for org, count in source_counts.items():
            print(f"  {org}: {count} papers")
    
    # Author analysis
    if 'author_list' in df.columns:
        # Count papers with known authors
        known_authors = df[df['author_list'] != 'Unknown']
        print(f"\n👥 Author Statistics:")
        print(f"  Papers with known authors: {len(known_authors)} ({len(known_authors)/len(df)*100:.1f}%)")
        print(f"  Papers with unknown authors: {len(df) - len(known_authors)} ({(len(df) - len(known_authors))/len(df)*100:.1f}%)")
    
    # Text analysis
    if 'paper_title' in df.columns:
        all_titles = ' '.join(df['paper_title'].dropna().astype(str))
        # Filter out common stop words and short words
        stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'as', 'by', 'an', 'at'}
        title_words = [word.lower() for word in all_titles.split() 
                      if len(word) > 3 and word.lower() not in stop_words]
        word_freq = Counter(title_words)
        print(f"\n📝 Top 20 meaningful words in paper titles:")
        for word, count in word_freq.most_common(20):
            print(f"  {word}: {count}")
    
    # License analysis
    if 'license' in df.columns:
        license_counts = df['license'].value_counts()
        print(f"\n📄 Papers by license type:")
        for license_type, count in license_counts.items():
            print(f"  {license_type}: {count} papers")
    
    # Word count analysis
    word_count_cols = [col for col in df.columns if 'word_count' in col]
    for col in word_count_cols:
        if col in df.columns:
            stats = df[col].describe()
            print(f"\n📊 {col.replace('_', ' ').title()} Statistics:")
            print(f"  Mean: {stats['mean']:.1f}")
            print(f"  Median: {stats['50%']:.1f}")
            print(f"  Max: {stats['max']:.1f}")
            print(f"  Min: {stats['min']:.1f}")

def create_visualizations(df):
    """Create comprehensive visualizations"""
    print("\n📈 Generating visualizations...")
    
    fig = plt.figure(figsize=(20, 16))
    
    # Plot 1: Publications by year
    ax1 = plt.subplot(3, 3, 1)
    year_cols = [col for col in df.columns if 'year' in col]
    if year_cols and df[year_cols[0]].notna().sum() > 0:
        year_counts = df[year_cols[0]].value_counts().sort_index()
        plt.bar(year_counts.index, year_counts.values, color='skyblue', alpha=0.7, edgecolor='navy')
        plt.title('Publications by Year', fontsize=14, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Number of Papers')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
    
    # Plot 2: Top source organizations
    ax2 = plt.subplot(3, 3, 2)
    if 'source_organization' in df.columns:
        source_counts = df['source_organization'].value_counts().head(10)
        y_pos = np.arange(len(source_counts))
        plt.barh(y_pos, source_counts.values, color='lightgreen', alpha=0.7, edgecolor='darkgreen')
        plt.yticks(y_pos, source_counts.index)
        plt.title('Top 10 Source Organizations', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Papers')
        plt.grid(True, alpha=0.3)
    
    # Plot 3: Word cloud of paper titles
    ax3 = plt.subplot(3, 3, 3)
    if 'paper_title' in df.columns:
        all_titles = ' '.join(df['paper_title'].dropna().astype(str))
        wordcloud = WordCloud(width=600, height=300, background_color='white', 
                             max_words=100, colormap='viridis', 
                             stopwords={'the', 'and', 'of', 'in', 'to', 'a'}).generate(all_titles)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title('Word Cloud of Paper Titles', fontsize=14, fontweight='bold')
        plt.axis('off')
    
    # Plot 4: Description word count distribution
    ax4 = plt.subplot(3, 3, 4)
    if 'description_word_count' in df.columns:
        plt.hist(df['description_word_count'], bins=30, color='orange', alpha=0.7, edgecolor='darkorange')
        plt.title('Description Word Count Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
    
    # Plot 5: License distribution
    ax5 = plt.subplot(3, 3, 5)
    if 'license' in df.columns:
        license_counts = df['license'].value_counts().head(8)
        colors = plt.cm.Set3(np.linspace(0, 1, len(license_counts)))
        plt.pie(license_counts.values, labels=license_counts.index, autopct='%1.1f%%', 
                startangle=90, colors=colors, textprops={'fontsize': 10})
        plt.title('Distribution by License Type', fontsize=14, fontweight='bold')
    
    # Plot 6: Temporal trend
    ax6 = plt.subplot(3, 3, 6)
    if year_cols and len(year_counts) > 1:
        plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=2, 
                markersize=6, color='red', alpha=0.7)
        plt.title('Publication Trend Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Number of Papers')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
    
    # Plot 7: Papers with known vs unknown authors
    ax7 = plt.subplot(3, 3, 7)
    if 'author_list' in df.columns:
        known_authors = (df['author_list'] != 'Unknown').sum()
        unknown_authors = len(df) - known_authors
        labels = ['Known Authors', 'Unknown Authors']
        sizes = [known_authors, unknown_authors]
        colors = ['lightblue', 'lightcoral']
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Author Information Availability', fontsize=14, fontweight='bold')
    
    # Plot 8: Top 10 words in titles (bar chart)
    ax8 = plt.subplot(3, 3, 8)
    if 'paper_title' in df.columns:
        all_titles = ' '.join(df['paper_title'].dropna().astype(str))
        stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'as', 'by', 'an', 'at'}
        title_words = [word.lower() for word in all_titles.split() 
                      if len(word) > 3 and word.lower() not in stop_words]
        word_freq = Counter(title_words)
        top_words = word_freq.most_common(10)
        
        words = [word[0] for word in top_words]
        counts = [word[1] for word in top_words]
        
        y_pos = np.arange(len(words))
        plt.barh(y_pos, counts, color='purple', alpha=0.7)
        plt.yticks(y_pos, words)
        plt.title('Top 10 Words in Titles', fontsize=14, fontweight='bold')
        plt.xlabel('Frequency')
    
    # Plot 9: Box plot of word counts
    ax9 = plt.subplot(3, 3, 9)
    word_count_cols = [col for col in df.columns if 'word_count' in col]
    if word_count_cols:
        word_count_data = [df[col].dropna() for col in word_count_cols]
        labels = [col.replace('_word_count', '').title() for col in word_count_cols]
        plt.boxplot(word_count_data, labels=labels)
        plt.title('Word Count Distribution by Text Type', fontsize=14, fontweight='bold')
        plt.ylabel('Word Count')
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Visualizations completed!")

def generate_summary_report(df):
    """Generate a comprehensive summary report"""
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    
    print(f"\n📋 Dataset Overview:")
    print(f"  • Total papers: {len(df):,}")
    print(f"  • Total columns: {df.shape[1]}")
    print(f"  • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Year summary
    year_cols = [col for col in df.columns if 'year' in col]
    if year_cols:
        year_data = df[year_cols[0]].dropna()
        print(f"\n📅 Temporal Analysis:")
        print(f"  • Coverage: {int(year_data.min())} - {int(year_data.max())}")
        print(f"  • Most productive year: {year_data.mode().iloc[0] if not year_data.mode().empty else 'N/A'}")
        print(f"  • Papers with year info: {len(year_data)} ({len(year_data)/len(df)*100:.1f}%)")
    
    # Content analysis
    print(f"\n📊 Content Analysis:")
    if 'description_word_count' in df.columns:
        desc_stats = df['description_word_count'].describe()
        print(f"  • Average description length: {desc_stats['mean']:.1f} words")
        print(f"  • Longest description: {desc_stats['max']:.0f} words")
    
    if 'paper_title_word_count' in df.columns:
        title_stats = df['paper_title_word_count'].describe()
        print(f"  • Average title length: {title_stats['mean']:.1f} words")
    
    # Source diversity
    if 'source_organization' in df.columns:
        unique_sources = df['source_organization'].nunique()
        print(f"  • Unique source organizations: {unique_sources}")
    
    print(f"\n✅ Analysis complete! The dataset contains valuable insights into COVID-19 research trends.")

# Main execution
if __name__ == "__main__":
    # Load and explore data
    print("🚀 Starting CORD-19 Dataset Analysis...")
    df = load_and_explore_data('CORD19 datasets - Sheet 1.csv')
    
    # Clean data
    df_clean = clean_data(df)
    
    # Analyze data
    analyze_data(df_clean)
    
    # Create visualizations
    create_visualizations(df_clean)
    
    # Generate summary report
    generate_summary_report(df_clean)
