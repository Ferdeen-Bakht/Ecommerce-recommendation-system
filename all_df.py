# from database import Database
import numpy as np
import pandas as pd

df=pd.read_csv('sample.csv')

# db=Database()


# our goal was to create a database and store all the values creating three
# tables we did store the values in the database
# but we never user it instead we used the excell sheet for accessing login
# as our main goal was to show recommendations but if the project is improved
# we can make this website database dependent but right now it just works on
# sign in functionalities not sign up functionality

index=[]
for i in range(20000):
    index.append(i)
index_no=pd.DataFrame({'index':index})

# what we are trying to do is to create a set of values from 0 to 3999
# so that buyer id is uniqque and there are no missing values of buyers
# we are creating buyer id,email,name and password using dummy values
# as there is no infromation about user in sample.csv

# creating an array of values from 0 to 3999
arr_straight = np.arange(4000)

# Create array with 16000 random values between 0 and 4000
arr_random = np.random.randint(low=0, high=4000, size=16000)

# Concatenate the two arrays
arr_combined = np.concatenate((arr_straight, arr_random))

buyer_id1 = arr_combined


# Complete table
all_df=df.copy()

all_df['index']=index_no

# changing missing values of brand to NewBrand
for i in range(20000):
    if pd.isna(all_df.iloc[i]['brand']) or len(all_df.iloc[i]['brand']) == 0:
        all_df.iloc[i, all_df.columns.get_loc('brand')] = 'NewBrand'


all_df['b_id'] = buyer_id1

#creating item id with respect to product name every product will have its own unique id
all_df['i_id'] = all_df.groupby('product_name').ngroup() + 1
#creating seller id with respect to brand name every brand will have its own unique id
all_df['s_id'] = all_df.groupby('brand').ngroup() + 1

all_df = all_df.sort_values(by=['index'], ascending=True)


# putted dummy names,emails and passwords fro buyers and sellers
all_df['s_name'] = all_df['brand']
all_df['s_email'] = 'seller' + all_df['s_id'].astype(str) + '@gmail.com'
all_df['s_password'] = 'seller' + all_df['s_id'].astype(str)

all_df['b_name'] = 'buyer' + all_df['b_id'].astype(str)
all_df['b_email'] = 'buyer' + all_df['b_id'].astype(str) + '@gmail.com'
all_df['b_password'] = 'buyer' + all_df['b_id'].astype(str)

# dropping the irrelevent columns
all_df = all_df.drop(columns=['product_url', 'uniq_id', 'crawl_timestamp','pid','overall_rating','product_specifications','is_FK_Advantage_product','product_category_tree'])
# print(len(all_df))
#print(all_df)

# print(all_df['brand'])

# there was a place showing bug in the column brand so we corrected it
brand_size = df['brand'].str.len()

all_df.iloc[99, all_df.columns.get_loc('brand')] = 'NewBrand'

# print(brand_size[99])

#all_df.to_csv('all_df.csv', index=False)


# buyer df

# we have commented where we converted the data from excel to database

buyer_df = all_df[['b_id', 'b_name', 'b_email', 'b_password']].copy()
buyer_df = buyer_df.sort_values(by=['b_id'], ascending=True)
buyer_df = buyer_df.drop_duplicates(subset=['b_id'])




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

