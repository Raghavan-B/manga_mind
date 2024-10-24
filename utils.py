import streamlit as st
def recommend(manga_name,data,index,embeddings,min_score):
    manga_idx = data[data["title"] == manga_name].index[0]
    query_embedding = embeddings[manga_idx].reshape(1,-1)
    _,indices = index.search(query_embedding,k = 5000)
    filtered_mangas = data.iloc[indices[0][1:]]
    sorted_by_scores_df = filtered_mangas.query(f"score>={min_score}")
    return sorted_by_scores_df

def convert_genre_to_str(row):
    row = row.replace(",,", ",")
    row = [x.strip().replace("'", "").replace('"', "") for x in row.strip('[]').split(',') if x.strip()]
    return ", ".join(row)


def display_results(manga_df):
    manga_len = len(manga_df)
    for i in range(0,manga_len,3):
        cols = st.columns(3)
        for j,col in enumerate(cols):
            if i+j<manga_len:
                manga = manga_df.iloc[i+j]

                ##display the information in each column
                with col:
                    genres = manga["genres"]
                    authors = str(manga["authors"]).strip("[]")
                    st.subheader(manga['title'])
                    with st.columns(3)[1]:
                        st.image(manga["image_url"],width = 150)
                    st.write(f"Genres : {genres}")
                    st.write(f"Synopsis : {manga['synopsis'][:-24]}")
                    st.write(f"Authors : {authors}")
        st.write("--"*100)
