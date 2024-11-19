from flask import Flask, render_template, redirect, request, session, url_for, abort
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

app.secret_key = 'your_secret_key'


# note that to use this file we have done some preprocessing in the the files pre_tf.py and all_df.py which
# will create two excel sheets small_vector.csv and all_df.csv after generating these excel sheets we can run
# this code

@app.route('/home', methods=['GET', 'POST'])
def home():
    # taky direct page load na hosaky kab tak login na kiya ho isliay condition if oali
    if 'name' in session and 'password' in session:

        name = session['name']
        password = session['password']
        print(name)
        print(password)

        # imported excel sheet and putted it in a dataframe
        # this is the most important excel sheet all datafraes and excell sheets are derived from it
        df = pd.read_csv('sample.csv')

        # COSINE SIMILIARITIES START

        # this contains the complete tf_idf vector in the same way you taught in the class dividing the magntitutes
        # with tf_idf etc for more information you can view pre_tf.py where it is calculated
        vector1 = pd.read_csv('small_vector.csv')

        # the dataframe was creating a garbage column itself without any reason so we removed it
        vector1 = vector1.drop(vector1.columns[0], axis=1)
        vector1 = vector1.drop(vector1.columns[0], axis=1)
        print(vector1.head(5))

        # print(len(vector1))

        def compute_cosine_similarities(df, row_index):
            # Extract the specified row
            target_row = df.iloc[row_index]

            # all the data including the target_row itself
            df_remaining = df

            # Compute cosine similarity
            cosine_similarities = cosine_similarity([target_row], df_remaining)

            return cosine_similarities.flatten()

        all_df = pd.read_csv('all_df.csv')

        # Create an empty list to store the values
        values_list = []

        # The variables that we accesed from the html login page gets the user either buyer0, buyer1 till
        # buyer19999 and gets all the items index in the dataframe all_df once it is obtained we will store
        # them in a list because we need to calculate cosine similiarities of the items not of users
        # so lets say buyer0 have purchased item eg 7 and 49 so it will be stored in a list
        if "b_name" in all_df.columns and "b_password" in all_df.columns:
            mask = (all_df["b_name"] == name) & (all_df["b_password"] == password)
            if mask.any():  # Check if there are any rows that satisfy the conditions
                values_list = all_df.loc[mask, "index"].tolist()
            else:
                print("No rows found that satisfy the conditions.")
        else:
            print("One or both of the columns 'b_name' and 'b_password' not found in DataFrame.")

        print(values_list)

        # Create an empty list to store the DataFrames
        list_1 = []
        list_2 = []

        for i in range(len(values_list)):
            # lets say buyer0 have purchased item eg 7 and 49
            # first row_index will be 7 second will be 49
            row_index = values_list[i]

            # we call the compute_cosine_similarities we defined above
            cosine_similarities = compute_cosine_similarities(vector1, row_index)

            # creating index of all rows from 0 to 19999
            index_range = np.arange(0, len(vector1))

            # values of first list will be saved lets say 7 then of 49
            list_1.append(cosine_similarities)
            list_2.append(index_range)

        # list of 7 and 49 are merged together
        list_1 = np.array(list_1).flatten().tolist()
        list_2 = np.array(list_2).flatten().tolist()

        # converted it into dataframe
        df_cos = pd.DataFrame({'index': list_2, 'cosine_similarities': list_1})
        print(df_cos.head(5))

        # we dont want to recommend same items more than once so we droped some of the values
        df_cos = df_cos.drop_duplicates(subset='cosine_similarities')
        df_cos = df_cos.drop_duplicates(subset='index')
        print(df_cos.head(5))  # merged thats why values are up and down

        tolerance = 0.001

        # Remove rows where cosine_similarities are very very close to 1
        # if it 1 it means it is the same item bought before which we are finding similiarity of lets say item 7
        # has 76 and 99 so they are removed
        df_cos1 = df_cos[abs(df_cos['cosine_similarities'] - 1) > tolerance]

        # sort it in decending order the values which will be heigher will be shown first
        df_cos1 = df_cos1.sort_values(by='cosine_similarities', ascending=False)

        print(df_cos1.head(10))

        # COSINE SIMILIARITIES END

        # Create a list of the sorted index values from df_cos1
        sorted_index_values = df_cos1['index'].tolist()

        # Sort the df DataFrame based on the sorted index values

        # sort the orignal dataset according to the the orignal dataset because it has the product_name ,images etc
        # which will be displayed on web page
        df_sorted = df.reindex(sorted_index_values)

        print(df_sorted.head(5))

        # # Reset the index to make it start from 0, 1, 2, ...
        df_sorted = df_sorted.reset_index(drop=True)

        # item=df[['product_name','retail_price','image']]
        # print(item.head())

        df = df_sorted
        df = df.head(50)
        print(df.head())

        # product name ola column access kiya or osko save kardia productname ky nam sy df my
        product_name = df[['product_name']]
        # used single brackets to make it series from a dataframe
        # making it one dimentional instead of two dimentional

        product_name = product_name['product_name']
        # print(product_name)

        retail_price = df[['retail_price']]
        # used single brackets to make it series from a dataframe
        # making it one dimentional instead of two dimentional

        retail_price = retail_price['retail_price']
        # print(retail_price)

        image = df[['image']]
        # image = image.head(10)
        # used single brackets to make it series from a dataframe
        # making it one dimentional instead of two dimentional
        # saf suthra kiya hy image ko unnessary chezain remove kari
        image = image['image'].str.replace('[', '').str.replace(']', '').str.replace('"', '')
        # print(image)

        discounted_price = df[['discounted_price']]
        discounted_price = discounted_price['discounted_price']
        # print(discounted_price)

        description = df[['description']]
        description = description['description']
        # print(description)

        product_rating = df[['product_rating']]
        product_rating = product_rating['product_rating']
        # print(product_rating)

        brand = df[['brand']]
        brand = brand['brand']
        # print(brand)

        # series ko lists my convert kiya hy taky javascript ki list my ye tabdeel hosakain
        product_name1 = []
        retail_price1 = []
        image1 = []
        discounted_price1 = []
        description1 = []
        product_rating1 = []
        brand1 = []

        for i in range(50):
            product_name1.append(product_name[i])

        for i in range(50):
            retail_price1.append(retail_price[i])

        for i in range(50):
            image1.append(image[i])

        for i in range(50):
            discounted_price1.append(discounted_price[i])

        for i in range(50):
            description1.append(description[i])

        for i in range(50):
            product_rating1.append(product_rating[i])

        for i in range(50):
            brand1.append(brand[i])

        # data session my store kiya tha ab access kar rahy

        return render_template('home.html',  # name=name,password=password,
                               product_name1=product_name1, retail_price1=retail_price1
                               , image1=image1, discounted_price1=discounted_price1
                               , description1=description1
                               , product_rating1=product_rating1
                               , brand1=brand1
                               )

    # put tf_idf.py here or my_pc.py
    # sort df with all_df because index of

    # return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # jab user login page py click kary ga tu jo input kiya hy oh save hoga
        name = request.form['name']
        password = request.form['pass']
        # SESSION my store kardia taky dosry page my access karsakain
        session['name'] = name
        session['password'] = password
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['name'] = ''
    session['password'] = ''
    return redirect(url_for('login'))


# @app.route('/cart')
# def cart():
#     return render_template('cart.html')

# @app.route('/signup')
# def signup():
#     return render_template('sign.html')

@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run(debug=True)