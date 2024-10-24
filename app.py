import streamlit as st 
import numpy as np
import pandas as pd
import faiss
import warnings
import base64
from PIL import Image,ImageFilter

# image  = Image.open("manga_background.jpg")
# blurred_img  = image.filter(ImageFilter.GaussianBlur())
# blurred_img.save("bg_blurred.png")
# image_base64 = base64.b64encode(blurred_img).decode()
warnings.filterwarnings("ignore")
from utils import convert_genre_to_str,recommend,display_results

st.set_page_config(layout="wide")

##Loading embeddings, Faiss index, Dataset
data = pd.read_csv("dataset\manga_dataset.csv")
embeddings = np.load("models\embeddings_pca.npy")
index = faiss.read_index("models/faiss_index.bin")
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"gif"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )


# add_bg_from_local("manga_background.jpg")   


# # Function to encode the image file as base64
# def get_base64_image(image_path):
#     with open(image_path, "rb") as file:
#         data = file.read()
#     return base64.b64encode(data).decode()

# # Path to your background image
# image_path = "bg_blurred.png"

# # Convert the image to base64
# image_base64 = get_base64_image(image_path)

# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{image_base64}");
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )



data["genres"] = data["genres"].apply(convert_genre_to_str)
#Creating a class container where there will be a sction whose background will be white
# st.markdown("""
#     <style>
#     .container {
#         padding: 16px;
#         border: 1px solid #ddd;
#         border-radius: 5px;
#         background-color: #f5f5f5;
#         margin-bottom: 16px;
#     }
#     </style>
# """, unsafe_allow_html=True)

st.write('<h1 style = "color:black;">Manga Mind - An AI Based Recommender System',unsafe_allow_html=True)
titles = data["title"].tolist()

title = st.selectbox(label = "Select a manga you've read",options=titles,placeholder="One Piece")
min_score = st.slider("Select the minimum score for the mangas to be recommended: ",min_value= 5.00,max_value=9.00,value= 7.00)

top_n = 5
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



