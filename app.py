import streamlit as st
import datetime
import pandas as pd
import pymongo
import pickle
from pymongo import MongoClient
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


myclient='mongodb://localhost:27017/'
collection=MongoClient(myclient).project.final

# Retrieve options from MongoDB
options = [record['username'] for record in collection.find()]

# Page configuration
st.set_page_config(page_title="Github Recommendation System", layout="wide", initial_sidebar_state="expanded")

def background():
    st.markdown("""
        <style>
        .main {
            background-color: #ffe6f0;
            padding: 20px;
        }
        .title {
            font-size: 2.5em;
            color: #333333;
            text-align: center;
            margin-bottom: 20px;
            font-family: 'Arial', sans-serif;
        }
        .subtitle {
            font-size: 1.5em;
            color: #555555;
            text-align: center;
            margin-bottom: 30px;
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #e0f7fa;
            padding: 20px;
            border-radius: 8px;
            }
        .stButton>button {
            color: blue;
            background-color: #cce5ff;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            
            font-family: 'Arial', sans-serif;
            font-size: 1em;
        }
        .stButton>button:hover {
            background-color: #cce5ff;
            
        }
        </style>
        """, unsafe_allow_html=True)
background()

# Title and subtitle
st.markdown('<div class="title">GitHub User Analytics and Recommendation System</div>', unsafe_allow_html=True)


# Sidebar
st.sidebar.title("Sidebar Menu")
st.sidebar.write("Use this sidebar to navigate through the app.")

option = st.sidebar.radio("Select an option", ['User Analytics', 'Recommendation System'])

if option=='User Analytics':

    username=st.selectbox('Choose Username', options)

    col_width=[1,2]
    col1, col2=st.columns(col_width)
    with col1:
        
        if username:
            user_record=collection.find_one({'username':username})
            time_str=user_record['created_on']
            time_str1=user_record['updated_on']
            
            time=datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
            time1=datetime.datetime.strptime(time_str1, '%Y-%m-%dT%H:%M:%SZ')

            # name=collection.find({'username':username})
            if user_record and 'avatar' in user_record:
                st.image(user_record['avatar'], width=200)

            else:
                st.write('No Avatar isfound for selected User')
    
    with col2:

        colx,coly,colz=st.columns(3)

        with colx:


            if user_record and 'name' in user_record:
                st.write('Name:', user_record['name'])

            if user_record and 'created_on' in user_record:
                current_date=datetime.datetime.now()
                year=current_date-time
                years=year.days//365
                month=year.days%365
                months=month//30
                st.write(f'Joined Github: {years} years {months} months ago')

            if 'url' in user_record:
                st.link_button('View Profile', user_record['url'])
            
        with coly:
            
            if user_record and 'bio' in user_record:
                st.write('Bio:', user_record['bio'])
            
            if 'updated_on' in user_record:
                current_date=datetime.datetime.now()
                days=current_date-time1
                days=days.days
                
                st.write(f'Last Logged: {days} days back')


            
        with colz:

            if user_record and 'public_repositories' in user_record:
                st.write('Public Repos:', user_record['public_repositories'])

            if 'total_commits' in user_record:
                st.write('Total Commits:', user_record['total_commits'])

            if 'following_count' in user_record:
                st.write('Following:', user_record['following_count'])

            if 'follower_count' in user_record:
                st.write('Followers:', user_record['follower_count'])

    # Add a line break between each iteration
    st.markdown("<hr>", unsafe_allow_html=True) 


    colx,coly,colz=st.columns(3)

    with colx:

        if 'repository_per_language' in user_record:
            try:
                repo_per_language=user_record['repository_per_language']

                st.markdown("<span style='color: blue;'>Repo Per Language - Top 10</span>", unsafe_allow_html=True)

                # Extract keys and values in repo per language
                repo_languages=list(repo_per_language.keys())
                repo_count=list(repo_per_language.values())

                # Sort languages and counts by counts
                sorted_indices = sorted(range(len(repo_count)), key=lambda k: repo_count[k], reverse=True)
                sorted_languages = [repo_languages[i] for i in sorted_indices]
                sorted_counts = [repo_count[i] for i in sorted_indices]

                # Top 10 repository
                top_sorted_languages=sorted_languages[:10]
                top_sorted_counts=sorted_counts[:10]

                # Plot the doughnut chart using Matplotlib
                fig, ax=plt.subplots(figsize=(10, 10))
                fig.patch.set_facecolor('none')  # Remove the white background

                wedges, texts, autotexts = ax.pie(
                                                    top_sorted_counts, 
                                                    labels=top_sorted_languages,  # Add labels
                                                    startangle=90, 
                                                    wedgeprops={'edgecolor': 'black'},
                                                    autopct='%1.1f%%',  # Display percentage labels
                                                    pctdistance=0.75,  # Position the percentage labels
                                                    textprops={'fontsize': 12}  # Font size for labels
                                                )


                ax.pie(top_sorted_counts, startangle=90, wedgeprops={'edgecolor':'black'})
                # Add legend based on the labels
                # ax.legend(sorted_languages, title='Languages', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

                # Draw a white circle at the center to create the doughnut shape
                center_circle = plt.Circle((0, 0), 0.50, color='black', fc='white')
                ax.add_artist(center_circle)

                ax.axis('equal')
                
                # Display the chart using Streamlit
                st.pyplot(fig)
            except:
                st.write("No values found")

    with coly:

        if 'stars_per_language' in user_record:
            try:
                stars_per_language=user_record['stars_per_language']

                st.markdown("<span style='color: blue;'>Stars Per Language- Top 10</span>", unsafe_allow_html=True)

                star_language=list(stars_per_language.keys())
                star_count=list(stars_per_language.values())

                # Sort languages and counts by counts
                sorted_indices=sorted(range(len(star_count)), key=lambda k: repo_count[k], reverse=True)
                sorted_counts=[star_count[i] for i in sorted_indices]
                sorted_languages=[star_language[i] for i in sorted_indices]

                # Top 10 repos per language
                top_sorted_counts=sorted_counts[:10]
                top_sorted_languages=sorted_languages[:10]


                # Plot the doughnut chart using Matplotlib
                fig, ax=plt.subplots(figsize=(10, 10))
                fig.patch.set_facecolor('none')  # Remove the white background

                wedges, texts, autotexts = ax.pie(
                                                    top_sorted_counts, 
                                                    labels=top_sorted_languages,  # Add labels
                                                    startangle=90, 
                                                    wedgeprops={'edgecolor': 'black'},
                                                    autopct='%1.1f%%',  # Display percentage labels
                                                    pctdistance=0.75,  # Position the percentage labels
                                                    textprops={'fontsize': 10}  # Font size for labels
                                                )


                ax.pie(top_sorted_counts, startangle=90, wedgeprops={'edgecolor':'black'})
                # Add legend based on the labels
                # ax.legend(top_sorted_languages, title='Languages', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

                # Draw a white circle at the center to create the doughnut shape
                center_circle = plt.Circle((0, 0), 0.50, color='black', fc='white')
                ax.add_artist(center_circle)

                ax.axis('equal')
                
                # Display the chart using Streamlit
                st.pyplot(fig)
            except:
                st.write("No values found")
    with colz:

        if 'commits_per_language' in user_record:
            try:
                commits_per_language=user_record['commits_per_language']

                st.markdown("<span style='color: blue;'>Commits Per Language- Top 10</span>", unsafe_allow_html=True)

                commit_language=list(commits_per_language.keys())
                commit_count=list(commits_per_language.values())

                # Sort languages and counts by counts
                sorted_indices=sorted(range(len(commit_count)), key=lambda k: commit_count[k], reverse=True)
                sorted_counts=[commit_count[i] for i in sorted_indices]
                sorted_languages=[commit_language[i] for i in sorted_indices]

                # Top 10 repos
                top_sorted_counts=sorted_counts[:10]
                top_sorted_languages=sorted_languages[:10]

                # Plot the doughnut chart using Matplotlib
                fig, ax=plt.subplots(figsize= (10, 10))
                fig.patch.set_facecolor('none')  # Remove the white background

                wedges, texts, autotexts = ax.pie(
                                                    top_sorted_counts, 
                                                    labels=top_sorted_languages,  # Add labels
                                                    startangle=90, 
                                                    wedgeprops={'edgecolor': 'black'},
                                                    autopct='%1.1f%%',  # Display percentage labels
                                                    pctdistance=0.75,  # Position the percentage labels
                                                    textprops={'fontsize': 10}  # Font size for labels
                                                )


                ax.pie(top_sorted_counts, startangle=90, wedgeprops={'edgecolor':'black'})
                # Add legend based on the labels
                # ax.legend(sorted_languages, title='Languages', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

                # Draw a white circle at the center to create the doughnut shape
                center_circle = plt.Circle((0, 0), 0.50, color='black', fc='white')
                ax.add_artist(center_circle)

                ax.axis('equal')
                
                # Display the chart using Streamlit
                st.pyplot(fig)
            except:
                st.write("No values found")

    cola,colb,colc=st.columns(3)

    with cola:

        if 'stars_per_repository' in user_record:

            try:

                st.markdown("<span style='color: blue;'>Stars Per Repo (Top-5)</span>", unsafe_allow_html=True)

                stars_per_repo=user_record['stars_per_repository']

                star_repo=list(stars_per_repo.keys())
                star_count=list(stars_per_repo.values())

                # Sort repo and stars by counts
                sorted_indices=sorted(range(len(star_count)), key=lambda k: star_count[k], reverse=True)
                sorted_counts=[star_count[i] for i in sorted_indices]
                sorted_repo=[star_repo[i] for i in sorted_indices]

                # Top 5 starred Repos
                top_repos=sorted_repo[:5]
                top_counts=sorted_counts[:5]

                # Plot the doughnut chart using Matplotlib
                fig, ax=plt.subplots(figsize=(10, 10))
                fig.patch.set_facecolor('none')  # Remove the white background

                wedges, texts, autotexts = ax.pie(
                                                    top_counts, 
                                                    startangle=90, 
                                                    wedgeprops={'edgecolor': 'black'},
                                                    autopct='%1.1f%%',  # Display percentage labels
                                                    pctdistance=0.75,  # Position the percentage labels
                                                    textprops={'fontsize': 10}  # Font size for labels
                                                )


                ax.pie(top_counts, startangle=90, wedgeprops={'edgecolor':'black'})
                # Add legend based on the labels
                ax.legend(top_repos, title='Repository', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

                # Draw a white circle at the center to create the doughnut shape
                center_circle = plt.Circle((0, 0), 0.50, color='black', fc='white')
                ax.add_artist(center_circle)

                ax.axis('equal')
                
                # Display the chart using Streamlit
                st.pyplot(fig)
            except:
                st.write("No values found")    

    with colb:

        if 'commits_per_repository' in user_record:
            try:

                st.markdown("<span style='color: blue;'>Commits Per Repo (Top-5)</span>", unsafe_allow_html=True)

                commits_per_repo=user_record['commits_per_repository']

                commit_repo=list(commits_per_repo.keys())
                commit_count=list(commits_per_repo.values())

                # Sort repo and commits by counts
                sorted_indices=sorted(range(len(commit_count)), key=lambda k: star_count[k], reverse=True)
                sorted_counts=[commit_count[i] for i in sorted_indices]
                sorted_repo=[commit_repo[i] for i in sorted_indices]

                # Top 5 starred Repos
                top_repos=sorted_repo[:5]
                top_counts=sorted_counts[:5]

                # Plot the doughnut chart using Matplotlib
                fig, ax=plt.subplots(figsize=(10, 10))
                fig.patch.set_facecolor('none')  # Remove the white background

                wedges, texts, autotexts = ax.pie(
                                                    top_counts, 
                                                    startangle=90, 
                                                    wedgeprops={'edgecolor': 'black'},
                                                    autopct='%1.1f%%',  # Display percentage labels
                                                    pctdistance=0.75,  # Position the percentage labels
                                                    textprops={'fontsize': 10}  # Font size for labels
                                                )



                ax.pie(top_counts, startangle=90, wedgeprops={'edgecolor':'black'})
                # Add legend based on the labels
                ax.legend(top_repos, title='Repository', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

                # Draw a white circle at the center to create the doughnut shape
                center_circle = plt.Circle((0, 0), 0.50, color='black', fc='white')
                ax.add_artist(center_circle)

                ax.axis('equal')
                
                # Display the chart using Streamlit
                st.pyplot(fig)
            except:
                st.write("No values found")
    with colc:
        if 'languages' in user_record:

            try:

                st.markdown("<span style='color: blue;'>Top 5 Language Worked in Bytes</span>", unsafe_allow_html=True)
                languages=user_record['languages']

                language_type=list(languages.keys())
                language_size=list(languages.values())

                # sort languages by size
                sorted_indices=sorted(range(len(language_size)), key=lambda k: language_size[k], reverse=True)
                sorted_language=[language_type[i] for i in sorted_indices]
                sorted_language_size=[language_size[i] for i in sorted_indices]

                # Top 5 - Language used
                top_language=sorted_language[:5]
                top_language_size=sorted_language_size[:5]

                # Plot the bar chart using Matplotlib
                fig, ax = plt.subplots(figsize=(10, 7))
                fig.patch.set_facecolor('none')  # Remove the white background
                ax.set_facecolor('none')

                
                bars=ax.bar(top_language, top_language_size, edgecolor='black')

                # Add labels at the top of each bar using bar_label
                ax.bar_label(bars, padding=3)
            
                ax.set_xlabel('Languages', fontsize=14, fontweight='bold')
                # ax.set_ylabel('Bytes of Language')
                ax.tick_params(axis='x', rotation=45)
                
                # Display the chart using Streamlit
                st.pyplot(fig)
            except:
                st.write("No values found")
if option=='Recommendation System':

    from recommendation import get_user_recommendation
   

    # Extract the list of usernames from the result_df Dataframe
    with open(r'C:\Users\Good Day\Desktop\Final Project\result_df.pkl', 'rb') as file:
        result_df=pickle.load(file)


    usernames=result_df['username'].tolist()
    # usernames = result_df['username'].to_pandas().tolist()


    user=st.selectbox('Select Username:', usernames)

    if user:
        # Label encode the username to fed to function
        with open(r'C:\Users\Good Day\Desktop\Final Project\user_encoder_new.pkl', 'rb') as file:
            user_label = pickle.load(file)

        username=user_label.transform([user])
        username=(username[0])
        # st.write(username)

        # unpickle the dictionary
        with open(r'C:\Users\Good Day\Desktop\Final Project\recommendation_final.pkl','rb') as file:
            loaded_dict=pickle.load(file)

        # Extract the items
        data = loaded_dict['data']
        csr_data= loaded_dict['csr_data']
        knn = loaded_dict['knn']
        result_df = loaded_dict['result_df']
        

        result= get_user_recommendation(username)
        
        st.markdown("<span style='color: green; font-size: 25px'>List of Recommended Users for the Selected User</span>", unsafe_allow_html=True)

        # Create headers for each column with custom color
        header_cols = st.columns([2, 2, 2, 5, 5])
        header_cols[0].markdown("<span style='color: blue;'>Username</span>", unsafe_allow_html=True)
        header_cols[1].markdown("<span style='color: blue;'>Public Repositories</span>", unsafe_allow_html=True)
        header_cols[2].markdown("<span style='color: blue;'>Total Commits</span>", unsafe_allow_html=True)
        header_cols[3].markdown("<span style='color: blue;'>Languages</span>", unsafe_allow_html=True)
        header_cols[4].markdown("<span style='color: blue;'>Repositories</span>", unsafe_allow_html=True)

        # Normalize function to scale values to 0-100 range
        def normalize(value, min_value, max_value):
            return int((value - min_value) / (max_value - min_value) * 100)

        # Find min and max values for normalization
        max_public_repos = result['Public_Repositories'].max()
        min_public_repos = result['Public_Repositories'].min()

        max_total_commits = result['Total_Commits'].max()
        min_total_commits = result['Total_Commits'].min()

        # Find min and max values for languages
        all_language_values = [value for lang_dict in result['Languages'] for value in lang_dict.values()]
        max_language_value = max(all_language_values)
        min_language_value = min(all_language_values)

        for index, row in result.iterrows():
            cols = st.columns([2, 2, 2, 5, 5])
            
            # Display the Username
            cols[0].write(row['Username'])
            
            # Normalize and Display Public Repositories with a progress bar
            public_repos_normalized = normalize(row['Public_Repositories'], min_public_repos, max_public_repos)
            cols[1].write(f"{row['Public_Repositories']} ")
            cols[1].progress(public_repos_normalized)
            
            # Normalize and Display Total Commits with a progress bar
            total_commits_normalized = normalize(row['Total_Commits'], min_total_commits, max_total_commits)
            cols[2].write(f"{row['Total_Commits']}")
            cols[2].progress(total_commits_normalized)
                      
            with cols[3].expander("See Languages"):
                # st.write(row['Languages'])
                cola, colb = st.columns(2)
                languages = row['Languages']
                for language, value in languages.items():
                    with cola:
                        st.write(f"{language}")
                    with colb:
                        st.write(f"{value}")
                       
                    
            
            # Display Repository
            with cols[4].expander("See Repositories"):
                st.write(row['Repositories'])
            

            # Add a line break between each iteration
            st.markdown("<hr>", unsafe_allow_html=True)

        

       