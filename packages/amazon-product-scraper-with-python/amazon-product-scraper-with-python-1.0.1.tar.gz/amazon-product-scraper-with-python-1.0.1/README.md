Amazon-Product-Scraper-With-Python is a python library to get product information on amazon automatically using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we will fetch the product info.
```sh
from amazon_product_scraper_with_python import *
product_link="https://www.amazon.in/OnePlus-Bullets-Wireless-Bluetooth-Earphones/dp/B086CSGV2N/ref=sr_1_16?crid=1YHOUOZCKZVNV&dchild=1&keywords=earbuds+wireless&qid=1613389628&sprefix=earb%2Caps%2C850&sr=8-16"
response=amazon.product_info(product_url=product_link)
data=response['body']
#data={"Review Terms": "sound quality \t\t battery life", "NoOfRatings": "5432", "ReviewsLink": "https://www.amazon.in/OnePlus-Bullets-Wireless-Bluetooth-Earphones/product-reviews/B086CSGV2N/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews", "Price": "935", "Ratings": "4.1", "Description": "Charge for 10 minutes, enjoy for 10 hours on your On....", "Features": "Features", "Offers": "Cashback (2): 5% back with Amazon Pay ICICI Bank Credit card for Prime-members. 3% back for everybody else See AllCashback (2): 5% back with Amazon Pay ICICI Bank Credit card for Prime-members. 3% back for", "Title": "OnePlus Bullets Wireless Z in-Ear Bluetooth Earphones with Mic (Black)"}
```

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which product link will be opened.

Complete documentation for Amazon Automation available [here](https://amazon-api.datakund.com/en/latest/)

### Installation

```sh
pip install amazon-product-scraper-with-python
```

### Import
```sh
from amazon_product_scraper_with_python import *
```

### Login with credentials
```sh
amazon.login(password='place password here', email='place email here')
```

### Login with cookies
```sh
amazon.login_cookie(cookies=list_of_cookies)
```

### Get product info
```sh
response=amazon.product_info(product_url='product link')
data=response['body']
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

