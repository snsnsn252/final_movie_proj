

import requests

def get_movie_data():

    move_list = []
    for i in range(200):
        if i > 0:
            url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={}".format(i)
            print(url)

            headers = {"accept": "application/json", 
                       "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZWUyMWQ4N2QzZjVhNmJhZWY3YTQ5OWU2MTFkYjZhNCIsInN1YiI6IjY1NWFhMjhjNTM4NjZlMDExYzA5Y2Q3NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Oa4VJpx6NI7zowz_Kucf9N_zc_zhwBg2Tq-PeVPx-4k"}

            response = requests.get(url, headers=headers)

            #print(response.text)

            page_list = response.json()['results']
            for j in range(len(page_list)):

                move_list.append(page_list[j])

    return move_list


'''
import requests

url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZWUyMWQ4N2QzZjVhNmJhZWY3YTQ5OWU2MTFkYjZhNCIsInN1YiI6IjY1NWFhMjhjNTM4NjZlMDExYzA5Y2Q3NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Oa4VJpx6NI7zowz_Kucf9N_zc_zhwBg2Tq-PeVPx-4k"
}

response = requests.get(url, headers=headers)

print(response.text)
'''