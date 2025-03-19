import streamlit as st

if __name__ == "__main__":
    # Streamlit configs
    st.set_page_config(
        layout="wide",
        page_title="Movimentação de Clientes da Base",
    )
    st.markdown(
    """ 
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """,
        unsafe_allow_html=True,
    )

    move_advisory = st.Page(
        "pages/move_advisory.py",
        title="Clientes Base",
        icon=":material/play_circle:",
        default=True,
    )
    move_asset = st.Page(
        "pages/move_asset.py", title="Clientes Asset", icon=":material/play_circle:"
    )

    pg = st.navigation(
        {
            "Mover Clientes": [move_advisory, move_asset],
            # "Ferramentas": [compiled, results],
        }
    )

    pg.run()