import io

from PIL import Image
import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import os
from io import BytesIO
import json 
from PIL import Image # type: ignore
try:
    import pdfkit  # type: ignore
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False
from tempfile import NamedTemporaryFile



# Set page configuration
st.set_page_config(page_title="Mobile Data Sweeper", layout="wide")

# Sidebar for settings

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # Theme selection
    theme = st.radio("Choose Theme:", [ "Dark Black","Dark Gray",])

    # Add more interactive elements
    st.markdown("---")
    st.markdown("### 📂 File Management")
    st.button("🔄 Refresh Data")
    st.button("🗑 Clear Cache")

    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    st.checkbox("Show Data Overview")
    st.checkbox("Enable Auto-Cleaning")

    st.markdown("---")
    st.markdown("👤 **User Profile**")
    st.text_input("Enter your name:")
    st.button("Save Settings")

# Apply selected theme styles
if theme == "Dark Gray":
    bg_color = "#424242"  # Dark Gray
    text_color = "white"
    sidebar_bg = "#BDBDBD"  # Light Gray for sidebar
    sidebar_text_color = "#212121"  # Darker Gray for readability
    button_text_color = "#212121"  # Dark text for buttons (on light sidebar)
elif theme == "Dark Black":
    bg_color = "#121212"  # Dark Black
    text_color = "white"
    sidebar_bg = "#2C2C2C"  # Light Black for sidebar
    sidebar_text_color = "#F5F5F5"  # Light Gray for contrast
    button_text_color = "#FFFFFF"  # White text for buttons (on dark sidebar)



# 🎨 Custom CSS for White Multiselect Label
# Custom CSS for White Text in Labels, Checkboxes, and Radio Buttons
st.markdown("""
    <style>
        div[data-testid="stMultiSelect"] label,
        div[role="radiogroup"] label,
        div[role="checkbox"] label {
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Apply CSS styles dynamically
st.markdown(
    f"""
    <style>
        /* Main page background */
        .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}

        /* Sidebar background */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
        }}

        /* Sidebar text */
        section[data-testid="stSidebar"] * {{
            color: {sidebar_text_color} !important;
        }}

        /* Buttons inside the sidebar */
        section[data-testid="stSidebar"] button {{
            color: {button_text_color} !important;
        }}

        /* Vibrant Gradient Title */
        .gradient-title {{
            font-size: 250px; /* Large but realistic font size */
            font-weight: bold;
            text-align: left;
            letter-spacing: 5px; /* Spacing for a premium look */
            background: linear-gradient(90deg, #00008B, #1E90FF, #800080, #FF00FF, #FF1493, #9400D3); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            padding: 22px 0;
            text-shadow: 5px 5px 20px rgba(255, 0, 255, 0.6); /* Soft glow effect */
        }}

        /* Gradient Description */
        .gradient-description {{
            font-size: 50px; /* Readable yet stylish */
            font-weight: bold;
            text-align: left;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #4682B4, #87CEFA, #1E90FF, #00BFFF, #5F9EA0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            padding: 10px 0;
            text-shadow: 2px 2px 10px rgba(30, 144, 255, 0.5); /* Soft glow */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Create two columns
col1, col2 = st.columns([1, 1])  # Equal width columns for better balance

with col1:
   image_path = os.path.abspath("public/mobile.png")

try:
    if os.path.exists(image_path):  # Check if file exists
        image = Image.open(image_path)
        st.image(image, width=600)  # Display image
    else:
        st.error(f"❌ Error: Image '{image_path}' not found! Please check the path.")
except Exception as e:
    st.error(f"⚠️ Error loading image: {str(e)}")


with col2:
    # Display title and description in the second column
    st.markdown('<h1 class="gradient-title">📱 Mobile Data Sweeper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-description">A powerful tool to clean and manage your mobile data efficiently.</p>', unsafe_allow_html=True)



st.markdown('<h1 class="gradient-title"> Sterling Integrator</h1>', unsafe_allow_html=True)
st.markdown('<p class="gradient-description">Transform your files between CSV and Excel formats with built-in data cleaning and visualization.</p>', unsafe_allow_html=True)
# File Upload
uploaded_files = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_name = file.name
        file_ext = os.path.splitext(file_name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file format: {file_ext}. Please upload a CSV or Excel file.")
            continue

        # Show DataFrame
        st.subheader(f"📂 Preview of {file_name}")
        st.write(f"✅ Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        st.dataframe(df, use_container_width=True)

        # Data Cleaning Options
        st.subheader("🔧 Data Cleaning Options")

        if st.checkbox(f"✔️ Clean data for {file_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates from {file_name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed successfully!")
                    st.dataframe(df, use_container_width=True)

            with col2:
                if st.button(f"🩹 Handle Missing Values in {file_name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")
                    st.dataframe(df, use_container_width=True)
        
        # Column Selection
        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns for {file_name}", df.columns, default=df.columns)
        df_filtered = df[columns]
        st.dataframe(df_filtered, use_container_width=True)



        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file_name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2], use_container_width=True, height=200)




# File uploader
file = st.file_uploader("Upload your file", type=["csv", "xlsx"])

if file:
    file_ext = file.name.split(".")[-1]  # Extract file extension
    df = pd.read_csv(file) if file_ext == "csv" else pd.read_excel(file)

    st.markdown("""
    <style>
    .gradient-text {
        font-size: 40px;
        font-weight: bold;
        background: linear-gradient(to right, #00008B, #FF1493, #8B008B, #ADD8E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    </style>
    <p class="gradient-text"   style="font-size: 60px;"> Convert Data Format</p>
""", unsafe_allow_html=True)


    # Custom Gradient Styling (Dark Blue, Dark Pink, Magenta, Light Blue)
    st.markdown("""
        <style>
        .gradient-text {
            font-size: 38px;
            font-weight: bold;
            background: linear-gradient(to right, #00008B, #FF1493, #8B008B, #ADD8E6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        .gradient-list li {
            font-size: 40px;
            font-weight: bold;
            background: linear-gradient(to right, #00008B, #FF1493, #8B008B, #ADD8E6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        </style>
       <p class="gradient-text" style="font-size: 40px;">Available Formats:</p>
        <ul class="gradient-list">
            <li><b>CSV:</b> csv</li>
            <li><b>Excel:</b> xlsx</li>
            <li><b>PDF:</b> pdf</li>
            <li><b>JSON:</b> json</li>
            <li><b>Parquet:</b> parquet</li>
            <li><b>HTML Table:</b> html</li>
        </ul>
    """, unsafe_allow_html=True)






            
  
    # Apply CSS styling to make radio button text white
    st.markdown(
        """
        <style>
            div[role="radiogroup"] label {
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Radio button for conversion selection
    conversion_type = st.radio(
        "🔄 Choose Format:",
        ["CSV", "Excel", "JSON","pdf", "Parquet", "HTML Table"], 
        key=file.name
    )

    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        file_name = ""  # Initialize file_name variable
        mime_type = "application/octet-stream"  # Default mime type

        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(f".{file_ext}", ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False, engine='openpyxl')
            file_name = file.name.replace(f".{file_ext}", ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        elif conversion_type == "PDF":
            mime_type = "application/pdf"
            if not PDFKIT_AVAILABLE:
                st.error("PDF conversion is not available. Please install pdfkit and wkhtmltopdf.")
                st.info("Run: pip install pdfkit")
                st.info("And install wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html")
                st.stop()
                
            # Convert DataFrame to HTML first
            html = df.to_html(index=False)
            
            # Create a temporary HTML file
            with NamedTemporaryFile(suffix='.html', delete=False) as f:
                f.write(html.encode('utf-8'))
                temp_html = f.name
            
            try:
                # Convert HTML to PDF
                pdf = pdfkit.from_file(temp_html, False)
                buffer.write(pdf)
            except Exception as e:
                st.error(f"PDF conversion failed: {str(e)}")
                st.info("Please ensure wkhtmltopdf is installed on your system.")
            finally:
                # Clean up temporary file
                os.unlink(temp_html)
            file_name = file.name.replace(f".{file_ext}", ".pdf")

        elif conversion_type == "JSON":
            buffer.write(df.to_json(orient="records").encode())
            file_name = file.name.replace(f".{file_ext}", ".json")
            mime_type = "application/json"

        elif conversion_type == "Parquet":
            df.to_parquet(buffer, index=False)
            file_name = file.name.replace(f".{file_ext}", ".parquet")
            mime_type = "application/octet-stream"

        elif conversion_type == "HTML Table":
            buffer.write(df.to_html(index=False).encode())
            file_name = file.name.replace(f".{file_ext}", ".html")
            mime_type = "text/html"

        buffer.seek(0)  # Reset buffer position

        # Move download button inside the conversion logic
        st.download_button(
            label=f"Download {file_name}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

        st.success("File conversion successful!")
# Custom CSS for gradient text
st.markdown(
    """
    <style>
    .gradient-text {
        font-size: 8px;  /* Adjust font size here */
        font-weight: small;
        background: linear-gradient(to right, #00008B, #FF1493, #8B008B, #ADD8E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with gradient text
st.markdown('<h5 class="gradient-text">Built By NOUSHEEN ATIF</h5>', unsafe_allow_html=True)
