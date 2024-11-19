import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import Input, Reshape, Dot, Embedding
from keras.optimizers import Adam

# Load the data
all_df = pd.read_csv('all_df.csv')
matrix = all_df[['b_id', 'i_id', 'product_rating']]
matrix['product_rating'] = matrix['product_rating'].replace('No rating available', 0).astype(float)
matrix.loc[:, 'product_rating'] = matrix['product_rating'].replace('No rating available', 0).astype(float)

matrix['product_rating'] = matrix['product_rating'].astype(float)

print(matrix['product_rating'].head())
min_rating = min(matrix['product_rating'])
max_rating = max(matrix['product_rating'])
print('Min',min_rating,max_rating)


# Label Encoder puts the values in a specific range
user_enc = LabelEncoder()
matrix['user'] = user_enc.fit_transform(matrix['b_id'].values)
n_users = matrix['user'].nunique()

item_enc = LabelEncoder()
matrix['item'] = item_enc.fit_transform(matrix['i_id'].values)
n_items = matrix['item'].nunique()

# Prepare the data for training
X = matrix[['user', 'item']].values
Y = matrix['product_rating'].values


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

# Define the model architecture
def Recommender(n_users, n_items, n_factors):
    user_input = Input(shape=(1,))
    item_input = Input(shape=(1,))

    # this neural network does not use activations instead it uses embeddings
    user_embedding = Embedding(n_users, n_factors)(user_input)
    item_embedding = Embedding(n_items, n_factors)(item_input)
    user_vecs = Reshape((n_factors,))(user_embedding)
    item_vecs = Reshape((n_factors,))(item_embedding)
    y = Dot(axes=1)([user_vecs, item_vecs])
    model = Model(inputs=[user_input, item_input], outputs=y)
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))
    return model

# Set model parameters
n_factors = 50

# Create and compile the model
model = Recommender(n_users, n_items, n_factors)
model.summary()

# Train the model
model.fit(x=[X_train[:, 0], X_train[:, 1]], y=Y_train, batch_size=64, epochs=5, verbose=1, validation_data=([X_test[:, 0], X_test[:, 1]], Y_test))

# Predict ratings
def predict_ratings(user_ids, item_ids, model):
    user_ids = np.array(user_ids)
    item_ids = np.array(item_ids)
    predictions = model.predict([user_ids, item_ids])
    return predictions.flatten()


# We tried to predict it on the actual dataframe but changing the list size was showing errors

# Example usage:
# values_list1 = []
#
# # Check if the conditions are met and retrieve the values
# if "b_name" in all_df.columns and "b_password" in all_df.columns:
#     user_id=all_df['b_id']
#     mask1 = (all_df["b_name"] != "buyer0") & (all_df["b_password"] != "buyer0")
#     if mask1.any():  # Check if there are any rows that satisfy the conditions
#         values_list1 = all_df.loc[mask1, "index"].tolist()
#     else:
#         print("No rows found that satisfy the conditions.")
# else:
#     print("One or both of the columns 'b_name' and 'b_password' not found in DataFrame.")
#
# print(values_list1)

#print('userid:',user_id)
user_id = 0
item_ids = [2, 3]
                                #user_id
predicted_ratings = predict_ratings([user_id] * len(item_ids), item_ids, model)

# Print the predicted ratings
for item_id, rating in zip(item_ids, predicted_ratings):
    print(f"Predicted rating for user {user_id} and item {item_id}: {rating}")
