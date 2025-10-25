#Current Project to-do list:
#1. Make it so that you can click on any movie in the results and it will take you to a webpage that gives you more information about that movie
#2. Make 

from flask import Flask, request, render_template, redirect, url_for, jsonify
from markupsafe import escape
import pandas as pd

#Creation of app taking template from the templates folder
#Template is called template_1.html
MovieRecomender = Flask(__name__,template_folder='templates')

#Creating, cleaning, and sorting dataframe
df=pd.read_csv('imdblist.csv')
df_clean=df.drop(['Meta_score','Gross','Certificate'],axis=1)
df_clean['Released_Year'].unique()
df_clean=df_clean[df_clean.Released_Year!='PG']
df_split = df_clean['Genre'].str.split(',',expand=True)
df_clean=pd.concat([df_clean,df_split],axis=1)
df_clean.rename(columns={df_clean.columns[13]:'Genre1'},inplace=True)
df_clean.rename(columns={df_clean.columns[14]:'Genre2'},inplace=True)
df_clean.rename(columns={df_clean.columns[15]:'Genre3'},inplace=True)

@MovieRecomender.route('/suggest') #URL endpoint in flask app
def suggest(): 
    q=request.args.get('q','').strip().lower()
    field=request.args.get('field','').strip().lower()
    if not q or field not in {'director','actor','genre'}:
        return jsonify([])
    max_results=10
    if field == 'director':
        source = df_clean['Director'].dropna().astype(str).str.strip().str.lower().unique()
    elif field == 'actor':
        actor_cols = ['Star1', 'Star2', 'Star3', 'Star4']
        source = pd.Series(pd.concat([df_clean[col].dropna().astype(str).str.strip() for col in actor_cols])).str.lower().unique()
    else:
        source = pd.Series(df_clean['Genre'].dropna().astype(str).str.split(',').explode()).str.strip().str.lower().unique()
    matches=[item for item in source if q in item]
    return jsonify([matches[:max_results]])

@MovieRecomender.route('/', methods=['GET','POST'])
def root():
    return redirect(url_for('Movie_Recomender'))

@MovieRecomender.route('/recomendation', methods=['GET','POST'])
def Movie_Recomender():
    results=[]
    if request.method =='POST':

        director=request.form['director'].strip().lower()
        genre=request.form['genre'].strip().lower()
        ao1=request.form['ao1'].lower()
        ao2=request.form['ao2'].lower()
        Actor=request.form['Actor'].strip().lower()
        count=0
        if director != '-1':
            director_data=[]
            for i in range(len(df_clean)):
                if df_clean.iloc[i].Director.lower() == director:
                    director_d={'Title':df_clean.iloc[i].Series_Title,
                    'IMDB rating':df_clean.iloc[i].IMDB_Rating,
                    'Overview':df_clean.iloc[i].Overview,
                    'Genre':df_clean.iloc[i].Genre,
                    'Star1':df_clean.iloc[i].Star1,
                    'Star2':df_clean.iloc[i].Star2,
                    'Star3':df_clean.iloc[i].Star3,
                    'Star4':df_clean.iloc[i].Star4}
                    director_data.append(director_d)
            df_new=pd.DataFrame(director_data)
        else:
            df_new=df_clean[['Series_Title','IMDB_Rating','Overview','Genre','Star1','Star2','Star3','Star4']].copy()
            df_new.rename(columns={df_new.columns[0]:'Title'},inplace=True)
            df_new.rename(columns={df_new.columns[1]:'IMDB rating'},inplace=True)
        if genre != '-1':
            if ao1 == 'and':
                while count < len(df_new):
                    if genre not in df_new.iloc[count].Genre.lower():
                        df_new=df_new.drop(df_new.index[count])
                        count=count-1
                    count=count+1
            else:
                genre_data=[]
                for j in range(len(df_clean)):
                    if genre in df_clean.iloc[j].Genre.lower():
                        genre_d={'Title':df_clean.iloc[j].Series_Title,
                        'IMDB rating':df_clean.iloc[j].IMDB_Rating,
                        'Overview':df_clean.iloc[j].Overview,
                        'Genre':df_clean.iloc[j].Genre,
                        'Star1':df_clean.iloc[j].Star1,
                        'Star2':df_clean.iloc[j].Star2,
                        'Star3':df_clean.iloc[j].Star3,
                        'Star4':df_clean.iloc[j].Star4}
                        genre_data.append(genre_d)
                df_with_genre = pd.DataFrame(genre_data)
                df_new=pd.concat([df_new,df_with_genre],ignore_index=True)
                df_new=df_new.drop_duplicates()
        count = 0
        if Actor != '-1':
            if ao2=='and':
                while count < len(df_new):
                    if (Actor != df_new.iloc[count].Star1.lower())and(Actor != df_new.iloc[count].Star2.lower())and(Actor != df_new.iloc[count].Star3.lower())and(Actor != df_new.iloc[count].Star4.lower()):
                        df_new=df_new.drop(df_new.index[count])
                        count=count-1
                    count=count+1
            else:
                actor_data=[]
                for k in range(len(df_clean)):
                    if (Actor == df_clean.iloc[k].Star1.lower())or(Actor == df_clean.iloc[k].Star2.lower())or(Actor == df_clean.iloc[k].Star3.lower())or(Actor == df_clean.iloc[k].Star4.lower()):
                        actor_d={'Title':df_clean.iloc[k].Series_Title,
                        'IMDB rating':df_clean.iloc[k].IMDB_Rating,
                        'Overview':df_clean.iloc[k].Overview,
                        'Genre':df_clean.iloc[k].Genre,
                        'Star1':df_clean.iloc[k].Star1,
                        'Star2':df_clean.iloc[k].Star2,
                        'Star3':df_clean.iloc[k].Star3,
                        'Star4':df_clean.iloc[k].Star4}
                        actor_data.append(actor_d)
                df_with_actor=pd.DataFrame(actor_data)
                df_new=pd.concat([df_new,df_with_actor],ignore_index=True)
                df_new=df_new.drop_duplicates()
        results=df_new['Title'].tolist()
    return render_template('template_1.html',results=results)

if __name__ == '__main__':
    MovieRecomender.run(debug=True,use_reloader=False)