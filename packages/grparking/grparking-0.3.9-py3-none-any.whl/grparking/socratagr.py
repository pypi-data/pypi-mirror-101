import requests
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
from socrata.authorization import Authorization
from socrata import Socrata


def comparison_date(dataframe, date_column):
    # Calculate Number of years ago for each data point
    this_year = datetime.now().year

    dataframe['Year'] = this_year - dataframe[date_column].dt.year

    # Determine Number of Unique Years in Dataset
    years_ago = dataframe['Year'].unique()

    # FORMAT HOUR PRECISION DATE COLUMN
    dataframe['Session Start Hour'] = pd.to_datetime(dataframe[date_column].dt.strftime('%Y-%m-%d %H:00:00'))

    # COMPARISON DATE
    dataframe['Comparison Date'] = dataframe['Session Start Hour']

    for number in years_ago:
        if number > 0:
            # Check is Current Year is Leap Year and Set Dates Accordingly
            if datetime.now().year - 1 % 4 == 0:
                dataframe.loc[dataframe['Year'] == number, 'Comparison Date'] = dataframe[
                                                                                  'Session Start Hour'] + timedelta(
                    days=364 - int(number))
            else:
                dataframe.loc[dataframe['Year'] == number, 'Comparison Date'] = dataframe[
                                                                                  'Session Start Hour'] + timedelta(
                    days=365 - int(number))

    return dataframe['Comparison Date']


# RENAME RAMPS FUNCTION
def rename_ramp(fourfour, column, current_name, replacement, update_config, blanks=False, blank_names=None):
    # GET EXISTING DATA
    url = 'https://data.grandrapidsmi.gov/resource/' + \
          fourfour + \
          '.json?$limit=10000000&$where=' + \
          column + "='" + \
          current_name + "'"

    df = requests.get(url, auth=(os.environ['SOCRATA_USERNAME'], os.environ['SOCRATA_PASSWORD']))

    df = pd.DataFrame(df.json())

    # RECODE VARIABLE
    df[column] = replacement

    # ADD COLUMNS WITH BLANK VALUES
    if blanks is True:
        for column in blank_names:
            df[column] = None

    # SOCRATA AUTH
    auth = Authorization(
        'data.grandrapidsmi.gov',
        os.environ['SOCRATA_USERNAME'],
        os.environ['SOCRATA_PASSWORD']
    )
    socrata = Socrata(auth)

    # REPLACE EXISTING DATA WITH RECODED DATA
    (ok, view) = socrata.views.lookup(fourfour)
    (revision, job) = socrata.using_config(
        update_config,
        view
    ).df(df)
    (ok, job) = job.wait_for_finish(progress=lambda job: print('Ramp Replacement Progress: ', job.attributes['status']))


def query_data(fourfour, user, password, query=None, limit=10000000):
    limit = str(limit)

    if query is None:
        url = 'https://data.grandrapidsmi.gov/resource/' + \
              fourfour + '.json?' + '$limit=' + limit

    elif isinstance(query, str):
        url = 'https://data.grandrapidsmi.gov/resource/' + \
              fourfour + '.json?' + '$limit=' + limit + '&$' +\
              query

    elif isinstance(query, list):
        url = 'https://data.grandrapidsmi.gov/resource/' + \
              fourfour + '.json?' + '$limit=' + limit
        for item in query:
            url = url + '&$' + item

    df = requests.get(url, auth=(user, password))

    df = df.json()

    df = pd.DataFrame(df)

    return df


def delete_rows(fourfour, delete_ids):
    # deletes rows in a dataset given an ID and a dataframe
    # dataframe must contain a column aligning with the dataset's ID column (it can contain only this column)
    auth = Authorization(
        'data.grandrapidsmi.gov',
        os.environ['SOCRATA_USERNAME'],
        os.environ['SOCRATA_PASSWORD']
    )
    socrata = Socrata(auth)

    (ok, view) = socrata.views.lookup(fourfour)
    assert ok
    (ok, revision) = view.revisions.create_delete_revision(permission='private')
    assert ok
    (ok, upload) = revision.create_upload('deleted_data')
    assert (ok)
    (ok, source) = upload.df(delete_ids)
    assert (ok)
    output_schema = source.get_latest_input_schema().get_latest_output_schema()
    (ok, job) = revision.apply(output_schema=output_schema)
    assert (ok)
    (ok, job) = job.wait_for_finish(progress=lambda job: print('Job progress:', job.attributes['status']))
