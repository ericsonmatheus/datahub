import os
import streamlit as st
import pandas as pd

from pages.services.database import Advisory
from pages.utils.utils import sanitize_customers_roles, get_roles_id

from dotenv import load_dotenv
load_dotenv()

# Create connection
advisory_conn = os.environ.get("ADVISORY_DB")
advisory = Advisory(advisory_conn)

# Generate data
customers_roles = advisory.get_customers()
collaborators = advisory.get_collaborators()
customers_table, customers_dict = sanitize_customers_roles(customers_roles)


st.subheader("Movimentação de Clientes da Base")
st.write(
    "Os dados se referem a todos os clientes presentes na empresa "
    "e seus respectivos representantes."
)
options_to_collaborators = list(collaborators["short_name"].sort_values())

column_configuration = {
    "Assessor": st.column_config.SelectboxColumn(
        "Assessor", options=options_to_collaborators
    ),
    "Originador": st.column_config.SelectboxColumn(
        "Originador", options=options_to_collaborators
    ),
    "Assessor RV": st.column_config.SelectboxColumn(
        "Assessor RV", options=options_to_collaborators
    ),
}
customers_table_edited = st.data_editor(
    customers_table,
    column_config=column_configuration,
    use_container_width=True,
    num_rows="fixed",
)

merged = pd.merge(customers_table, customers_table_edited, how='outer', indicator=True)

df_diff = merged[merged['_merge'] == 'right_only'].drop('_merge', axis=1)

st.subheader("Validação de Movimentações")
st.write(
    "Valide todos as alterações a serem realizadas antes de continuar."
)
st.dataframe(df_diff)

if st.button("Salvar Alterações"):
    customers_to_save_advisor, customers_to_save_rv = get_roles_id(df_diff, customers_dict, collaborators)
    if not customers_to_save_advisor.empty:
        advisory.save_customers_collaborators(customers_to_save_advisor)
    if not customers_to_save_rv.empty:
        advisory.save_customers_collaborators(customers_to_save_rv)
    
    st.success("Salvo com Sucesso")