import pandas as pd
import numpy as np
import warnings; warnings.filterwarnings('ignore')

import os
os.chdir('C:/Users/User/OneDrive/바탕 화면/archive2')

#데이터 전처리
movies = pd.read_csv('tmdb_5000_movies.csv')
print(movies.shape)
movies.head()

#genres 열이 이상하다 -> str 확인 
movies['genres'][0]
type(movies['genres'][0])

#literal_eval : str -> list 형태로 바꿔준다

from ast import literal_eval
movies['genres'] = movies['genres'].apply(literal_eval)
movies['keywords'] = movies['keywords'].apply(literal_eval)

movies['genres'][0]

#list 내 여러 개 딕셔너리의 name키에 해당하는 값들을 리스트로 변환
movies['genres'] = movies['genres'].apply(lambda x : [y['name'] for y in x])

movies['keywords'] = movies['keywords'].apply(lambda x : [y['name'] for y in x])

movies[['genres', 'keywords']][:1]

#장르 유사도 기반 영화 추천 시스템

#장르 CBF 추천 : 장르를 피처 벡터화한 후 행렬 데이터 값을 코사인 유사도로 계산하기

#<프로세스>
#1. 장르피처 벡터화 : 문자열로 변환된 genres 칼럼을 Count기반으로 피처 벡터화 변환
#2. 코사인 유사도 계산 : genres 문자열을 피쳐 벡터화한 행렬로 변환한 데이터 세트를 코사인 유사도로 비교
#3. 평점으로 계산 : 장르 유사도가 높은 영화 중 평점이 높은 순으로 영화 추천

#CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#참고 : CountVectorizer에 대하여
#1. 문서를 토큰 리스트로 변환한다
#2. 각 문서에서 토큰의 출현 빈도를 센다
#3. 각 문서로 BOW(Bag of Words) 인코딩 벡터로 변환한다.

#CountVectorizer를 적용하기 위해 공백문자로 word 단위가 구분되는 문자열로 변환

movies['genres_literal'] = movies['genres'].apply(lambda x : (' ').join(x))
movies['genres_literal']

#CountVectorizer로 학습시켰더니 4803개 영화에 대한 276개 장르의 '장르 매트릭스'가 생성되었따.
count_vect = CountVectorizer(min_df = 0, ngram_range=(1,2)) #min_df : 단어장에 들어갈 최소빈도)

genre_mat = count_vect.fit_transform(movies['genres_literal'])
genre_mat.shape


#코사인 유사도 이용해서 영화별 유사도 계산

#코사인 유사도에 의해 4803개 영화 각각 유사한 영화들이 계산됨
from sklearn.metrics.pairwise import cosine_similarity
genre_sim = cosine_similarity(genre_mat, genre_mat)
genre_sim.shape
genre_sim[:5]

#자료를 정렬하는 것이 아니라 순서만 알고 싶다면 argsort
#유사도가 높은 영화를 앞에서부터 순서대로 보여줌
# 0번째 영화의 경우 유사도 순서 : 0번, 3494번, 813번 순서
genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1] #전체를 -1칸 간격으로
genre_sim_sorted_ind[:1]  #특정 영화와 유사도가 높은 순서대로 인덱스 번호를 보여줌

#추천 ver1. 장르 코사인 유사도에 의해 영화를 추천하는 함수
def find_sime_movie_ver1(df, sorted_ind, title_name, top_n=10):
    #인자로 입력된 movies_df DataFrame에서 'title'컬럼이 입력된 title_name 값인 DataFrame추출
    title_movie = df[df['title'] ==title_name]

    #title_named를 가진 DataFrame의 index 객체를 ndarray로 반환하고
    #sorted_ind 인자로 입력된 genre_sim_sorted_ind 객체에서 유사도 순으로 top_n개의 index 추출
    title_index = title_movie.index.values
    similar_indexes = sorted_ind[title_index, :(top_n)]

    #추출된 top_n index를 출력. top_n index는 2차원 데이터임.
    #dataframe에서 index로 사용하기 위해 1차원 array로 변경
    print(similar_indexes)
    #2차원 데이터를 1차원으로 변환
    similar_indexes = similar_indexes.reshape(-1)

    return df.iloc[similar_indexes]

#영화 Godfather와 장르가 유사한 영화 10개 추천
similar_movies = find_sime_movie_ver1(movies, genre_sim_sorted_ind, 'The Godfather',10)
similar_movies[['title', 'vote_average', 'genres', 'vote_count']]

#문제 -> 평가횟수가 현저히 적은 영화들이 추천되는 경우 : low quality 추천문제/ 평가횟수를 반영한 추천 시스템이 필요


#상위 60%에 해당하는 vote_count를 최소 투표 횟수인 m으로 지정
C = movies['vote_average'].mean()
m = movies['vote_count'].quantile(0.6)

#C : 전체 영화에 대한 평균평점 = 약 6점
# m : 평점을 부여하기 위한 최소 투표 횟수 = 370회(상위 60% 수준)
print('C', round(C,3), 'm', round(m,3))


#가중 평점을 계산하는 함수
def weighted_vote_average(record):
    v = record['vote_count']
    R = record['vote_average']

    return ((v/(v+m)) *R) + ( (m/(m+v))*C)

#기존 데이터에 가중평점 칼럼 추가
movies['weighted_vote'] = movies.apply(weighted_vote_average, axis=1)

movies.head()


#추천 ver2. 먼저 장르 유사성 높은 영화 20개 선정 후, 가중평점순 10개 선정

def find_sim_movie_ver2(df, sorted_ind, title_name, top_n = 10):
    title_movie = df[df['title'] == title_name]
    title_index = title_movie.index.values

    #top_n의 2배에 해당하는 장르 유사성이 높은 index 추출
    similar_indexes = sorted_ind[title_index, :(top_n*2)]
    similar_indexes = similar_indexes.reshape(-1)

    #기준 영화 index는 제외
    similar_indexes = similar_indexes[similar_indexes != title_index]

    #top_n의 2배에 해당하는 후보군에서 weighted_vote 높은 순으로 top_n만큼 추출
    return df.iloc[similar_indexes].sort_values('weighted_vote', ascending=False)[:top_n]

similar_movies = find_sim_movie_ver2(movies, genre_sim_sorted_ind, 'The Godfather', 10)
similar_movies[['title', 'vote_average', 'genres', 'vote_count']]

