import os
import json
import pandas as pd

ADVISOR_ROLE_ID = os.environ.get("ADVISOR_ROLE_ID")
ADVISOR_RV_ROLE_ID = os.environ.get("ADVISOR_RV_ROLE_ID")
CUSTOMER_FILTER_NAMES_LIST = os.environ.get("CUSTOMER_FILTER_NAMES_LIST")

CUSTOMER_FILTER_NAMES = json.loads(CUSTOMER_FILTER_NAMES_LIST)

def sanitize_customers(data: pd.DataFrame):
    data_table = data[CUSTOMER_FILTER_NAMES]
    data_table.columns = ["Código", "Cliente", "Assessor", "Originador", "Assessor RV"]

    customers_dict = data.set_index("Código")["id"].to_dict()
    return data_table, customers_dict


def get_ids(data: pd.DataFrame, customers_dict: set, collaborators: pd.DataFrame):
    collaborators_dict = collaborators.set_index("short_name")["collaborator_id"].to_dict()

    data["customer_id"] = data["Código"].apply(lambda x: customers_dict.get(x, None))
    data["advisor_id"] = data["Assessor"].apply(lambda x: collaborators_dict.get(x, None))
    data["rv_advisor_id"] = data["Assessor RV"].apply(lambda x: collaborators_dict.get(x, None))

    to_save_advisor = data[["customer_id", "advisor_id"]]
    to_save_advisor = to_save_advisor.rename(columns={"advisor_id": "collaborator_id"})
    to_save_advisor["role_id"] = ADVISOR_ROLE_ID
    to_save_advisor = to_save_advisor.dropna(subset=["collaborator_id"])

    to_save_rv = data[["customer_id", "rv_advisor_id"]]
    to_save_rv = to_save_rv.rename(columns={"rv_advisor_id": "collaborator_id"})
    to_save_rv["role_id"] = ADVISOR_RV_ROLE_ID
    to_save_rv = to_save_rv.dropna(subset=["collaborator_id"])

    return to_save_advisor, to_save_rv