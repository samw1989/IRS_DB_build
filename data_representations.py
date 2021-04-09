from collections import namedtuple

essentials_fieldnames = [
    "ein",
    "tax_year",
    "name",
    "other_names",
    "defunct",
    "url",
    "street",
    "city",
    "state",
    "zip",
    "country",
    "year_of_formation",
    "return_type",
    "org_type"
]


financials_fieldnames = [
    "employees_number",
    "volunteers_number",
    "operate_local_branches",
    "total_revenue",
    "total_expenses",
    "total_assets",
    "net_assets",
    "foreign_fundraising",
    "foreign_grants_to_orgs",
    "foreign_grants_to_individuals",
    "foreign_grants_amount",
    "foreign_bank_account",
    "payments_to_govt_officials",
    "government_grants",
    "total_lobbying_amount",
    "total_legal_spending",
]

grants_fieldnames = [
    "grantee_name",
    "grantee_address",
    "grantee_ein",
    "grantee_org_type",
    "cash_amount",
    "non_cash_amount",
    "cash_purpose",
    "non_cash_purpose",
]

preparer_fieldnames = [
    "preparer_firm",
    "preparer_ein",
    "preparer_address_street",
    "preparer_address_city",
    "preparer_address_state",
    "preparer_address_zip",
    "preparer_name",
    "preparer_ptin",
]


Essentials = namedtuple("essentials_match", essentials_fieldnames)
Financials = namedtuple("financials_match", financials_fieldnames)
Grants = namedtuple("grants_match", grants_fieldnames)
Preparer = namedtuple("preparer_match", preparer_fieldnames)
