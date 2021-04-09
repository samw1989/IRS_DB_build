import read_xml as read_xml
from db_models import MainReturn, Grants
#
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from mongoengine import connect
import time
import concurrent.futures


def open_xml(filepath):
    with open(filepath) as f:
        content = f.read()
        content = content.encode('utf-8-sig')
        soup = BeautifulSoup(content, 'lxml')
        return soup


def scrape_xml(soup):
    essentials = read_xml.essentials(soup)
    financials = read_xml.financials(soup)
    preparer = read_xml.preparer(soup)

    return essentials, financials, preparer


def build_main(essentials, financials, preparer, filename):
    mainreturn = MainReturn(
        # Essentials
        source='https://s3.amazonaws.com/irs-form-990/' + filename,
        ein=essentials.ein,
        tax_year=essentials.tax_year,
        name=essentials.name,
        other_names=essentials.other_names,
        defunct=essentials.defunct,
        url=essentials.url,
        address_street=essentials.street,
        address_city=essentials.city,
        address_state=essentials.state,
        address_zip=essentials.zip,
        address_country=essentials.country,
        year_of_formation=essentials.year_of_formation,
        return_type=essentials.return_type,
        org_type=essentials.org_type,
        # Financials
        number_employees=financials.employees_number,
        number_volunteers=financials.volunteers_number,
        operate_local_branches=financials.operate_local_branches,
        total_revenue=financials.total_revenue,
        total_expenses=financials.total_expenses,
        total_assets=financials.total_assets,
        net_assets=financials.net_assets,
        foreign_fundraising=financials.foreign_fundraising,
        foreign_grants_to_orgs=financials.foreign_grants_to_orgs,
        foreign_grants_to_individuals=financials.foreign_grants_to_individuals,
        foreign_grants_amount=financials.foreign_grants_amount,
        foreign_bank_account=financials.foreign_bank_account,
        payments_to_govt_officials=financials.payments_to_govt_officials,
        government_grants=financials.government_grants,
        total_lobbying_amount=financials.total_lobbying_amount,
        total_legal_spending=financials.total_legal_spending,
        # Preparer
        preparer_firm=preparer.preparer_firm,
        preparer_ein=preparer.preparer_ein,
        preparer_address_street=preparer.preparer_address_street,
        preparer_address_city=preparer.preparer_address_city,
        preparer_address_state=preparer.preparer_address_state,
        preparer_address_zip=preparer.preparer_address_zip,
        preparer_name=preparer.preparer_name,
        preparer_ptin=preparer.preparer_ptin,
    )

    return mainreturn


def find_grant_items(xml_data):
    grant_items = xml_data.find_all(['grantorcontripaidduringyear', 'grantorcontributionpdduryrgrp', 'recipienttable'])
    return grant_items


def build_grants(grants, mainreturn):
    grant_data = Grants(
        related_org=mainreturn.id,
        grantor_name=mainreturn.name,
        grant_year=mainreturn.tax_year,
        grantee=grants.grantee_name,
        grantee_address=grants.grantee_address,
        grantee_ein=grants.grantee_ein,
        grantee_org_type=grants.grantee_org_type,
        cash_amount=grants.cash_amount,
        non_cash_amount=grants.non_cash_amount,
        cash_purpose=grants.cash_purpose,
        non_cash_purpose=grants.non_cash_purpose,
        source=mainreturn.source,
    )
    return grant_data


def process(file):
    f = Path.cwd() / filepath / file
    xml_contents = open_xml(f)
    essentials, financials, preparer = scrape_xml(xml_contents)
    mainreturn = build_main(essentials, financials, preparer, file)
    mainreturn.save()
    grant_items = find_grant_items(xml_contents)
    if grant_items:
        for g in grant_items:
            data = read_xml.grants(g)
            grant_row = build_grants(data, mainreturn)
            grant_row.save()


if __name__ == '__main__':

    filepath = input('Filepath? ')

    t1 = time.perf_counter()

    connect(db="990s", connect=False)
    print('hello')
    files_list = [file.name for file in Path(filepath).rglob('*.xml')]

    # for file in tqdm(files_list):
    #     process(file)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(process, files_list), total=len(files_list)))

    t2 = time.perf_counter()
    print(f'Time taken: {round((t2-t1), 2)}')