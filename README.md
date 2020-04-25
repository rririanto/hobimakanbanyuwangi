# hobimakanbanyuwangi
Web that make you easily do culinary activities in Banyuwangi.
The idea started when I was in Banyuwangi city for the first time and was trying to do culinary activities. 
1. Most of restaurant or cafe not available in Google maps especially popular street food.
2. There's alot instagram account about Banyuwangi culinary on Instagram but they don't provide you a google maps point, only an address. So most of their followers also face difficult situation to find the location as well as me who just lived in the city.

So, I did small research to find best & popular instagram Banyuwangi culinary account and found [@hobimakan.banyuwangi](https://www.instagram.com/hobimakan.banyuwangi/). I contact the admin to have a cup of coffee and we end up with collaboration. I make [@hobimakan.banyuwangi](https://hobimakanbanyuwangi) website with 3 solution: Find, Get the maps, and see what popular based by ratings and like on Instagram. And I also come up with simple web solution since the admin never had an experience to manage a website:

- Admin just need to post on Instagram, open [this url](https://hobimakanbanyuwangi.com/andreyongz) and click update button and the scraper will run and replace the following format and save it into database automatically, no need to reinput the data on the website which is waste a time:

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

