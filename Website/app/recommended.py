from app.models import Comment
import requests
import json

def get_recommendation(self,request):
    url_1 = 'http://127.0.0.1:8000/popularity'
    url_2 = 'http://127.0.0.1:8000/user-recommendation'
    user = request.user
    if request.user.is_authenticated:
        commentData = Comment.objects.filter(user=user)
        details_arr = []
        for a in commentData:
            new_dict={'productId': a.product.title,'userId':'A061','Rating':a.rating}
            details_arr.append(new_dict)
            #print(details_arr)
        no_of_products = len(details_arr)
        #print(no_of_products)
        if no_of_products>4:
            user_rating_data = json.dumps(details_arr)
            response1 = requests.post(url_2,data = user_rating_data)
            user_recommendation = response1.json()
            product_names = []
            for key, value in user_recommendation["shoes"].items():
                product_names.append(value)
            return product_names
            # return user_recommendation
            #print(user_recommendation)
        else:
            response = requests.get(url_1)
            popular_recommendation = response.json()
            product_names = list(popular_recommendation['Rating'].keys())
            return product_names
    else:
        response = requests.get(url_1)
        popular_recommendation = response.json()
        product_names = list(popular_recommendation['Rating'].keys())
        return product_names
        #print(popular_recommendation)
        # return popular_recommendation