import streamlit as st
from recommendation_function import (
    search_article,
    get_recommendations,
    df
)

#----- Page Setup -----#

st.set_page_config(
    page_title="Rekomendasi Artikel Jurnal Statistika",
    page_icon="📄",
    layout="wide",
)

#----- Session State Pagination -----#

if "page_number" not in st.session_state:

    st.session_state.page_number = 0

#----- CSS Styling -----#

st.markdown("""
<style>

/*----- Header Dropdown -----*/

.streamlit-expanderHeader{

    background-color:#FFF1E6;

    color:#1E293B;

    border:1px solid #F3D9C5;

    border-radius:14px;

    font-weight:600;
}

/*----- Isi Dropdown -----*/

div[data-testid="stExpanderDetails"]{

    background-color:#FFFFFF;

    border-left:1px solid #F3D9C5;

    border-right:1px solid #F3D9C5;

    border-bottom:1px solid #F3D9C5;

    border-radius:0px 0px 14px 14px;

    padding:18px;
}

/*----- Expander Container -----*/

div[data-testid="stExpander"]{

    border-radius:14px;

    overflow:hidden;

    box-shadow:0 2px 8px rgba(0,0,0,0.03);
}

/*----- Info Box -----*/

div[data-testid="stAlert"]{

    background-color:#C8D0BE;

    border:1px solid #2F3A2F;

    border-radius:14px;

    color:#2F3A2F;
}

div[data-testid="stAlert"] *{

    color:#2F3A2F;
}

</style>
""", unsafe_allow_html=True)

#----- Sidebar -----#

with st.sidebar:

    st.title(
        "Sistem Rekomendasi Artikel Jurnal Statistika"
    )

    st.caption(
        "Rekomendasi artikel berbasis "
        "TF-IDF dan Cosine Similarity"
    )

    st.divider()

    st.subheader(
        "Pengaturan Sistem"
    )

    option = st.selectbox(
        "Parameter Rekomendasi",
        (
            "Top-5 (Threshold 0,2)",
            "Top-20 (Threshold 0,1)"
        )
    )

    if option == "Top-5 (Threshold 0,2)":

        top_n = 5
        threshold = 0.2

    else:

        top_n = 20
        threshold = 0.1

    st.divider()

    st.subheader(
        "Informasi Parameter"
    )

    st.info(
        """
             - Parameter yang digunakan untuk mengatur sistem rekomendasi artikel jurnal ini berasal dari 
             hasil eksperimen yang dilakukan oleh penulis.
             - **Top-N**: Jumlah rekomendasi artikel yang ditampilkan.
             - **Threshold**: Batas minimum nilai *similarity* untuk artikel yang direkomendasikan.
             - **Example**: Jika threshold adalah 0.2, maka hanya artikel dengan nilai *similarity* di atas 0.2 yang akan direkomendasikan.   
        """
    )

#----- Main Page -----#

#----- Header -----#

st.title(
    "Sistem Rekomendasi Artikel Jurnal Statistika"
)

st.caption(
    "Rekomendasi artikel jurnal berbasis "
    "TF-IDF dan Cosine Similarity"
)
#----- Search Bar -----#

search_col, button_col = st.columns(
    [6,1]
)

with search_col:

    keyword = st.text_input(
        "",
        placeholder=
        "Masukkan kata kunci artikel..."
    )
st.info("Disarankan *input* judul atau kata kunci artikel menggunakan bahasa Inggris untuk hasil yang lebih relevan.")
with button_col:

    st.write("")

    search_button = st.button(
        "Cari",
        use_container_width=True
    )

#----- Top Section -----#

top_left, top_right = st.columns(
    [3,2],
    gap="large"
)

#=====================================================
# LEFT COLUMN
#=====================================================#

with top_left:

    st.subheader(
        f"Hasil Pencarian Artikel {keyword}"
    )

    #----- Sebelum Input -----#

    if not keyword:

        st.info(
            "Hasil pencarian artikel "
            "akan ditampilkan pada bagian ini."
        )

    #----- Setelah Input -----#

    else:

        result = search_article(keyword)

        #----- Reset Page Jika Search Baru -----#

        if "last_keyword" not in st.session_state:

            st.session_state.last_keyword = keyword

        if keyword != st.session_state.last_keyword:

            st.session_state.page_number = 0

            st.session_state.last_keyword = keyword

        st.caption(
            f"Menampilkan "
            f"{len(result)} hasil pencarian"
        )

        #----- Tidak Ada Hasil -----#

        if len(result) == 0:

            st.warning(
                "Artikel tidak ditemukan."
            )

        #----- Ada Hasil -----#

        else:

            #----- Pagination Setup -----#

            items_per_page = 5

            start_idx = (
                st.session_state.page_number
                * items_per_page
            )

            end_idx = (
                start_idx
                + items_per_page
            )

            paginated_result = result.iloc[
                start_idx:end_idx
            ]

            #----- Menampilkan Artikel -----#

            for i, row in enumerate(
                paginated_result.itertuples(),
                start=start_idx + 1
            ):

                with st.expander(
                    f"{i}. {row.judul_artikel}"
                ):

                    st.write(
                        f"**Kata Kunci:** "
                        f"{row.kata_kunci}"
                    )

                    st.write(
                        f"**Abstrak:** "
                        f"{row.abstrak[:700]}..."
                    )

            #----- Navigation Button -----#

            prev_col, middle_col, next_col = st.columns(
                [1,3,1]
            )

            #----- Tombol Sebelumnya -----#

            with prev_col:

                if st.button("<-"):

                    if st.session_state.page_number > 0:

                        st.session_state.page_number -= 1

                        st.rerun()

            #----- Informasi Halaman -----#

            with middle_col:

                total_page = (
                    len(result) - 1
                ) // items_per_page + 1

                st.markdown(
                    f"""
                    <div style='text-align:center'>
                    Halaman
                    {st.session_state.page_number + 1}
                    dari
                    {total_page}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            #----- Tombol Berikutnya -----#

            with next_col:

                if st.button("->"):

                    if end_idx < len(result):

                        st.session_state.page_number += 1

                        st.rerun()

#=====================================================
# RIGHT COLUMN
#=====================================================#

with top_right:

    st.subheader(
        f"Pilih Artikel Acuan"
    )

    #----- Sebelum Input -----#

    if not keyword:

        st.info(
            "Pilih artikel acuan "
            "untuk mendapatkan rekomendasi."
        )

    #----- Setelah Input -----#

    elif len(result) > 0:

        selected_title = st.selectbox(
            "Pilih Artikel",
            result["judul_artikel"].tolist()
        )

        selected_row = result[
            result["judul_artikel"]
            == selected_title
        ].iloc[0]

        selected_id = selected_row[
            "id_document"
        ]

        st.divider()

        st.subheader(
            "Informasi Artikel Acuan"
        )

        with st.expander(
            selected_row["judul_artikel"],
            expanded=True
        ):

            st.write(
                f"**Kata Kunci:** "
                f"{selected_row['kata_kunci']}"
            )

            st.write(
                f"**Abstrak:** "
                f"{selected_row['abstrak'][:1000]}..."
            )

#----- Bottom Section -----#

st.divider()

st.subheader(
    "Rekomendasi Artikel Acuan"
)

#----- Sebelum Input -----#

if not keyword:

    st.info(
        "Rekomendasi artikel "
        "akan ditampilkan pada bagian ini."
    )

#----- Setelah Input -----#

elif len(result) > 0:

    recommendation = get_recommendations(
        id_document=selected_id,
        top_n=top_n,
        threshold=threshold
    )

    st.caption(
        f"Top-{top_n} recommendation "
        f"dengan threshold {threshold}"
    )

    #----- Tidak Ada Rekomendasi -----#

    if len(recommendation) == 0:

        st.warning(
            "Tidak ada artikel "
            "yang memenuhi threshold."
        )

    #----- Ada Rekomendasi -----#

    else:

        for i, row in enumerate(
            recommendation.itertuples(),
            start=1
        ):

            with st.expander(
                f"{i}. {row.judul_artikel}"
            ):

                rec_col1, rec_col2 = st.columns(
                    [5,1]
                )

                #----- Informasi Artikel -----#

                with rec_col1:
                    st.write(
                        f"**Judul Artikel:** "
                        f"{row.judul_artikel}"
                    )
                    st.write(
                        f"**Kata Kunci:** "
                        f"{row.kata_kunci}"
                    )

                    st.write(
                        f"**Abstrak:** "
                        f"{row.abstrak[:700]}..."
                    )

                #----- Similarity Score -----#

                with rec_col2:

                    similarity_score = float(
                        row.similarity
                    )

                    st.success(
                        f"Similarity\n"
                        f"{similarity_score:.4f}"
                    )