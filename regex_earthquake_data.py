#regEx sample: EDA derived from terminology used in text field for earthquake data
#data set courtesy of https://www.kaggle.com/datasets/rajkumarpandey02/lists-of-earthquakes-deadliest-and-largest

import pandas as pd
import numpy as np
import regex as re
url = 'https://raw.githubusercontent.com/A-Bin1/Data-Science-Misc/main/deadliest_earthquakes_by_year.csv'
earthquake_df = pd.read_csv(url)
earthquake_df.head()
#    Unnamed: 0  Year Magnitude                   Location Depth (km)   MMI                                              Notes                         Event    Date
# 0           0  1939       7.8  Turkey, Erzincan Province         20   XII                At least 32,700 people were killed.      1939 Erzincan earthquake  27-Dec
# 1           1  1940       7.7    Romania, Vrancea County        133     X  1,000 people were killed in Romania and Moldov...       1940 Vrancea earthquake  10-Nov
# 2           2  1941       5.8      Yemen, Razih District         35  VIII                          1,200 people were killed.   1941 Jabal Razih earthquake  11-Jan
# 3           3  1942         7              Turkey, Erbaa         10    IX                          3,000 people were killed.  1942 Niksar–Erbaa earthquake  20-Dec
# 4           4  1943   7.5-7.7            Turkey, Çankırı         20    XI        Between 2,824 and 5,000 people were killed.   1943 Tosya–Ladik earthquake  27-Nov

#two index fields populated -remove Unnamed column
del(earthquake_df['Unnamed: 0'])
earthquake_df.head()
#    Year Magnitude                   Location Depth (km)   MMI                                              Notes                         Event    Date
# 0  1939       7.8  Turkey, Erzincan Province         20   XII                At least 32,700 people were killed.      1939 Erzincan earthquake  27-Dec
# 1  1940       7.7    Romania, Vrancea County        133     X  1,000 people were killed in Romania and Moldov...       1940 Vrancea earthquake  10-Nov
# 2  1941       5.8      Yemen, Razih District         35  VIII                          1,200 people were killed.   1941 Jabal Razih earthquake  11-Jan
# 3  1942         7              Turkey, Erbaa         10    IX                          3,000 people were killed.  1942 Niksar–Erbaa earthquake  20-Dec
# 4  1943   7.5-7.7            Turkey, Çankırı         20    XI        Between 2,824 and 5,000 people were killed.   1943 Tosya–Ladik earthquake  27-Nov


def find_phrase(p):
    return(lambda x: re.findall(r'{}'.format(p), x))

def get_phrase_count(phrase, data, col):
    phrase_results = data[col].apply(find_phrase(phrase))
    phraselist = list(filter(None, phrase_results))
    phraseCount = len(phraselist)
    return phraseCount

#find count of occurences -- case sensitive examples
get_phrase_count('At least', earthquake_df, 'Notes')
#25

get_phrase_count('at least', earthquake_df, 'Notes')
#4

#find a record based on partial match of text field
def get_df_record(phrase, data, col):
    phrase_results = data[col].apply(find_phrase(r'{}'.format(phrase)))
    phrase_bool = pd.Series([bool(x) for x in phrase_results], index = data.index)
    df_recs = data[phrase_bool]
    return df_recs



#based on partial match of location
get_df_record("sia, Yog\B", earthquake_df, 'Location')
#     Year Magnitude               Location Depth (km) MMI                                              Notes                       Event    Date
# 66  2006       6.4  Indonesia, Yogyakarta         10  IX  At least 28,903 people were killed, 137,883 we...  2006 Yogyakarta earthquake  27-May


#based on numbers at beginning or end of entire number in Notes
get_df_record("03\\b" ,earthquake_df, 'Notes')
#     Year Magnitude                            Location Depth (km)    MMI                                              Notes                       Event    Date
# 60  2000       7.9  Indonesia, Enggano Island offshore         44  VI[4]  This earthquake killed at least 103 people and...     2000 Enggano earthquake   4-Jun
# 66  2006       6.4               Indonesia, Yogyakarta         10     IX  At least 28,903 people were killed, 137,883 we...  2006 Yogyakarta earthquake  27-May

#find notes that have a number in the beginning or end of entire number accounting for comma separated numbers
get_df_record("12\\b*(\d),(\d)" ,earthquake_df, 'Notes')
# 64  2004       9.1  Indonesia, Sumatra offshore         30  IX  This is the third largest earthquake in the wo...  2004 Indian Ocean earthquake  26-Dec
# 66  2006       6.4        Indonesia, Yogyakarta         10  IX  At least 28,903 people were killed, 137,883 we...    2006 Yogyakarta earthquake  27-May

get_df_record("deadliest" ,earthquake_df, 'Notes')
#     Year Magnitude      Location Depth (km) MMI                                              Notes                     Event    Date
# 36  1976       7.6  China, Hebei       12.2  XI  242,719 people were officially counted as dead...  1976 Tangshan earthquake  28-Jul

get_df_record("worst" ,earthquake_df, 'Notes')
#     Year Magnitude           Location Depth (km) MMI                                              Notes                        Event    Date
# 45  1985         8  Mexico, Michoacán         20  IX  Between 5,000 and 45,000 were killed and 30,00...  1985 Mexico City earthquake  19-Sep

get_df_record("in the world" ,earthquake_df, 'Notes')
#     Year Magnitude                     Location Depth (km) MMI                                              Notes                         Event    Date
# 64  2004       9.1  Indonesia, Sumatra offshore         30  IX  This is the third largest earthquake in the wo...  2004 Indian Ocean earthquake  26-Dec

#number of records that used the term 'destroyed'
len(get_df_record("destroyed" ,earthquake_df, 'Notes'))
#28

#what is the average magnitude of the 28 data records that include the term 'destroyed' in the Notes col?
subset_df = get_df_record("destroyed" ,earthquake_df, 'Notes')
avg_mag = np.average(pd.to_numeric(subset_df['Magnitude']))
avg_mag
#7.064285714285714
