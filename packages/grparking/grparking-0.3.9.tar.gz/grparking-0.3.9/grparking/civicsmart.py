import requests
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime
from grparking import socratagr

### CivicSmart Grand Rapids Meter Payments Request API by Hour:
### 'http://meterpayment.duncan-usa.com/payment/customer/4199/transactions/20210308/hour/11'
### CivicSmart Grand Rapids Meter Payments Request API by Date and Hour range:
### 'http://meterpayment.duncan-usa.com/payment/customer/4199/transactions/20210308/from/0/to/12' (0 to 12 hours)
### 'http://meterpayment.duncan-usa.com/payment/customer/4199/transactions/20210308/from/0/to/0' (Whole day)

def get_sessions(start_date, end_date):
    ### DATA PULL
    url_lead = 'http://meterpayment.duncan-usa.com/payment/customer/4199/transactions/'
    url_end = '/from/0/to/0'
    date_list = pd.date_range(start_date, end_date, freq='d').strftime('%Y%m%d')
    civicsmart_data = pd.DataFrame()

    for date in date_list:
        concat_url = url_lead + date + url_end
        meters = requests.get(concat_url)

        meters_data = ET.fromstring(meters.content)

        # customer_id = meters_data[0].text
        # transmission_dt = meters_data[1].text

        transaction_seq_id = []
        post_id            = []
        session_id         = []
        amount             = []
        payment_type       = []
        start_time         = []
        end_time           = []

        for i in meters_data[2:]:
            transaction_seq_id.append(i[0].text)
            post_id.append(i[1].text)
            session_id.append(i[2][0].text)
            amount.append(i[2][1].text)
            payment_type.append(i[2][2].text)
            start_time.append(i[3].text)
            end_time.append(i[4].text)

        payments_dict = {'paystation_or_parker_id': transaction_seq_id,
                         'post_id': post_id,
                         'session_id': session_id,
                         'fee_in_cents': amount,
                         'payment_type': payment_type,
                         'session_start': start_time,
                         'session_end': end_time}
        paymentsdf = pd.DataFrame(payments_dict)
        civicsmart_data = pd.concat([civicsmart_data, paymentsdf], sort=True)

    ### TRANSFORMATIONS

    # SESSION_START, SESSION_END FORMAT
    civicsmart_data['session_start'] = pd.to_datetime(civicsmart_data['session_start'], format = '%Y-%m-%dT%H:%M:%SZ')
    civicsmart_data['session_end'] = pd.to_datetime(civicsmart_data['session_end'], format = '%Y-%m-%dT%H:%M:%SZ')

    # SESSION START HOUR
    civicsmart_data['session_start_hour'] = civicsmart_data['session_start'].dt.strftime('%Y-%m-%dT%H:00:00')

    # DURATION IN MINUTES
    civicsmart_data['duration_in_minutes'] = (civicsmart_data['session_end'] - civicsmart_data[
        'session_start']).dt.seconds / 60

    # COMPARISON_DATE FUNCTION
    civicsmart_data['comparison_date'] = socratagr.comparison_date(civicsmart_data, 'session_start')

    # YEAR
    civicsmart_data['year'] = pd.DatetimeIndex(civicsmart_data['session_start']).year

    # CREATE NEW COLUMNS
    civicsmart_data['data_source'] = 'CivicSmart'
    civicsmart_data['rate_name'] = 'CivicSmart Meters'
    civicsmart_data['zone_type'] = 'Space Based'
    civicsmart_data['zone_number'] = 'CivicSmart'
    civicsmart_data['space_number'] = None
    civicsmart_data['space_coordinates'] = None
    civicsmart_data['space_point_coordinates'] = None

    # REORDER COLUMNS
    column_order = ['session_id',
                    'year',
                    'comparison_date',
                    'session_start_hour',
                    'session_start',
                    'session_end',
                    'duration_in_minutes',
                    'fee_in_cents',
                    'payment_type',
                    'rate_name',
                    'zone_type',
                    'zone_number',
                    'space_number',
                    'data_source',
                    'space_coordinates',
                    'space_point_coordinates',
                    'paystation_or_parker_id']
    civicsmart_data = civicsmart_data.reindex(columns=column_order)

    # FORMAT DATES FOR SOCRATA
    civicsmart_data['session_start'] = civicsmart_data['session_start'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    civicsmart_data['session_end'] = civicsmart_data['session_end'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    return civicsmart_data

def update_sessions():
    # GET THE DATE RIGHT NOW
    now_date = datetime.now()
    now_year = now_date.strftime('%Y')
    now_month = now_date.strftime('%m')
    now_day = now_date.strftime('%d')
    now_hour = now_date.strftime('%H')

    civicsmart_data = pd.DataFrame()

    ### PULL FROM CIVICSMART API ENDPOINT
    url_lead = 'http://meterpayment.duncan-usa.com/payment/customer/4199/transactions/'

    #CONCATENATE CUSTOM URL FROM DATE RIGHT NOW
    concat_url = url_lead + now_year + now_month + now_day + '/hour/' + now_hour

    meters = requests.get(concat_url)
    meters_data = ET.fromstring(meters.content)

    # customer_id = meters_data[0].text
    # transmission_dt = meters_data[1].text

    transaction_seq_id = []
    post_id = []
    session_id = []
    amount = []
    payment_type = []
    start_time = []
    end_time = []

    for i in meters_data[2:]:
        transaction_seq_id.append(i[0].text)
        post_id.append(i[1].text)
        session_id.append(i[2][0].text)
        amount.append(i[2][1].text)
        payment_type.append(i[2][2].text)
        start_time.append(i[3].text)
        end_time.append(i[4].text)

    payments_dict = {'transaction_seq_id': transaction_seq_id,
                     'post_id': post_id,
                     'session_id': session_id,
                     'fee_in_cents': amount,
                     'payment_type': payment_type,
                     'session_start': start_time,
                     'session_end': end_time}
    paymentsdf = pd.DataFrame(payments_dict)
    civicsmart_data = pd.concat([civicsmart_data, paymentsdf], sort=True)

    ### TRANSFORMATIONS

    # SESSION_START, SESSION_END FORMAT
    civicsmart_data['session_start'] = pd.to_datetime(civicsmart_data['session_start'], format='%Y-%m-%dT%H:%M:%SZ')
    civicsmart_data['session_end'] = pd.to_datetime(civicsmart_data['session_end'], format='%Y-%m-%dT%H:%M:%SZ')

    # CONVERT DATE COLUMNS TO EASTERN TIME
    civicsmart_data['session_start'] = civicsmart_data['session_start'].dt.tz_localize('Etc/GMT+4').dt.tz_convert('EST')
    civicsmart_data['session_end'] = civicsmart_data['session_end'].dt.tz_localize('Etc/GMT+4').dt.tz_convert('EST')

    # SESSION START HOUR
    civicsmart_data['session_start_hour'] = civicsmart_data['session_start'].dt.strftime('%Y-%m-%dT%H:00:00')

    # DURATION IN MINUTES
    civicsmart_data['duration_in_minutes'] = (civicsmart_data['session_end'] - civicsmart_data[
        'session_start']).dt.seconds / 60

    # COMPARISON_DATE FUNCTION
    civicsmart_data['comparison_date'] = socratagr.comparison_date(civicsmart_data, 'session_start')

    # YEAR
    civicsmart_data['year'] = pd.DatetimeIndex(civicsmart_data['session_start']).year

    # CREATE NEW COLUMNS
    civicsmart_data['data_source'] = 'CivicSmart'
    civicsmart_data['rate_name'] = 'CivicSmart Meters'
    civicsmart_data['zone_type'] = 'Space Based'
    civicsmart_data['zone_number'] = 'CivicSmart'
    civicsmart_data['space_number'] = None
    civicsmart_data['space_coordinates'] = None
    civicsmart_data['space_point_coordinates'] = None
    civicsmart_data['paystation_or_parker_id'] = None

    # REORDER COLUMNS
    column_order = ['session_id',
                    'year',
                    'comparison_date',
                    'session_start_hour',
                    'session_start',
                    'session_end',
                    'duration_in_minutes',
                    'fee_in_cents',
                    'payment_type',
                    'rate_name',
                    'zone_type',
                    'zone_number',
                    'space_number',
                    'data_source',
                    'space_coordinates',
                    'space_point_coordinates',
                    'paystation_or_parker_id']
    civicsmart_data = civicsmart_data.reindex(columns=column_order)

    # FORMAT DATES FOR SOCRATA
    civicsmart_data['session_start'] = civicsmart_data['session_start'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    civicsmart_data['session_end'] = civicsmart_data['session_end'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    return civicsmart_data