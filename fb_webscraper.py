import pymongo
import datetime
import yaml
from facebook_scraper import get_posts

class FBWebScraper():

    def __init__(self, my_email, my_password, my_account_name):
        self.my_email = my_email
        self.my_password = my_password
        self.my_account_name = my_account_name
        # Initialize MongoDB
        self.mc = pymongo.MongoClient()
        self.db = self.mc['my-facebook-webscrape']
        self.fb_statuses = self.db['fb-statuses']

        person_dict = self.fb_statuses.find_one({'friends_dict': {'$exists': True}})
        if person_dict == None:
            self.friends_dict = {}
        else:
            self.friends_dict = person_dict['friends_dict']

    

    def scrape_friends_statuses(self):
        # Web scrape each friend in friends dictionary, add statuses to mongoDB.
        # Data structure of each entry:
        #   {'name': STRING = name,
        #   'url': STRING = profile url,
        #   'datetime': DATETIME = current time,
        #   'statuses': DICT = {key=time of status post, value=status},
        #   'html': STRING = html of page,}


        
        posts = get_posts(self.my_account_name, pages=2, credentials=[self.my_email, self.my_password])

        for post in posts:
            # post_time_element = post.find_element_by_css_selector('abbr')
            post_time = post['time']
            post_context = post['text']
            post_text = post['post_text']

            # Add entry to MongoDB
            self.fb_statuses.insert_one({
                    'context': post_context,
                    'post_text': post_text,
                    'post_time': post_time
                    })
            print("Finished creating a status entry!")

if __name__ == '__main__':
    my_account_name = input("Enter your account name: ")
    my_email = input("Enter your email: ")
    my_password =  input("Enter your password: ")

FBWS = FBWebScraper(
    my_email=my_email,
    my_password=my_password,
    my_account_name=my_account_name
)

FBWS.scrape_friends_statuses()
