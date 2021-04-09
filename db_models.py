from mongoengine import Document, StringField, URLField, IntField, FloatField, BooleanField, ObjectIdField


class MainReturn(Document):
    source = URLField()
    # Essentials
    ein = StringField(required=True)
    tax_year = IntField(required=True)
    name = StringField()
    other_names = StringField()
    defunct = BooleanField()
    url = StringField()
    address_street = StringField()
    address_city = StringField()
    address_state = StringField()
    address_zip = StringField()
    address_country = StringField()
    year_of_formation = StringField()
    return_type = StringField()
    org_type = StringField()
    
    # Financials
    number_employees = StringField()
    number_volunteers = StringField()
    operate_local_branches = BooleanField()
    total_revenue = StringField()
    total_expenses = StringField()
    total_assets = StringField()
    net_assets = StringField()
    foreign_fundraising = BooleanField()
    foreign_grants_to_orgs = BooleanField()
    foreign_grants_to_individuals = BooleanField()
    foreign_grants_amount = StringField()
    foreign_bank_account = BooleanField()
    payments_to_govt_officials = BooleanField()
    government_grants = StringField()
    total_lobbying_amount = StringField()
    total_legal_spending = StringField()
    # Preparer
    preparer_firm = StringField()
    preparer_ein = StringField()
    preparer_address_street = StringField()
    preparer_address_city = StringField()
    preparer_address_state = StringField()
    preparer_address_zip = StringField()
    preparer_name = StringField()
    preparer_ptin = StringField()



class Grants(Document):
    related_org = ObjectIdField()
    grantor_name = StringField()
    grant_year = IntField()
    grantee = StringField()
    grantee_address = StringField()
    grantee_ein = StringField()
    grantee_org_type = StringField()
    cash_amount = StringField()
    non_cash_amount = StringField()
    cash_purpose = StringField()
    non_cash_purpose = StringField()
    source = StringField()

    # Essentials
    # org_id=org.rec_id,
    # org_ein=org.ein,
    # irs_ein=irs_ein,
    # tax_year=tax_year,
    # irs_name=irs_name,
    # irs_other_names=irs_other_name,
    # irs_defunct=irs_defunct,
    # irs_url=irs_url,
    # irs_street=irs_street,
    # irs_city=irs_city,
    # irs_state=irs_state,
    # irs_zip=irs_zip,
    # irs_country=irs_country,
    # irs_phone_number=irs_phone_number,
    # irs_year_of_formation=irs_year_of_formation,
    # irs_return_type=irs_return_type,
    # fellow_traveler=org.fellow_traveler,
    # irs_org_type=irs_org_type,

    # Financials
    # (rec_id=record_id, irs_name=org_name, irs_ein=ein,
    # tax_year=date_of_990, employees_number=employees_number,
    # volunteers_number=volunteers_number, total_revenue=total_revenue, total_expenses=total_expenses,
    # total_assets=total_assets, net_assets=net_assets,
    # campaign_or_legislation_involvement=campaign_or_legislation_involvement,
    # over_100_for_political_purposes=over_100_for_political_purposes,
    # foreign_fundraising=foreign_fundraising,
    # foreign_grants_to_orgs=foreign_grants_to_orgs,
    # foreign_grants_to_individuals=foreign_grants_to_individuals,
    # operate_local_branches=operate_local_branches, foreign_grants=foreign_grants,
    # foreign_bank_account=foreign_bank_account, payments_to_govt_officials=payments_to_govt_officials,
    # government_grants=government_grants, total_lobbying_amount=total_lobbying_amount,
    # total_legal_spending=total_legal_spending, xml_year=xml_year, source=xml_url,
    # fellow_traveler=org.fellow_traveler)

    # Preparer
    # org_id=org.rec_id,
    # org_ein=org.ein,
    # tax_year=tax_year,
    # irs_name=irs_name,
    # preparer_firm=preparer_firm,
    # preparer_ein=preparer_ein,
    # preparer_address_street=preparer_address_street,
    # preparer_address_city=preparer_address_city,
    # preparer_address_state=preparer_address_state,
    # preparer_address_zip=preparer_address_zip,
    # preparer_name=preparer_name,
    # preparer_phone=preparer_phone,
    # preparer_ptin=preparer_ptin,
    # source=url
