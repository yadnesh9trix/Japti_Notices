import datetime
import pandas as pd
import datetime as dt
from datetime import datetime,timedelta
import numpy as np
import csv
import warnings
warnings.filterwarnings('ignore')



def execute_data(inppath ,tax_data):

    # Read property data
    property_file = "Demand Excluding Illegal 2023-24 27072023.csv"
    property_data = pd.read_csv(inppath + property_file, low_memory=False)
    property_data.dropna(subset=['propertycode', 'propertykey'], how='all', inplace=True)
    property_data['propertycode'] = property_data['propertycode'].astype(float)
    woutduplicates_pid = property_data.drop_duplicates('propertycode')
    # Rename in standard columns 'arrearsdemand', 'currentdemand', and 'totaldemand'
    property_data_list = woutduplicates_pid.rename(columns={'arrearsdemand': 'Arrears',
                                                            'currentdemand': 'Current Bill',
                                                            'totaldemand': 'Total_Amount'})
    property_data_list = pd.DataFrame(property_data_list,columns=['propertykey', 'propertycode', 'propertyname',
                                                                'propertyaddress', 'Arrears', 'Current Bill', 'Total_Amount'])

    # Read bill distributed details
    bill_distributed_file = "Master_Bill_Distributed_Payments.csv"
    bill_distributed_details = pd.read_csv(inppath + bill_distributed_file, encoding='utf-8')
    bill_distributed_details['propertycode'] = bill_distributed_details['propertycode'].astype(float)
    bill_distributed_details = pd.DataFrame(bill_distributed_details,
                                            columns=['propertycode', 'propertyLat', 'propertyLong', 'mobileUpdated'])

    # Read japtinotice data
    # Read japtinotice data
    japtinotice_file = "Japti_data03102023.csv"
    japtinotice_data = pd.read_csv(tax_data + japtinotice_file, encoding='utf-8')
    japtinotice_data['propertycode'] = japtinotice_data['propertycode'].astype(float)
    # Rename in standard columns 'arrearsdemand', 'currentdemand', and 'totaldemand'
    japtinotice_data = japtinotice_data.rename(columns={'zonename': 'Zone',
                                                            'gatname': 'Gat'})
    japtinotice_data = pd.DataFrame(japtinotice_data,
                                    columns=['Zone','Gat','propertycode','finalusetype','mobileno', 'status'])

    # ['निवासी', 'बिगरनिवासी', 'मिश्र', 'मोकळ्या जमिन', 'इतर', 'औद्योगिक', 'Not-Available', nan]

    msterdatapath_ = "D:\Master Data\Mapping/"
    zonetype = pd.read_csv(msterdatapath_ + "zone.csv")
    zonemap = dict(zip(zonetype['zonename'], zonetype['eng_zonename']))
    return property_data_list, bill_distributed_details, japtinotice_data,zonemap


def data_clean(japtinotice_data):
    # Define a function 'convert_mobilefmt' to extract and format mobile numbers in a DataFrame column
    def convert_mobilefmt(df, col_name):
        try:
            df[col_name] = df[col_name].str.extract(r'(\d{10})')
        except:
            pass
        df[col_name] = df[col_name].fillna(0000000000).astype("int64")
        df[col_name] = np.where((df[col_name] > 5999999999) & (df[col_name] <= 9999999999),
                                df[col_name], np.nan)
        return df

    # --------------------------------------------------------------------------------------------------
    # Apply 'convert_mobilefmt' function to format 'own_mobile' column in 'property_data_lyreceipts'
    cleaned_property_data = convert_mobilefmt(japtinotice_data, 'mobileno')

    # Merge 'cleaned_property_data' with 'bill_distributed_details' DataFrame on 'propertycode'
    # Fill missing values in 'own_mobile' with values from 'mobileUpdated' column
    cleaned_propertydata_bills = convert_mobilefmt(cleaned_property_data, 'mobileUpdated')

    cleaned_propertydata_bills['own_mobile'] = \
        cleaned_propertydata_bills['mobileno'].fillna(cleaned_propertydata_bills['mobileUpdated'])

    return cleaned_propertydata_bills