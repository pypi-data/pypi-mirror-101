import pandas as pd
import time
import sys

def df_parser(file) -> tuple:
    """
    Returns df and name depending on file type
    """
    extention = file.split('.')[1]
    name = file.split('.')[0]

    if extention == 'csv':
        return pd.read_csv(file), name
    elif extention == 'xlsx':
        return pd.read_excel(file), name
    elif extention == 'sql':
        return pd.read_sql(file), name
    else:
        return None

def data_lst(df) -> dict:
    """
    Stores input data into a dictionary
    """
    data = {}
    value = ''
    for row in df.index:
        value = ','.join(str(x) for x in df.iloc[row].values)
        if data.get(value):
            data[value]['rows'].append(row)
        else:
            data[value] = {'rows': [row]}
    return data

def val_list_count(lst1, lst2) -> list:
    """
    Computes total match and unmatch lengths and returns counts and data list.
    """
    match_count = 0
    unmatch_count = 0
    match_lst = []
    unmatch_lst = []
    for key in lst1:
        if lst2.get(key):
            match_count += len(lst1[key]['rows'])
            match_lst.append(key.split(','))
        else:
            unmatch_count += len(lst1[key]['rows'])
            unmatch_lst.append(key.split(','))
    return match_lst, unmatch_lst, match_count, unmatch_count
        

def validator(workbook1, workbook2) -> None:
    """
    Auto validator that will return percentage of corrlelation either positive or negative

    :param workbook1 string: path to workbook 1
    :param workbook2 string: path to workbook 2
    :param corr boolean: choose whether you would like to search for positive or negative correlation
    :return: percentages
    """
    start_time = time.time()
    df1, name1 = df_parser(workbook1)
    df2, name2 = df_parser(workbook2)
    val_list_1 = data_lst(df1)
    val_list_2 = data_lst(df2)
    mlst1, ulst1, mcount1, ucount1 = val_list_count(val_list_1, val_list_2)
    mlst2, ulst2, mcount2, ucount2 = val_list_count(val_list_2, val_list_1)   

    pd.DataFrame(mlst1).to_csv(f'reports/Matching_{name1}.csv')
    pd.DataFrame(mlst2).to_csv(f'reports/Matching_{name2}.csv')
    pd.DataFrame(ulst1).to_csv(f'reports/Unmatching_{name1}.csv')
    pd.DataFrame(ulst2).to_csv(f'reports/Unmatching_{name2}.csv')

    output_info = pd.DataFrame((

        (
        df1.shape[0], df1.shape[1], mcount1, ucount1, 
        round(mcount1 / df1.shape[0] * 100, 2), round(ucount1 / df1.shape[0] * 100, 2), ''
        ),


        (
        df2.shape[0], df2.shape[1], mcount2, ucount2,
        round(mcount2 / df2.shape[0] * 100, 2), round(ucount2 / df2.shape[0] * 100, 2), ''
        ),
     
        (
        '', '', '', '', '', '', round(time.time() - start_time, 3)
        ),

        ),
        columns=['RowCount', 'ColumnCount', 'Matching', 'Unmatching', 'Matching%', 'Unmatching%', 'RunTime'], 
        index=[name1, name2, 'Total'])

    output_info.to_excel('reports/00_FullReport.xlsx')

    print('============================================Report================================================')
    print(output_info)
    print('==================================================================================================')
    return None

def field_check(field1, field2) -> None:
    """
    For testing
    """
    test1 = field1
    test2 = field2
    file = open('field_check.txt', 'w+')
    file.writelines(test1)
    file.writelines('\n')
    file.writelines(test2)
    file.close()
    return None

if __name__ == '__main__':
    workbook1 = sys.argv[1]
    workbook2 = sys.argv[2]
    validator(workbook1, workbook2)
