from data_representations import Essentials, Financials, Preparer, Grants


def essentials(xml_data):
    subsoup = xml_data.find("filer")

    tax_year = xml_data.find(['taxyr', 'taxyear'])
    tax_year = tax_year.get_text() if tax_year else None

    ein = subsoup.find("ein").get_text()

    name = subsoup.find(["businessnameline1txt", "businessnameline1"]).get_text()

    other_names = subsoup.find(["doingbusinessasname", "doingbusinessas"])
    other_names = other_names.get_text if other_names else ""

    defunct = xml_data.find(
        [
            "terminateoperationsind",
            "terminated",
            "organizationdissolvedetcind",
            "organizationdissolvedetc",
        ]
    )
    defunct = defunct.get_text() if defunct else ""

    url = xml_data.find(["websiteaddresstxt", "website", "websiteaddress"])
    url = url.get_text() if url else ""

    street = subsoup.find(["addressline1txt", "addressline1"])
    street = street.get_text() if street else ""

    city = subsoup.find(["citynm", "city"])
    city = city.get_text() if city() else ""

    state = subsoup.find(["stateabbreviationcd", "state"])
    state = state.get_text() if state else ""

    zip = subsoup.find(["zipcd", "zipcode"])
    zip = zip.get_text() if zip else ""

    country = "us"

    year_of_formation = xml_data.find(["formationyr", "yearformation"])
    year_of_formation = (
        year_of_formation.get_text() if year_of_formation else ""
    )

    return_type = xml_data.find(["returntypecd", "returntype"]).get_text()

    org_type = xml_data.find(['organization501c3', 'organization501c3ind',
                              'organization501c3exemptpfind', 'exemptpf'])
    if org_type is None:
        try:
            tag = xml_data.find(['organization501cind', 'organization501c'])
            if any(x == '4' for x in tag.attrs.values()):
                org_type = '501(c)4' if tag.get_text() else 'unknown'
            else:
                org_type = str([(k + ": " + v) for k, v in tag.attrs.items()])
        except AttributeError:
            org_type = 'unknown'
    else:
        if '501c3' in org_type.name:
            org_type = '501(c)3'
        else:
            org_type = str((org_type.name, str([(k + ": " + v) for k, v in org_type.attrs.items()]),
                        org_type.get_text()))
            # print(org_type)

    result = Essentials(

        ein=ein,
        tax_year=tax_year,
        name=name,
        other_names=other_names,
        defunct=defunct,
        url=url,
        street=street,
        city=city,
        state=state,
        zip=zip,
        country=country,
        year_of_formation=year_of_formation,
        return_type=return_type,
        org_type=org_type,
    )

    return result


def financials(xml_data):
    subsoup = xml_data.find(['irs990', 'irs990pf', 'irs990ez', 'returndata'])

    employees_number = subsoup.find(['totalemployeecnt', 'totalnbremployees'])
    employees_number = employees_number.get_text() if employees_number else ''

    volunteers_number = subsoup.find(['totalvolunteerscnt', 'totalnbrvolunteers'])
    volunteers_number = volunteers_number.get_text() if volunteers_number else ''

    total_revenue = subsoup.find(['cytotalrevenueamt', 'totalrevenuecurrentyear',
                                  'totalrevenueandexpenses', 'totalrevandexpnssamt', 'totalrevenueamt',
                                  'totalrevenue'])
    total_revenue = total_revenue.get_text() if total_revenue else ''

    total_expenses = subsoup.find(['cytotalexpensesamt', 'totalexpensescurrentyear',
                                   'totalexpensesrevandexpnss', 'totalexpensesrevandexpnssamt', 'totalexpensesamt',
                                   'totalexpenses'])
    total_expenses = total_expenses.get_text() if total_expenses else ''

    try:
        total_assets = subsoup.find(['form990totalassetsgrp', 'totalassets']).find(['eoyamt', 'eoy']).get_text()
    except AttributeError:
        total_assets = subsoup.find(['totalassetseoyamt', 'totalassetseoy',
                                     'totalassetseoy'])
        total_assets = total_assets.get_text() if total_assets else ''

    net_assets = subsoup.find(['netassetsorfundbalanceseoyamt', 'netassetsorfundbalanceseoy',
                               'totalnetassetseoy', 'totnetastorfundbalanceseoyamt', 'netassetsorfundbalanceseoyamt'])
    net_assets = net_assets.get_text() if net_assets else ''

    # 14.b on 990 (more than $10,000 revenues/expenses or more than $100k investments

    foreign_fundraising = subsoup.find(['foreignactivitiesind', 'foreignactivities'])
    foreign_fundraising = foreign_fundraising.get_text() if foreign_fundraising else ''

    foreign_grants_to_orgs = subsoup.find(['morethan5000ktoorgind', 'morethan5000ktoorganizations'])
    foreign_grants_to_orgs = foreign_grants_to_orgs.get_text() if foreign_grants_to_orgs else ''

    foreign_grants_to_individuals = subsoup.find(['morethan5000ktoindividualsind',
                                                  'morethan5000ktoindividuals'])
    foreign_grants_to_individuals = foreign_grants_to_individuals.get_text() if foreign_grants_to_individuals else ''

    operate_local_branches = subsoup.find(['localchaptersind', 'localchapters'])
    operate_local_branches = operate_local_branches.get_text() if operate_local_branches else ''

    foreign_grants_group = subsoup.find(['foreigngrantsgrp', 'foreigngrants'])
    if foreign_grants_group:
        foreign_grants_amount = foreign_grants_group.find(['totalamt', 'total'])
        foreign_grants_amount = foreign_grants_amount.get_text() if foreign_grants_amount else ''
    else:
        foreign_grants_amount = ''

    # part vii-a
    foreign_bank_account = subsoup.find(['foreignaccountsquestionind', 'foreignbank',
                                         'foreignfinancialaccountind', 'foreignfinancialaccount'])
    foreign_bank_account = foreign_bank_account.get_text() if foreign_bank_account else ''

    # part ix line 18
    payments_to_govt_officials_group = xml_data.find(
        ['pymttravelentrtnmntpubofclgrp', 'travelentrtnmntpublicofficials'])
    if payments_to_govt_officials_group:
        payments_to_govt_officials = payments_to_govt_officials_group.find('totalamt')
        payments_to_govt_officials = payments_to_govt_officials.get_text() if payments_to_govt_officials else ''
    else:
        payments_to_govt_officials = ''

    government_grants = xml_data.find(['governmentgrantsamt', 'governmentgrants'])
    government_grants = government_grants.get_text() if government_grants else ''

    # schedule c part ii-a
    try:
        total_lobbying_amount = xml_data.find(
            ['totallobbyingexpendituresiib', 'totallobbyingexpendituresamt']).get_text()
    except AttributeError:
        total_lobbying_amount_group = xml_data.find(['totallobbyingexpendgrp', 'totallobbyingexpenditures'])
        if total_lobbying_amount_group:
            total_lobbying_amount = total_lobbying_amount_group.find(['filingorganizationstotalamt',
                                                                      'filingorganizationstotals'])
            total_lobbying_amount = total_lobbying_amount.get_text() if total_lobbying_amount else ''
        else:
            total_lobbying_amount = ''

    try:
        total_legal_spending = xml_data.find(['legalfeesrevandexpns', 'legalfeesrevandexpnssamt']).get_text()
    except AttributeError:
        total_legal_spending_group = xml_data.find(['feesforserviceslegal', 'feesforserviceslegalgrp'])
        if total_legal_spending_group:
            total_legal_spending = total_legal_spending_group.find(['total', 'totalamt'])
            total_legal_spending = total_legal_spending.get_text() if total_legal_spending else ''
        else:
            total_legal_spending = ''

    data = Financials(
        employees_number=employees_number,
        volunteers_number=volunteers_number,
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        total_assets=total_assets,
        net_assets=net_assets,
        foreign_fundraising=foreign_fundraising,
        foreign_grants_to_orgs=foreign_grants_to_orgs,
        foreign_grants_to_individuals=foreign_grants_to_individuals,
        operate_local_branches=operate_local_branches,
        foreign_grants_amount=foreign_grants_amount,
        foreign_bank_account=foreign_bank_account,
        payments_to_govt_officials=payments_to_govt_officials,
        government_grants=government_grants,
        total_lobbying_amount=total_lobbying_amount,
        total_legal_spending=total_legal_spending
    )

    return data


def preparer(xml_data):
    preparer_firm_grp = xml_data.find(['preparerfirm', 'preparerfirmgrp'])
    if preparer_firm_grp:
        preparer_firm = preparer_firm_grp.find(['businessnameline1', 'businessnameline1txt'])
        preparer_firm = preparer_firm.get_text() if preparer_firm else None

        preparer_ein = preparer_firm_grp.find(['preparerfirmein', 'ein'])
        preparer_ein = preparer_ein.get_text() if preparer_ein else None

    else:
        preparer_firm, preparer_ein = None, None

    preparer_address = xml_data.find(['preparerfirmusaddress', 'preparerusaddress'])
    if preparer_address:
        preparer_address_street = preparer_address.find(['addressline1', 'addressline1txt'])
        preparer_address_street = preparer_address_street.get_text() if preparer_address_street else None

        preparer_address_city = preparer_address.find(['city', 'citynm'])
        preparer_address_city = preparer_address_city.get_text() if preparer_address_city else None

        preparer_address_state = preparer_address.find(['state', 'stateabbreviationcd'])
        preparer_address_state = preparer_address_state.get_text() if preparer_address_state else None

        preparer_address_zip = preparer_address.find(['zipcode', 'zipcd'])
        preparer_address_zip = preparer_address_zip.get_text() if preparer_address_zip else None

    else:
        preparer_address_street, preparer_address_city, preparer_address_state, preparer_address_zip = [None] * 4

    preparer_person = xml_data.find(['preparer', 'preparerpersongrp'])

    if preparer_person:
        preparer_name = preparer_person.find(['name', 'preparerpersonnm'])
        preparer_name = preparer_name.get_text() if preparer_name else None

        preparer_ptin = xml_data.find(['ptin'])
        preparer_ptin = preparer_ptin.get_text() if preparer_ptin else None

    else:
        preparer_name, preparer_phone, preparer_ptin = [None] * 3

    result = Preparer(
        preparer_firm=preparer_firm,
        preparer_ein=preparer_ein,
        preparer_address_street=preparer_address_street,
        preparer_address_city=preparer_address_city,
        preparer_address_state=preparer_address_state,
        preparer_address_zip=preparer_address_zip,
        preparer_name=preparer_name,
        preparer_ptin=preparer_ptin,
    )

    return result


def grants(xml_data):

    address = xml_data.find(['recipientusaddress', 'recipientforeignaddress', 'usaddress', 'addressus', 'foreign address'])
    if address:
        fixed_address = address.get_text()
        fixed_address = fixed_address.replace('\n', ', ')
        grantee_address = fixed_address[2:-2]  # to remove spaces and errant commas
    else:
        grantee_address = ''

    grantee_ein = xml_data.find(['recipientein', 'einofrecipient'])
    grantee_ein = grantee_ein.get_text() if grantee_ein else ''

    grantee_org_type = xml_data.find(['ircsectiondesc', 'ircsection',
                                   'recipientfoundationstatustxt', 'recipientfoundationstatus'])
    grantee_org_type = grantee_org_type.get_text() if grantee_org_type else ''

    cash_purpose = xml_data.find(['grantorcontributionpurposetxt', 'purposeofgrantorcontribution',
                               'purposeofgranttxt', 'purposeofgrant'])
    cash_purpose = cash_purpose.get_text() if cash_purpose else ''

    non_cash_purpose = xml_data.find(['noncashassistancedesc', 'descriptionofnoncashassistance'])
    non_cash_purpose = non_cash_purpose.get_text() if non_cash_purpose else ''

    cash_amount = xml_data.find(['amt', 'amount', 'cashgrantamt', 'amountofcashgrant'])
    cash_amount = cash_amount.get_text() if cash_amount else ''

    non_cash_amount = xml_data.find(['noncashassistanceamt', 'amountofnoncashassistance'])
    non_cash_amount = non_cash_amount.get_text() if non_cash_amount else ''

    name = xml_data.find(
        ['recipientbusinessname', 'recipientpersonname', 'recipientpersonnm', 'recipientnamebusiness'])
    if name:
        fixed_name = name.get_text()
        grantee_name = fixed_name.replace('\n', '')
    else:
        grantee_name = 'test'

    result = Grants(
        grantee_name=grantee_name,
        grantee_address=grantee_address,
        grantee_ein=grantee_ein,
        grantee_org_type=grantee_org_type,
        cash_amount=cash_amount,
        non_cash_amount=non_cash_amount,
        cash_purpose=cash_purpose,
        non_cash_purpose=non_cash_purpose
    )

    # print(result)

    return result
