import streamlit as st 
import numpy as np
import pandas as pd
import faiss
import warnings
from utils import convert_genre_to_str,recommend,display_results
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")

##Loading embeddings, Faiss index, Dataset
data = pd.read_csv("dataset/manga_dataset.csv")
embeddings = np.load("models/embeddings_pca.npy")
index = faiss.read_index("models/faiss_index.bin")


data["genres"] = data["genres"].apply(convert_genre_to_str)

st.title('Manga Mind - An AI Based Recommender System')
titles = data["title"].tolist()

title = st.selectbox(label = "Select a manga you've read",options=titles,placeholder="One Piece")
min_score = st.slider("Select the minimum score for the mangas to be recommended: ",min_value= 5.00,max_value=9.00,value= 7.00)

top_n = 6
# Custom CSS to increase button size
st.markdown(
    """
    <style>
    .stButton {
        display: flex;
        justify-content: center; /* Center the button horizontally */
        margin-top: 20px; /* Optional: Add some margin on top */
    }
    .stButton button {
        font-size: 20px; /* Adjust the font size */
        padding: 15px 30px; /* Adjust the padding for height and width */
    }
    </style>
    """,
    unsafe_allow_html=True
)


if st.button("Recommend"):
    filtered_mangas= recommend(manga_name=title,index=index,data=data,embeddings= embeddings,min_score = min_score)
    display_results(filtered_mangas[:top_n])
    st.success(body="Success")



