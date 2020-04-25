# hobimakanbanyuwangi
Web that makes you experience culinary activities easily in Banyuwangi.
The idea started when I was in Banyuwangi city for the first time and was trying to do culinary activities. 
1. Most of the restaurants or cafe's were not available on Google maps, especially popular street food.
2. There's a lot of instagram accounts about Banyuwangi culinary on Instagram but they don't provide you a google maps point, only an address. So most of their followers also faced difficulty in finding the location just like me who moved to the city recently.

So, I did a small research to find the best & popular Banyuwangi culinary instagram account and found [@hobimakan.banyuwangi](https://www.instagram.com/hobimakan.banyuwangi/). I contacted the admin to have a cup of coffee and we ended up with a collaboration. I made [@hobimakan.banyuwangi](https://hobimakanbanyuwangi) website with 3 solutions: Find, Get the maps, and see what popular based by ratings and likes on Instagram. And I also came up with a simple web solution since the admin never had any experience in managing a website:

- The Admin only need to post on Instagram, open [this url](https://hobimakanbanyuwangi.com/andreyongz) and click update button and the scraper will run and replace the following format and save it into database automatically, no need to reinput the data on the website which is a waste of time:

```sh
def replace_text(capt):
    capt = capt.replace("📎", "Address:")
    capt = capt.replace("⌚", "Hours:")
    capt = capt.replace("💸", "PriceInfo:")
    capt = capt.replace("🌟", "Ratings:")
    capt = capt.replace("📣", "InstagramAccount:")
    capt = capt.replace("☎️", "Telephone:")
    capt = capt.replace("📞", "Telephone:")
    capt = capt.replace("📌", "LatLang:")
    return capt

```


### What you can learn from here
[1. How to scrape instagram feed](https://github.com/jimmyromanticdevil/hobimakanbanyuwangi/blob/master/hobimakanbanyuwangi/utils/scrapper.py#L11) using [instagram-scraper](https://github.com/rarcega/instagram-scraper)

[2. Extract and cleaning the data and save it into database over Django ORM](https://github.com/jimmyromanticdevil/hobimakanbanyuwangi/blob/master/hobimakanbanyuwangi/utils/instagram-extraction.py#L72)

[3. Async background processing without Celery](https://github.com/jimmyromanticdevil/hobimakanbanyuwangi/blob/master/main/views.py#L306) using [Django After Responses](https://github.com/defrex/django-after-response)

[4. Simple Search Query Strings in Django](https://github.com/jimmyromanticdevil/hobimakanbanyuwangi/blob/master/main/views.py#L55) 


## Base Requirements

- Django `pip install Django`
- Django after responses `pip install django-after-response`
- Instagram-scraper `pip install instagram-scraper`


## Installation

```sh

git clone https://github.com/jimmyromanticdevil/hobimakanbanyuwangi/
cd hobimakanbanyuwangi
pip install -r requirements.txt
python manage.py runserver

Access url -> http://localhost:8000/andreyongz/ to start the scraper.
Wait for 5 minutes then you can open http://localhost:8000/ to see the result 

```

