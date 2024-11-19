#from flask import Flask, render_template, redirect, request, session, url_for, abort
#from database import Database
import pandas as pd
import numpy as np

#app = Flask(__name__)

#app.secret_key = 'your_secret_key'


# this file describes tf-idf vector in the same way that was taught in class
# with one exception

# FROM THE COMMENT START TO COMMENT END IS ALREADY DESCRIBED IN all_df.py


# START

df=pd.read_csv('sample.csv')

#db=Database()


index=[]
for i in range(20000):
    index.append(i)
index_no=pd.DataFrame({'index':index})


arr_straight = np.arange(4000)

# Create array with 16000 random values between 0 and 4000
arr_random = np.random.randint(low=0, high=4000, size=16000)

# Concatenate the two arrays
arr_combined = np.concatenate((arr_straight, arr_random))

buyer_id1 = arr_combined


# Complete table
all_df=df.copy()

all_df['index']=index_no

for i in range(20000):
    if pd.isna(all_df.iloc[i]['brand']) or len(all_df.iloc[i]['brand']) == 0:
        all_df.iloc[i, all_df.columns.get_loc('brand')] = 'NewBrand'


all_df['b_id'] = buyer_id1

all_df['i_id'] = all_df.groupby('product_name').ngroup() + 1
all_df['s_id'] = all_df.groupby('brand').ngroup() + 1

all_df = all_df.sort_values(by=['index'], ascending=True)


all_df['s_name'] = all_df['brand']
all_df['s_email'] = 'seller' + all_df['s_id'].astype(str) + '@gmail.com'
all_df['s_password'] = 'seller' + all_df['s_id'].astype(str)

all_df['b_name'] = 'buyer' + all_df['b_id'].astype(str)
all_df['b_email'] = 'buyer' + all_df['b_id'].astype(str) + '@gmail.com'
all_df['b_password'] = 'buyer' + all_df['b_id'].astype(str)

all_df = all_df.drop(columns=['product_url', 'uniq_id', 'crawl_timestamp','pid','overall_rating','product_specifications','is_FK_Advantage_product','product_category_tree'])
# print(len(all_df))
#print(all_df)

# print(all_df['brand'])

brand_size = df['brand'].str.len()

all_df.iloc[99, all_df.columns.get_loc('brand')] = 'NewBrand'

# print(brand_size[99])

#all_df.to_csv('all_df.csv', index=False)


# buyer df

buyer_df = all_df[['b_id', 'b_name', 'b_email', 'b_password']].copy()
buyer_df = buyer_df.sort_values(by=['b_id'], ascending=True)
buyer_df = buyer_df.drop_duplicates(subset=['b_id'])
#

# db.CreateTableBuyer()
# db.CreateTableSeller()

#
# for i in range(len(buyer_df)):
#     b_id = buyer_df.iloc[i, 0]
#     b_name = buyer_df.iloc[i,1]
#     b_email = buyer_df.iloc[i,2]
#     b_password = buyer_df.iloc[i,3]
#
#     print('bid:',b_id)
#     # print('b_name: ',b_name)
#
#     db.insertIntoBuyer(b_id, b_name, b_email, b_password)
#


# items=db.returnBuyer()
# print(items)
#buyer_df.to_csv('buyer_df.csv',index=False)

# seller df

seller_df = all_df[['s_id','s_name', 's_email', 's_password']].copy()
seller_df = seller_df.sort_values(by=['s_id'], ascending=True)
seller_df = seller_df.drop_duplicates(subset=['s_id'])
#seller_df.to_csv('seller_df.csv',index=False)

# for i in range(len(seller_df)):
#
#     s_id = seller_df.iloc[i, 0]
#     s_name = seller_df.iloc[i, 1]
#     s_email = seller_df.iloc[i, 2]
#     s_password = seller_df.iloc[i, 3]
#
#     print('sid:',s_id)
#     print('s_name: ',s_name)
#
#     db.insertIntoSeller(s_id, s_name, s_email, s_password)

# items=db.returnSeller()
# print(items)

# item df
item_df = all_df.drop(columns=['b_name', 'b_email', 'b_password', 's_name', 's_email', 's_password'])
item_df['image'] = item_df['image'].str.replace('[', '').str.replace(']', '').str.replace('"', '')
item_df['image'] = item_df['image'].str.split(',').str[0]
#item_df.to_csv('item_df.csv', index=False)
#
# db.CreateTableItem()

#product_name	retail_price	discounted_price	image	description	product_rating	brand	index	b_id	i_id	s_id
# for i in range(len(item_df)):
#     product_name = item_df.iloc[i, 0]
#     retail_price = item_df.iloc[i, 1]
#     discounted_price = item_df.iloc[i, 2]
#     image = item_df.iloc[i, 3]
#     description = item_df.iloc[i, 4]
#     product_rating = item_df.iloc[i, 5]
#     brand = item_df.iloc[i, 6]
#     item_index = item_df.iloc[i, 7]
#     buyer_id = item_df.iloc[i, 8] + 1
#     i_id = item_df.iloc[i, 9]
#     seller_id = item_df.iloc[i, 10]
#     print('buyer_id:', buyer_id)
#     print('retail_price: ', retail_price)
#     db.insertIntoItem(item_index, product_name, retail_price, discounted_price, image, description, product_rating, brand, buyer_id, i_id, seller_id)

# items = db.returnItem()
# print(items)

## END

##### RECOMMENDATION PROCESS STARTS

## TF-IDF starts

max_levels = 0
for item in df['product_category_tree']:
    count = len(item.split(">>"))
    if count > max_levels:
        max_levels = count

# print("The data has", max_levels, "levels")


# create an empty list to store the split categories
split_category_list = []

for category in df['product_category_tree']:
    # spliting
    split_category = category.split('>>')
    # spliting and putting in 2D list
    split_category_list.append(split_category)

# print(split_category_list[1:10])

# breaked into individual words
words = []
for categories in split_category_list:
    for category in categories:
        words += category.split()

# print(words[1:30])
words = [word for word in words if len(word) > 1]

words = [w.replace("'", "").replace('"', '').replace('(', '').
             replace(')', '').replace('[', '').
         replace(']', '').replace('...', '').
         replace(',', '')for w in words]

# print('Words\n',words[1:30])

#unique_words = []
# for word in words:
#     if word not in unique_words: # jab pehly sy hi hoga tu  dobara nahi jaey ga tokri my
#         unique_words.append(word)


unique_words = set(words) # removes duplicates
unique_words=sorted(list(unique_words))

# Define the list of words to remove #remove strat
words_to_remove = ['', '&', '+1', '-', '-446', '-522', '-583', '-B150AC', '-R-MEDIUM3', '-Therap', '-value', '.43X', '0', '0-100', '0-15', '0.5', '0019', '002-SE', '0024', '011', '01400-0015', '017', '03', '0303', '04', '0401-002', '05', '05102', '052', '06', '0622', '07', '08HD-ES-62', '1', '1-g--nike-m', '1-st1b--nike-m', '1.5', '1.75', '10', '10%', '10.5v2.9a', '100', '100%', '100/90-17', '1000', '10000', '10000mAh', '10000mah', '1000m', '1005', '1019', '1033', '1038', '1042', '105key', '106', '1066.', '107751', '109F', '109f', '10X70X70', '10\\', '11', '110', '112', '1150', '119M', '12', '12.7', '120', '1200', '12000', '1219', '122/1000M', '123', '125g', '12V/24V', '12W', '12\\', '13', '13.97', '1320', '135ml', '138246', '14', '14.5', '140/70-17', '142492', '144', '145', '145744', '147', '148', '149', '14K', '15', '15.24X20.32', '15.6', '150', '1500', '150013', '15052HTCX9-SKN', '15059HTCX9-SKN', '1514', '1524', '154', '154222', '154226', '154235', '154243', '154253', '154257', '154266', '154267', '154274', '154280', '154298', '154314', '154317', '154320', '154324', '154325', '154326', '154331', '154357', '154388', '154402', '154422', '154433', '154436', '154438', '154439', '155489', '157466', '157497', '15cmx10cm', '15mtr', '16', '16-510', '160/2gb/DDR2', '1600W', '161', '165', '166', '169', '169-CIN', '17', '170', '1706201621', '170760', '170774', '170783', '170792', '170798', '170817', '170822', '170831', '170906', '170909', '171', '172', '17500', '17502', '17505', '17507', '176', '179', '18', '18.5', '180', '1828.8', '1829', '183', '186', '186136', '186879', '186926', '187', '18K', '18W', '19', '19.5', '19.5v3.9a', '190', '1905', '194', '196', '1981.199999999', '1OAK', '1Pair', '1kg', '1m189', '1pack', '1pcs', '1pen', '1x2GB', '2', '2-D-', '2-Fo', '2-Ma', '2-O-', '2.0', '2.1', '2.25', '2.5', '2.75-17', '2.75-18', '2.8', '20', '20%', '20.2', '20.4', '200', '2000', '2006', '2015-2016', '2016-2017', '20200W', '202050', '202051', '202056', '202058', '20503', '207232', '208', '20881', '20mtr', '21', '210', '2110', '2113', '2133.6', '216', '216008', '216456', '216510', '216552', '217', '218', '2188-4', '22', '220', '220102', '220106', '220108', '220113', '220164', '220165', '220175', '220179', '225', '225-Button', '22K', '22nd', '23', '23000', '2300W', '232241', '2323', '232305', '232358', '2333', '236', '24', '240', '240306', '240318', '240319', '240322', '240325', '240327', '240342', '240350', '240362', '240363', '240371', '240403', '240404', '240408', '240411', '240420', '240421', '240428', '240437', '240439', '240440', '240450', '240459', '240460', '240461', '245', '247', '24K', '24ct', '24kt', '25', '250', '256-SPM', '25868', '26', '2615.023.132', '26cm', '27', '270', '273', '28', '280', '280r', '290', '2nd', '3', '3-speed', '3.0', '3.00-18', '3.1', '3.2', '3.4', '3.5', '3.50-10', '3.50-19', '3.5mm', '3/4', '3/4ths', '30', '30.4', '300', '3000', '31', '32', '320', '325', '3250', '33568', '33649', '34', '343', '35', '35.56', '350', '3500i', '3514', '354', '36', '360', '365', '38', '3Bright', '3D', '3D+', '3R', '3d', '3g', '3in1', '3kFactory', '3wish', '4', '4.00-8', '4.1', '4.25g', '4.26', '4.3', '4.5', '4.8V', '4/4s/4g/5/5c', '40', '400', '4000', '4102', '420', '4202', '428', '43', '434', '45', '450', '456', '45W', '46', '460', '475', '476', '477', '48', '483', '497', '4C', '4D', '4G', '4K', '4S', '4U', '4X', '4i', '4mm', '4s', '4thneed', '5', '5.5', '5.5x5.5', '50', '500', '5000', '5000mah', '502', '503TF_BLK', '51', '510', '52', '520', '526', '52Mm', '52mm', '53', '54', '55', '550', '56', '56m', '57', '58', '59', '591', '5921', '5A', '5I', '5SL', '5X', '6', '6.35', '60', '600', '60W', '61', '612', '62', '620', '633D', '64', '66', '67', '67mm', '684658-003', '69SS0002-X1', '69SS0003-B6', '69th', '6LED', '6P', '6S', '6W', '7', '7.6', '7.62', '70', '720', '7230', '728S', '73171', '75', '750', '7512_TM_P', '7562', '762', '77', '77306', '77341', '77365', '77370', '77374', '77489', '77538', '77551', '77555', '77565', '77595', '77599', '7I', '7\\', '7in', '8', '8.646', '80', '800', '83.820', '85', '8520', '85W', '86', '883', '8908-1', '8K', '8\\', '9', '9.40', '9.8250000000', '90', '91', '9107or', '9340', '9500', '99', '999', '999store', '99Gems', '99Hunts', '99Moves', '9LED', '9V', '9\\', '@499', '@home']

# Remove the words from the list
for word in words_to_remove:
    while word in unique_words:
        unique_words.remove(word)

# remove words with less than 2 length
unique_words = [word for word in unique_words if len(word) > 2] # we can remove words to remove finctionlity
#remove end

# Print the updated list
# print('Unique words\n', unique_words[1:30])

# print('Length: ',len(unique_words))

# if 'Womens' in unique_words:
#     print('Yes, the list contains "Womens"')
# else:
#     print('No, the list does not contain "Womens"')





#words_2d=unique_words
words_2d=split_category_list
words_2d = [[w.replace("'", "").replace('"', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('...', '').replace(',', '') for w in sublist] for sublist in words_2d]

# splited into individual words
words_2d = [[word for phrase in sublist for word in phrase.split()] for sublist in words_2d]

# print(words_2d[1:30])

## TF (TERM FREQUENCY) STARTS


# print('Term frequency dataframe\n',tf_df)

# empty 2d list bana rahy
tf_list = []

# Populate the list with empty sublists
for i in range(20000):
    row=[]
    word_row=words_2d[i]
    for j in range(len(word_row)):
        row.append('')
    tf_list.append(row)

# print(tf_list)


# intialize kardo sub values ko 0
for i in range(20000):
    word_row=words_2d[i]
    for j in range(len(word_row)):
        tf_list[i][j]=0

# print(tf_list)

# words removed doesnot matter as key will become 0

# agar ohi word dubara aey tu +1 kardo kitni bar aik word aya hy aik row my
for i in range(20000):
    word_row=words_2d[i]
    len1=len(word_row)
    for j in range(len(word_row)):
        for k in range(len(word_row)):
            if words_2d[i][j]==words_2d[i][k]:
                tf_list[i][j]=tf_list[i][j]+1


for i in range(9):
  word_row=words_2d[i]
  for j in range(len(word_row)): #10
    print(words_2d[i][j],end=' ')
  print('')

for i in range(9):
  word_row=words_2d[i]
  for j in range(len(word_row)): #10
    print(tf_list[i][j],end=' ')
  print('')


# the term frequency is calculated in a different way then described in class
# because according to the data
# word ko apni row ki length sy divide kardia
for i in range(20000):
    word_row=words_2d[i]
    len1=len(word_row)
    for j in range(len(word_row)):
        tf_list[i][j]=round(tf_list[i][j]/len1,2)

# print(tf_list[0:30])
# print(word_row[0:30])
print(len(word_row))

# just printing the values
for i in range(9):
  word_row=words_2d[i]
  for j in range(len(word_row)): #10
    print(tf_list[i][j],end=' ')
  print('')


# tf_df = pd.DataFrame(0,index=range(20000),columns=unique_words)
# if any("Womens" in col_name for col_name in tf_df.columns):
#     print('Yes')
# else:
#     print('No')

tf_df = pd.DataFrame(0,index=range(10),columns=unique_words)


# for i in range(10): #computation too large so instead we used for i, word_row in enumerate(words_2d):
#   word_row=words_2d[i]
#   for j in range(len(word_row)):
#       tf_df.loc[i,words_2d[i][j]]=tf_list[i][j]
#
# tf_df.fillna(0, inplace=True)
#
# print(tf_df)
# tf_df.to_csv('small_tf.csv')

# create an empty matrix of the same size as tf_df
tf_array = np.zeros((len(words_2d), len(unique_words)))

# update tf_array with the values from tf_list
for i, word_row in enumerate(words_2d):
    j_indices = [unique_words.index(word) for word in word_row if word in unique_words]
    tf_array[i, j_indices] = tf_list[i][:len(j_indices)]

# convert tf_array back to a DataFrame
tf_df = pd.DataFrame(tf_array, columns=unique_words)

# fill NaN values with 0
tf_df.fillna(0, inplace=True)

print(tf_df)

# tf_df.to_csv('large_df.csv')

## TF (TERM FREQUENCY) ENDS

# IDF
no_of_sentences=len(split_category_list) # no of rows in dataframe(should it not be no of columns)
print('No of sentences: ',no_of_sentences)
tf_df_array = tf_df.to_numpy()



# No of sentences
non_zero_counts = np.divide(np.count_nonzero(tf_df_array, axis=0),no_of_sentences)

word_repeated = np.count_nonzero(tf_df_array, axis=0)
word_repeated=pd.DataFrame({'column_name':tf_df.columns,'word_repeated':word_repeated})
word_repeated.to_csv('word_repeated.csv', index=False)

before_log = pd.DataFrame({'column_name': tf_df.columns, 'non_zero_count': non_zero_counts})

# Save DataFrame to CSV file
# before_log.to_csv('before_log.csv', index=False)


# Replace 0 values with NaN to avoid taking logarithm of 0
non_zero_counts[non_zero_counts == 0] = np.nan

# Take logarithm of non-zero values
non_zero_counts = np.log10(non_zero_counts)

# Replace NaN values with 0
non_zero_counts = np.nan_to_num(non_zero_counts)

# Create DataFrame from non_zero_counts array
df_counts = pd.DataFrame({'column_name': tf_df.columns, 'non_zero_count': non_zero_counts})

# Save DataFrame to CSV file
# df_counts.to_csv('non_zero_counts.csv', index=False)


df_counts = pd.DataFrame(non_zero_counts.reshape(1, -1), columns=tf_df.columns)



# Save DataFrame to CSV file
# non_zero_counts1.csv or non_zero_counts.csv same hain ya nahi
# df_counts.to_csv('non_zero_counts1.csv', index=False)
# yes they are same

## IDF ends

print('TF shape: ',np.shape(tf_df_array))
print('IDF shape: ',np.shape(non_zero_counts))
non_zero_counts.reshape([8089,1])
print('IDF shape: ',np.shape(non_zero_counts))
tf_idf=tf_df_array * non_zero_counts
print('TF_IDF shape: ',np.shape(tf_idf))


df_tf_idf=pd.DataFrame(tf_idf,columns=tf_df.columns)
#df_tf_idf.to_csv('large_tf_idf.csv')

tf_idf_square=np.square(tf_idf)
print(np.shape(tf_idf))
df_tf_idf_square=pd.DataFrame(tf_idf_square,columns=tf_df.columns)
#df_tf_idf_square.to_csv('tf_idf_square.csv')

sum_tf_idf=np.sum(tf_idf_square,axis=1,keepdims=True)
print('Sum\n',sum_tf_idf) # just print it only 10 values no need to convert into csv

sqrt_tf_idf=np.sqrt(sum_tf_idf)
print('Sqrt\n',sqrt_tf_idf)

print('TF_IDF shape: ',np.shape(tf_idf))
print('Sqrt shape: ',np.shape(sqrt_tf_idf))
df_sqrt = pd.DataFrame(sqrt_tf_idf)
# df_sqrt.to_csv('df_sqrt.csv')

vector=np.divide(tf_idf,sqrt_tf_idf)
print('Vector\n',vector)
df_vector=pd.DataFrame(vector,columns=tf_df.columns)
# df_vector.to_csv('vector.csv')

# TF-IDF ends

#vector=pd.read_csv('vector.csv')
vector=df_vector

word_unique = pd.read_csv('word_repeated.csv')
column_list = word_unique[word_unique['word_repeated'] == 1]['column_name'].tolist()
print(column_list)
print(len(column_list))

print("Number of columns:", vector.shape[1])
vector = vector.drop(columns=column_list)
print(vector[0:5])

print('start')
row_sum = vector.sum(axis=1)
print(row_sum[0:10])

vector = vector.drop(vector.columns[0], axis=1)

row_sum = vector.sum(axis=1)
print(row_sum[0:10])

print('end')
print(vector[0:5])
print("Number of columns:", vector.shape[1])

vector.to_csv('small_vector.csv')