 Movie Recommendation System using Machine Learning

##  Project Overview
This project is a Movie Recommendation System built using Python and Machine Learning.  
The system processes a dataset of 5000 movies, performs data cleaning, preprocessing, and feature engineering, and recommends movies based on similarity.

This project demonstrates real-world data handling and practical use of Scikit-Learn.


##  Key Features
- Processed and cleaned a dataset of 5000+ movies
- Handled missing and duplicate values
- Performed feature extraction for recommendation
- Implemented a content-based recommendation system
- Used cosine similarity for movie recommendations


##  Technologies & Libraries Used
- Python
- NumPy
- Pandas
- Scikit-Learn


##  Dataset Description
The dataset contains movie-related information such as:
- Movie title
- Genres
- Overview
- Keywords
- Cast and crew (if applicable)
Raw data was cleaned and transformed to make it suitable for machine learning.



## Data Preprocessing Steps
- Removed duplicate records
- Handled missing/null values
- Selected important features
- Combined text-based features
- Converted text data into numerical vectors


##  Machine Learning Approach
- Content-Based Filtering
- Vectorization of movie features
- Cosine Similarity to measure movie similarity
- Recommended top similar movies based on user input


##  Project Workflow
1. Data Collection
2. Data Cleaning
3. Data Preprocessing
4. Feature Engineering
5. Model Building
6. Movie Recommendation

---

##  How to Run the Project
```bash
git clone <your-github-repo-link>
cd movie-recommendation-system
pip install -r requirements.txt
python app.py
