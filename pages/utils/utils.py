import os
import pandas as pd

ADVISOR_ROLE_ID = os.environ.get("ADVISOR_ROLE_ID")
ADVISOR_RV_ROLE_ID = os.environ.get("ADVISOR_RV_ROLE_ID")

def sanitize_customers_roles(data: pd.DataFrame):
    customers_dict = data.set_index("code")["id"].to_dict()

    data_table = data[["code", "name", "advisor", "originator", "rv_advisor"]]
    data_table.columns = ["Código", "Cliente", "Assessor", "Originador", "Assessor RV"]

    return data_table, customers_dict


def get_roles_id(data: pd.DataFrame, customers_dict: set, collaborators: pd.DataFrame):
    collaborators_dict = collaborators.set_index("name")["collaborator_id"].to_dict()

    data["customer_id"] = data["Código"].apply(lambda x: customers_dict[x])
    data["advisor_id"] = data["Assessor"].apply(lambda x: collaborators_dict[x])
    data["rv_advisor_id"] = data["Assessor RV"].apply(lambda x: collaborators_dict[x])

    to_save_advisor = data[["customer_id", "advisor_id"]]
    to_save_advisor = to_save_advisor.rename(columns={"advisor_id": "collaborator_id"})
    to_save_advisor["role_id"] = ADVISOR_ROLE_ID

    to_save_rv = data[["customer_id", "rv_advisor_id"]]
    to_save_rv = to_save_rv.rename(columns={"rv_advisor_id": "collaborator_id"})
    to_save_rv["role_id"] = ADVISOR_RV_ROLE_ID

    return to_save_advisor, to_save_rv