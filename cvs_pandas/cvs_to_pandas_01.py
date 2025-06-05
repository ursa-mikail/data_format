import pandas as pd

# Load CSV file into a pandas dataframe
df = pd.read_csv('https://raw.githubusercontent.com/mikail-eliyah-00/trial_00/refs/heads/main/data/heart_disease_uci.csv')

print(df.size)
print(df.shape)

number_of_rows = df.shape[0]
print(number_of_rows)
number_of_columns = df.shape[1]
print(number_of_columns)

print(df.info())
print(df.describe())
# print(df.describe().T)

print(df.head())
print(df.tail())

print(df.columns)

# print field-tags
# Print all field tags (column names) with their index
print("Field tags (column names):")
print(df.columns.tolist())

field_tags = df.columns.tolist()
for i in range(len(field_tags)):
    print(f"{i}: {field_tags[i]}")

row_number = 0

print(f"Row {row_number} data [START]")
print(df.iloc[row_number])
print(df.iloc[row_number, 0])
print(df.iloc[row_number, 1])
print(f"Row {row_number} data [END]")

# Select cell at row 2 and column 3
cell_value = df.iloc[2, 3]

# Print the value of the selected cell
print(cell_value)

# Example DataFrame
data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda'],
    'Age': [28, 24, 35, 32],
    'City': ['New York', 'Paris', 'Berlin', 'London']
}
df = pd.DataFrame(data)

# Print the column fields
print(df.columns)

# Sample DataFrame
data = {
    'PaymentMethod': ['Credit Card', 'Cash', 'Credit Card', 'Debit Card', 'Cash']
}
df = pd.DataFrame(data)

# Convert categorical variable into dummy/indicator variables
df_dummies = pd.get_dummies(df, columns=['PaymentMethod'])

# Convert True/False to 1/0 inplace. Convert the boolean values to integers.
df_dummies = df_dummies.astype(int)

print(df_dummies.head())

def pack_lists(*args):
    return list(zip(*args))

id = [1, 2, 3, 4]
leaders = ['Elon Ma', 'Tim Cook', 'Bill Gates', 'Sun Tze']
sex = ['male', 'male', 'male', 'male']

packed = pack_lists(id, leaders, sex)
print(packed)
# [(1, 'Elon Ma', 'male'), (2, 'Tim Cook', 'male'), (3, 'Bill Gates', 'male'), (4, 'Sun Tze', 'male')]

leaders.sort()  # This will sort by the full name in alphabetical order
print(leaders)

leaders.sort(key=lambda x: x.split()[0])  # This will sort by the first name
print(leaders)

leaders.sort(key=lambda x: x.split()[-1])  # This will sort by the last name
print(leaders)

"""
14720
(920, 16)
920
16
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 920 entries, 0 to 919
Data columns (total 16 columns):
 #   Column    Non-Null Count  Dtype  
---  ------    --------------  -----  
 0   id        920 non-null    int64  
 1   age       920 non-null    int64  
 2   sex       920 non-null    object 
 3   dataset   920 non-null    object 
 4   cp        920 non-null    object 
 5   trestbps  861 non-null    float64
 6   chol      890 non-null    float64
 7   fbs       830 non-null    object 
 8   restecg   918 non-null    object 
 9   thalch    865 non-null    float64
 10  exang     865 non-null    object 
 11  oldpeak   858 non-null    float64
 12  slope     611 non-null    object 
 13  ca        309 non-null    float64
 14  thal      434 non-null    object 
 15  num       920 non-null    int64  
dtypes: float64(5), int64(3), object(8)
memory usage: 115.1+ KB
None
               id         age    trestbps        chol      thalch     oldpeak  \
count  920.000000  920.000000  861.000000  890.000000  865.000000  858.000000   
mean   460.500000   53.510870  132.132404  199.130337  137.545665    0.878788   
std    265.725422    9.424685   19.066070  110.780810   25.926276    1.091226   
min      1.000000   28.000000    0.000000    0.000000   60.000000   -2.600000   
25%    230.750000   47.000000  120.000000  175.000000  120.000000    0.000000   
50%    460.500000   54.000000  130.000000  223.000000  140.000000    0.500000   
75%    690.250000   60.000000  140.000000  268.000000  157.000000    1.500000   
max    920.000000   77.000000  200.000000  603.000000  202.000000    6.200000   

               ca         num  
count  309.000000  920.000000  
mean     0.676375    0.995652  
std      0.935653    1.142693  
min      0.000000    0.000000  
25%      0.000000    0.000000  
50%      0.000000    1.000000  
75%      1.000000    2.000000  
max      3.000000    4.000000  
   id  age     sex    dataset               cp  trestbps   chol    fbs  \
0   1   63    Male  Cleveland   typical angina     145.0  233.0   True   
1   2   67    Male  Cleveland     asymptomatic     160.0  286.0  False   
2   3   67    Male  Cleveland     asymptomatic     120.0  229.0  False   
3   4   37    Male  Cleveland      non-anginal     130.0  250.0  False   
4   5   41  Female  Cleveland  atypical angina     130.0  204.0  False   

          restecg  thalch  exang  oldpeak        slope   ca  \
0  lv hypertrophy   150.0  False      2.3  downsloping  0.0   
1  lv hypertrophy   108.0   True      1.5         flat  3.0   
2  lv hypertrophy   129.0   True      2.6         flat  2.0   
3          normal   187.0  False      3.5  downsloping  0.0   
4  lv hypertrophy   172.0  False      1.4    upsloping  0.0   

                thal  num  
0       fixed defect    0  
1             normal    2  
2  reversable defect    1  
3             normal    0  
4             normal    0  
      id  age     sex        dataset               cp  trestbps   chol    fbs  \
915  916   54  Female  VA Long Beach     asymptomatic     127.0  333.0   True   
916  917   62    Male  VA Long Beach   typical angina       NaN  139.0  False   
917  918   55    Male  VA Long Beach     asymptomatic     122.0  223.0   True   
918  919   58    Male  VA Long Beach     asymptomatic       NaN  385.0   True   
919  920   62    Male  VA Long Beach  atypical angina     120.0  254.0  False   

              restecg  thalch  exang  oldpeak slope  ca          thal  num  
915  st-t abnormality   154.0  False      0.0   NaN NaN           NaN    1  
916  st-t abnormality     NaN    NaN      NaN   NaN NaN           NaN    0  
917  st-t abnormality   100.0  False      0.0   NaN NaN  fixed defect    2  
918    lv hypertrophy     NaN    NaN      NaN   NaN NaN           NaN    0  
919    lv hypertrophy    93.0   True      0.0   NaN NaN           NaN    1  
Index(['id', 'age', 'sex', 'dataset', 'cp', 'trestbps', 'chol', 'fbs',
       'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num'],
      dtype='object')
Field tags (column names):
['id', 'age', 'sex', 'dataset', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']
0: id
1: age
2: sex
3: dataset
4: cp
5: trestbps
6: chol
7: fbs
8: restecg
9: thalch
10: exang
11: oldpeak
12: slope
13: ca
14: thal
15: num
Row 0 data [START]
id                       1
age                     63
sex                   Male
dataset          Cleveland
cp          typical angina
trestbps             145.0
chol                 233.0
fbs                   True
restecg     lv hypertrophy
thalch               150.0
exang                False
oldpeak                2.3
slope          downsloping
ca                     0.0
thal          fixed defect
num                      0
Name: 0, dtype: object
1
63
Row 0 data [END]
Cleveland
Index(['Name', 'Age', 'City'], dtype='object')
   PaymentMethod_Cash  PaymentMethod_Credit Card  PaymentMethod_Debit Card
0                   0                          1                         0
1                   1                          0                         0
2                   0                          1                         0
3                   0                          0                         1
4                   1                          0                         0
[(1, 'Elon Ma', 'male'), (2, 'Tim Cook', 'male'), (3, 'Bill Gates', 'male'), (4, 'Sun Tze', 'male')]
['Bill Gates', 'Elon Ma', 'Sun Tze', 'Tim Cook']
['Bill Gates', 'Elon Ma', 'Sun Tze', 'Tim Cook']
['Tim Cook', 'Bill Gates', 'Elon Ma', 'Sun Tze']
"""