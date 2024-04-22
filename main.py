from settings import driver
from utils import days_to_months
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import pandas as pd
import os
# END IMPORTS

# EXCEL FORMAT
df = pd.DataFrame(columns=['Name', 'Description', 'Protocol', 'Blockchain', 'Deal Structure',
                           'Status', 'KYC Status', 'Credit Analyst', 'Currency',
                           'Super Senior Tranche APY', 'Senior Tranche APY', 'Mezzanine Tranche APY',
                           'Junior Tranche APY', 'Fixed APY', 'Variable APY',
                           'Native Token', 'Variable Native Token Bonus APY',
                           'Principal', 'Interest', 'Total', 'Loan Term (Months)',
                           'Liquidity', 'Term Start Date', 'Loan Maturity Date',
                           'Repayment Structure', 'Payment Frequency', 'Total Number of Payments',
                           'Leverage Ratio', 'LTV', 'Super Senior Pool Capital Allocation',
                           'Senior Pool Capital Allocation', 'Mezzanine Pool Capital Allocation',
                           'Junior Pool Capital Allocation', 'Direct Funding Capital Allocation',
                           'On-chain Capital Priority', 'Off-chain Capital Priority',
                           'Collateralization', 'Resource to Borrower', 'Borrower Name',
                           'About Borrower', 'Pool Funded', 'Block Explorer', 'Source Link'])

# GET LINK
driver.get('https://app.credix.finance/')

# CLICK ON ALL OPPORTUNITIES TAB
all_opportunities_tab = driver.find_element(
    By.XPATH, '//*[@id="rc-tabs-0-tab-allOpportunities"]')
all_opportunities_tab.click()

# WAIT FOR DATA TO BE LOADED
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
    (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/main/div[2]/div/div/div/div[2]/div/div[2]/div[2]')))
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
    (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/main/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div/div/table/thead/tr/th[1]')))
body = driver.find_element(By.TAG_NAME, 'body')
body.send_keys(Keys.END)
time.sleep(10)

# START PROCESSING EACH RECORD OF TABLE
pagination = 2
while True:
    for i in range(1, 13):
        while True:
            try:
                show_btn = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[2]/main/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[6]/div/a')
                break
            except NoSuchElementException:
                continue
        # Get the href attribute of the link
        link_href = show_btn.get_attribute("href")
        driver.execute_script(f"window.open('{link_href}', '_blank');")
        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[1])
        #####################################################################
        while True:
            try:
                name = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[1]/div/h1').text
                description = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div[1]').text
                principal = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/div/div/div[2]/div').text.split(' ')[0].replace(',', '')
                interest = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div').text.split(' ')[0].replace(',', '')
                if principal == '0' or interest == '0':
                    continue

                try:
                    total = int(principal) + int(interest)
                    interest = '$'+str(interest)
                except ValueError:
                    total = principal
                long_term = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div').text.split(' ')[0]
                long_term = days_to_months(int(long_term))
                term_start_date = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
                # Convert the string to a datetime object
                term_start_date = datetime.strptime(
                    term_start_date, '%b %d, %Y, %I:%M %p')

                # Format the datetime object to include only the month, day, and year
                term_start_date = term_start_date.strftime('%b %d, %Y')
                try:
                    ul_list = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/ul')
                    list_elements = ul_list.find_elements(By.TAG_NAME, 'li')
                    list_elements[-2].click()
                    time.sleep(2)
                    table_xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/table"
                    last_row = driver.find_element(
                        By.XPATH, f'{table_xpath}//tbody//tr[last()]')
                    loan_maturity_date = last_row.find_element(
                        By.XPATH, './td[1]/span').text
                    # Convert the string to a datetime object
                    loan_maturity_date = datetime.strptime(
                        loan_maturity_date, '%b %d, %Y, %I:%M %p')

                    # Format the datetime object to include only the month, day, and year
                    loan_maturity_date = loan_maturity_date.strftime(
                        '%b %d, %Y')
                except NoSuchElementException:
                    table_xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/table"
                    last_row = driver.find_element(
                        By.XPATH, f'{table_xpath}//tbody//tr[last()]')
                    loan_maturity_date = last_row.find_element(
                        By.XPATH, './td[1]/span').text
                    # Convert the string to a datetime object
                    loan_maturity_date = datetime.strptime(
                        loan_maturity_date, '%b %d, %Y, %I:%M %p')

                    # Format the datetime object to include only the month, day, and year
                    loan_maturity_date = loan_maturity_date.strftime(
                        '%b %d, %Y')

                total_number_of_payments = long_term
                borrower_name = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/a[1]').text
                about_borrower = description
                source_link = driver.current_url

                # Tranche structure
                tranche_format = {
                    'Super Senior': ['Super Senior Tranche APY', 'Super Senior Pool Capital Allocation', '—', '—'],
                    'Senior': ['Senior Tranche APY', 'Senior Pool Capital Allocation', '—', '—'],
                    'Junior': ['Junior Tranche APY', 'Junior Pool Capital Allocation', '—', '—'],
                    'Mezzanine': ['Mezzanine Tranche APY', 'Mezzanine Pool Capital Allocation', '—', '—']
                }
                fixed_apr = '—'
                try:
                    tranches = ['Super Senior',
                                'Senior', 'Junior', 'Mezzanine']
                    canvas = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[1]/div/div/canvas')
                    tranche1 = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[4]/div[1]/span').text
                    tranche1_apr = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[4]/div[2]/div').text
                    tranche1_capital = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[4]/span/span[2]').text
                    tranche2 = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[6]/div[1]/span').text
                    tranche2_apr = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[6]/div[2]/div').text
                    tranche2_capital = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[6]/span/span[2]').text
                    for tranche in tranches:
                        if tranche1 == tranche:
                            tranche_format[tranche][2] = tranche1_apr
                            tranche_format[tranche][3] = tranche1_capital
                        if tranche2 == tranche:
                            tranche_format[tranche][2] = tranche2_apr
                            tranche_format[tranche][3] = tranche2_capital
                except NoSuchElementException:
                    fixed_apr = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/div/div[5]/div').text

                # EXPLORER PAGE
                explorer_page_element = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/a')
                explorer_page_link = explorer_page_element.get_attribute(
                    "href")
                driver.execute_script(
                    f"window.open('{explorer_page_link}', '_blank');")
                driver.switch_to.window(driver.window_handles[2])
                time.sleep(1)
                while True:
                    try:
                        wait_for = driver.find_element(
                            By.XPATH, '/html/body/div[3]/div[3]/div[8]/div[1]/h3')
                        break
                    except NoSuchElementException:
                        continue
                try:
                    block_explorer_link = driver.find_element(
                        By.XPATH, '/html/body/div[3]/div[3]/div[7]/div[2]/table/tbody/tr[25]/td/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[1]/span[2]/a').get_attribute('href')
                except NoSuchElementException:
                    block_explorer_link = driver.find_element(
                        By.XPATH, '/html/body/div[3]/div[3]/div[7]/div[2]/table/tbody/tr[23]/td/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[1]/span[2]/a').get_attribute('href')
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                print('NAME:', name)
                print('DESCRIPTION:', description)
                print('PRINCIPAL:', principal)
                print('INTEREST:', interest)
                print('TOTAL:', total)
                print('LONG TERM:', long_term)
                print('TERM START DATE:', term_start_date)
                print('LOAD MATURITY DATE:', loan_maturity_date)
                print('TOTAL NUMBER OF PAYMENTS:', total_number_of_payments)
                print('BORROWER NAME:', borrower_name)
                print('ABOUT BORROWER:', about_borrower)
                print('BLOCK EXPLORER:', block_explorer_link)
                print('SOURCE LINK:', source_link)
                # WRITING DATA INTO EXCEL
                df = pd.concat([df, pd.DataFrame({
                    'Name': [name],
                    'Description': [description],
                    'Protocol': ['Credix'],
                    'Blockchain': ['Solana'],
                    'Deal Structure': ['Unitranche'],
                    'Status': ['Active'],
                    'KYC Status': ['Non-US, US Accredited'],
                    'Credit Analyst': ['—'],
                    'Currency': ['USDC-SPL'],
                    'Super Senior Tranche APY': tranche_format['Super Senior'][2],
                    'Senior Tranche APY': tranche_format['Senior'][2],
                    'Mezzanine Tranche APY': tranche_format['Mezzanine'][2],
                    'Junior Tranche APY': tranche_format['Junior'][2],
                    'Fixed APY': fixed_apr,
                    'Variable APY': ['—'],
                    'Native Token': ['—'],
                    'Variable Native Token Bonus APY': ['—'],
                    'Principal': [f'${principal}'],
                    'Interest': [f'{interest}'],
                    'Total': [f'${total}'],
                    'Loan Term (Months)': [long_term],
                    'Liquidity': ['End of loan term'],
                    'Term Start Date': [term_start_date],
                    'Loan Maturity Date': [loan_maturity_date],
                    'Repayment Structure': ['Bullet'],
                    'Payment Frequency': ['Monthly'],
                    'Total Number of Payments': [total_number_of_payments],
                    'Leverage Ratio': ['—'],
                    'LTV': ['—'],
                    'Super Senior Pool Capital Allocation': tranche_format['Super Senior'][3],
                    'Senior Pool Capital Allocation': tranche_format['Senior'][3],
                    'Mezzanine Pool Capital Allocation': tranche_format['Mezzanine'][3],
                    'Junior Pool Capital Allocation': tranche_format['Junior'][3],
                    'Direct Funding Capital Allocation': ['—'],
                    'On-chain Capital Priority': ['—'],
                    'Off-chain Capital Priority': ['—'],
                    'Collateralization': ['—'],
                    'Resource to Borrower': ['—'],
                    'Borrower Name': [borrower_name],
                    'About Borrower': [about_borrower],
                    'Pool Funded': ['Yes'],
                    'Block Explorer': [block_explorer_link],
                    'Source Link': [source_link]
                })], ignore_index=True)
                df.to_excel('Private Credit Deals.xlsx', index=False)
                print('######################################')
                break
            except NoSuchElementException:
                continue
        #####################################################################
        # Close the new tab
        driver.close()
        # Switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])

    # NEXT BUTTON
    try:
        ul = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/main/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/ul')
        li = ul.find_elements(By.TAG_NAME, 'li')
        try:
            li[pagination].click()
            pagination += 1
            time.sleep(2)
        except ElementClickInterceptedException:
            break
    except NoSuchElementException:
        break

driver.quit()
