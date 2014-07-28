import logging
import re
import smtplib
import sys
from alerter import models
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.management.base import BaseCommand
from cookielib import CookieJar
from email.mime.text import MIMEText
from requests import Session
from urllib import urlencode


logger = logging.getLogger(__name__)

def send_email(transactions, mpesa_account):
    recipient_map = {}
    for receipt, info in transactions.items():
        account, details = info[0:2]
        recipients = [r.email_recipient for r in models.EmailRecipient.objects.all() if r.account_number.lower() in account.lower()]
        for recipient in recipients:
            if recipient not in recipient_map:
                recipient_map[recipient] = [receipt]
            else:
                recipient_map[recipient].append(receipt)
    for recipient, receipts in recipient_map.items():
        msg_body = ''
        for receipt in transactions.keys():
            if receipt in receipts:
                account, date, details, status, amount, _ = transactions[receipt]
                msg_body += 'Date: %s | %s | Status: %s | Amount: %s\n' % (date, details, status, amount)

        msg = MIMEText(msg_body)
        msg['Subject'] = 'New M-Pesa Transactions for %s' % mpesa_account
        msg['From'] = 'robot@example.com'
        msg['To'] = recipient

        s = smtplib.SMTP('localhost')
        s.sendmail('robot@example.com', [recipient], msg.as_string())
        s.close()

def post_to_api(transactions):
    url = 'http://api.linguisticmobile.com/mpesa.cfm'
    session = Session()
    for receipt, info in transactions.items():
        account = info[0]
        if account == '05882':
            logger.info('Sending transaction data to %s for account %s' % (url, account))
            response = session.get(url + '?msisdn=%s&confirmation_code=%s&Account=%s&Amount=%s' % (info[5], receipt, account, info[4]))
            logger.debug(response.headers)
            logger.debug(response.text)

def login(session, url, username, password, org):
    login_params = urlencode({
        '__VIEWSTATE': '',
        'LoginCtrl$UserName': username,
        'LoginCtrl$Password': password,
        'LoginCtrl$txtOrganisationName': org,
        'LoginCtrl$LoginButton': 'Log In',
    })
    r = session.post(url, login_params)
    logger.debug(r.headers)
    for line in r.iter_lines():
        logger.debug(line)
    logger.debug(session.cookies)
    for cookie in session.cookies:
        if cookie.name == '.ASPXAUTH':
            return True
    return False

def get_new_transactions(session, url, account):
    # Go to transaction page to get ID of account type given in config, and also get __VIEWSTATE 
    # parameter (needed by ASP.Net used by M-Pesa, otherwise form submission will fail).
    doc = BeautifulSoup(session.get(url).text)
    account_type = doc.find('option', text=account).get('value')
    viewstate = doc.find('input', id='__VIEWSTATE').get('value')

    # To the same page, submit the form to retrieve the desired transaction history.
    search_params = urlencode({
        '__VIEWSTATE': viewstate,
        'ctl00$Main$ctl00$cbAccountType': account_type,
        'ctl00$Main$ctl00$cbTransactionsShown': '50',
        'ctl00$Main$ctl00$rblTransType': 'All',
        'ctl00$Main$ctl00$btnSearch': 'Search',
    })
    doc = BeautifulSoup(session.post(url, search_params).text)
    logger.debug(doc)

    new_transactions = {}
    table = doc.find('table', id='ctl00_Main_ctl00_AccountStatementGrid2_dgStatement_ctl01')
    account_re = re.compile('Payment received from (?P<msisdn>\d+).* Acc. (?P<account>.+)')
    for row in table.find_all('tr'):
        if 'class' in row.attrs and row['class'][0].startswith('Grid'):
            columns = row.find_all('td')
            receipt, date, details, status, amount, _ = columns
            receipt = str(receipt.a.text)
            match = account_re.match(details.text)
            if not match: continue
            msisdn = match.group('msisdn')
            account = match.group('account')
            date_obj = datetime.strptime(date.text, '%Y-%m-%d %H:%M:%S')
            if not models.History.objects.filter(receipt=receipt):
                new_transactions[receipt] = [account, date_obj, details.text, status.text.strip(), amount.text, msisdn]
    return new_transactions

def main():
    base_url = 'https://ke.m-pesa.com/ke'
    urls = {
        'login': base_url+'/Default.aspx',
        'transactions': base_url+'/Main/home2.aspx?MenuID=1692',
    }

    for account in models.MPesaAccount.objects.all():
        session = Session(cookies=CookieJar(), cert='/opt/env/oxygen8/etc/mpesa.pem', verify='/opt/env/oxygen8/etc/cacert.pem')

        if not login(session, urls['login'], account.username, account.password, account.org):
            logger.error('Failed to log in')
            sys.exit(1)

        new_transactions = get_new_transactions(session, urls['transactions'], account.account_type)
        if new_transactions:
            send_email(new_transactions, account.org)
            post_to_api(new_transactions)
            for k, v in new_transactions.items():
                history_obj = models.History(receipt=k, timestamp=v[1], details=v[2], status=v[3], amount=v[4], msisdn=v[5])
                history_obj.save()


class Command(BaseCommand):
    args = ''
    help = 'Check M-Pesa site and alert on new transactions'

    def handle(self, *args, **options):
        main()


if __name__ == '__main__':
    main()
