# Fake News Detection System
A Machine Learning-powered web application that helps identify whether a news article is genuine or potentially fake. The project uses Natural Language Processing (NLP) and a trained classification model to analyze news content and provide credibility predictions through an interactive Streamlit interface.


📖 Project Overview:

The rapid spread of misinformation on the internet has made it difficult to distinguish between authentic and fake news. This project aims to address this issue by leveraging Machine Learning and NLP techniques to evaluate news articles and predict their authenticity.Users can enter news content into the application, and the system analyzes the text before generating a prediction


# Features:

- Fake News Detection using Machine Learning
- Text Analysis and Processing
- Interactive Streamlit Web Interface
- Real-Time Predictions
- User-Friendly Dashboard
- NLP-Based Feature Extraction


# Tech Stack:
-Frontend
-Streamlit
-Backend
-Python
-Machine Learning
-Scikit-learn
-Joblib
-Data Processing
-Pandas
-NumPy
-NLTK




# Project Structure:
Fake-news-Detection/
│
├── app.py                 # Main Streamlit application
├── app.ipynb              # Development notebook
├── model.pkl              # Trained model
├── lr_model.jb            # Logistic Regression model
├── vectorizer.jb          # Text vectorizer
├── requirements.txt       # Dependencies
├── .gitignore
└── README.md



# Installation
1. Clone the Repository
git clone <your-github-repository-url>
cd Fake-news-Detection
2. Create a Virtual Environment
python -m venv venv
Activate Environment
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt


# Running the Application

Start the Streamlit server:
streamlit run app.py

Open your browser and visit:
http://localhost:8501



# Workflow
-User enters a news article or headline.
-The text is preprocessed and cleaned.
-The vectorizer converts text into numerical features.
-The trained Machine Learning model analyzes the features.
-The system predicts whether the news is real or fake.
-Results are displayed through the Streamlit interface.




# Applications
-News Verification
-Media Monitoring
-Educational Research
-Fact-Checking Support
-Misinformation Detection


# Future Enhancements
-Integration with live news APIs
-Deep Learning Models (BERT, LSTM)
-Multi-language News Detection
-URL-Based News Verification
-Mobile Application Support
-Advanced Visualization Dashboard


# Developer
Snehashis Roy
Computer Science & Engineering Student

Interested in:
-Artificial Intelligence
-Machine Learning
-Web Development
-Data Science

# License
This project is developed for academic and educational purposes.
