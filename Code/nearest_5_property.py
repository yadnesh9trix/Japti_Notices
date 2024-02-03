import os
import time
# import module
import pandas as pd
import xlsxwriter
import openpyxl
from openpyxl import Workbook
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings('ignore')
import calaculate_distance as cd
#-----------------------------------------------------------------------------------------------------------------------

path = "D:\Master Data\Output/19_Oct_2023/Master_Data(19102023).csv"
df = pd.read_csv(path,encoding="utf-8-sig")

# Get current location's latitude and longitude
current_lat, current_lon = cd.get_current_location()
df = df.sort_values('Total_Amount',ascending=False)

# Calculate distance for each row and add as a new column 'Distance'
df['Distance'] = df.apply(lambda row: cd.calculate_distance(current_lat, current_lon, row['propertyLat'], row['propertyLong']), axis=1)

# Sort the dataframe based on the 'Distance' column
df_sorted = df.sort_values(by='Distance')
df_sorted = df_sorted[df_sorted['Distance'].notnull()]

# Select only required columns and avoid sorting if not necessary
# identical_col_df = pd.DataFrame(df_sorted, columns=['propertykey', 'propertycode', 'Zone', 'Gat', 'own_mobile',
#                                                     'Arrears', 'Current Bill', 'Total_Amount',
#                                                     'propertyLat', 'propertyLong', 'visitDate',
#                                                     'last payment date', 'Quarter', 'propertyname',
#                                                     'propertyaddress'])

# identical_col_df = pd.DataFrame(df_sorted, columns=['propertycode', 'Zone', 'Gat', 'own_mobile',
#                                                     'Distance'])
# missing_mobile = identical_col_df[identical_col_df['own_mobile'].isnull()]
# presnt_mobile = identical_col_df[identical_col_df['own_mobile'].notnull()]


# Function to find the closest neighbors
def find_neighbours(row, present_mobile_df):
    df_closest = present_mobile_df.iloc[(present_mobile_df['Distance'] - row['Distance']).abs().argsort()[:5]]
    df_closest1 = pd.concat([pd.DataFrame([row]),df_closest], ignore_index=True)
    df_closest1['MissingMobile_Name'] = row['propertyname']
    return df_closest1

identical_col_df = pd.DataFrame(df_sorted, columns=['propertycode', 'Zone', 'Gat',
                                                    'own_mobile', 'Distance',
                                                    'propertyname','paidTY_Flag',
                                                    'propertyaddress',
                                                    'propertyLat', 'propertyLong',
                                                    'Total_Amount','Quarter'])
identical_col_df = identical_col_df.sort_values('paidTY_Flag',ascending=True)
missing_mobile = identical_col_df[identical_col_df['own_mobile'].isnull()]
present_mobile = identical_col_df[identical_col_df['own_mobile'].notnull()]

result_df = missing_mobile.apply(lambda row: find_neighbours(row, present_mobile), axis=1)

result_df = pd.concat(result_df.tolist(), ignore_index=True)
result_df = pd.DataFrame(result_df, columns=['MissingMobile_Name','propertycode', 'Zone', 'Gat',
                                                    'own_mobile',
                                                    'propertyname',
                                                    'propertyaddress',
                                                    'propertyLat', 'propertyLong',
                                                    'Total_Amount','paidTY_Flag','Quarter'])

result_df.to_csv("final_df.csv",index=False,encoding='utf-8-sig')

df111 = pd.read_csv("final_df.csv")



# # Load the Excel file
# df = pd.read_excel('final_df.xlsx')
#
# # Define the number of rows after which to merge
# merge_interval = 5
#
# # Create a list to hold the merged cells
# merged_cells = []
#
# # Iterate through the rows and add to the list
# for i in range(0, len(df), merge_interval):
#     merged_cells.append(df.iloc[i:i + merge_interval, :].apply(lambda x: ' '.join(x), axis=0))
#
# # Concatenate the merged cells and create a new DataFrame
# result_df = pd.concat(merged_cells, axis=1).T
#
# # Save the result to a new Excel file
# result_df.to_excel('output.xlsx', index=False)
# print(True)


