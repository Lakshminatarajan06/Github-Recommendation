import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors

# Fit Knn algorithm
knn = NearestNeighbors(metric='cosine', algorithm='brute')

# Unpickle the required data
with open(r'C:\Users\Good Day\Desktop\Final Project\recommendation_final.pkl', 'rb') as file:
    rec_data = pickle.load(file)

# Extract the files
data_final = rec_data['data']
csr_final = rec_data['csr_data']
knn = rec_data['knn']
result_df = rec_data['result_df']

# Function to get user recommendations
def get_user_recommendation(username):
    n_users_to_recommend = 10

    # Check if the username exists in the data
    username_list = result_df[result_df['username_encode'] == username]

    if not username_list.empty:
        # Get the index of the first matching username
        user_idx = username_list.index[0]

        # Find neighbors
        distances, indices = knn.kneighbors(csr_final[user_idx], n_neighbors=n_users_to_recommend + 1)

        # Remove the input user index from the recommendations
        rec_user_indices = [idx for idx in indices.squeeze().tolist() if idx != user_idx][:n_users_to_recommend]

        recommend_frame = []

        for neighbor_idx in rec_user_indices:
            neighbor_data = result_df.iloc[neighbor_idx]
            neighbor_username = neighbor_data['username']
            public_repositories = neighbor_data['public_repositories']
            total_commits = neighbor_data['total_commits']
            languages = neighbor_data['languages']
            repositories = neighbor_data['stars_per_repository']
            recommend_frame.append({
                'Username': neighbor_username,
                'Public_Repositories': public_repositories,
                'Total_Commits': total_commits,
                'Languages': languages,
                'Repositories': repositories
            })

        df = pd.DataFrame(recommend_frame, index=range(1, n_users_to_recommend + 1))
        return df

    else:
        return "No users found. Please check your input"





