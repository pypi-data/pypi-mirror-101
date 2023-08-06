Amazon-Buy-Bot is a python library to buy product on amazon automatically using browser automation. 
It currently runs only on windows.

### Example 1
In this example we first import library, then we login with cookies, then we buy product using credit/debit cards.
```sh
from amazon_buy_bot import *
true=True;false=False
list_of_cookies=[
{
    "domain": ".amazon.in",
    "expirationDate": 1644925588.404523,
    "hostOnly": false,
    "httpOnly": false,
    "name": "i18n-prefs",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "INR",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
product_link="https://www.amazon.in/Boat-Airdopes-171-Functionality-Resistance/dp/B086WN6N4G/ref=sr_1_14_mod_primary_lightning_deal?crid=1YHOUOZCKZVNV&dchild=1&keywords=earbuds+wireless&qid=1613389628&sbo=Tc8eqSFhUl4VwMzbE4fw%2Fw%3D%3D&smid=A14CZOWI0VEHLG&sprefix=earb%2Caps%2C850&sr=8-14"
amazon.login_cookie(cookies=list_of_cookies)
amazon.buy(product_url=product_link)
amazon.select_payment_method(payment_method='Punjab National Bank Debit Card')
amazon.fill_cvv(cvv='123')
amazon.place_order()
```

### Example 2
In this example we first import library, then we login with cookies, then we buy product using net banking.
```sh
from amazon_buy_bot import *
true=True;false=False
list_of_cookies=[
{
    "domain": ".amazon.in",
    "expirationDate": 1644925588.404523,
    "hostOnly": false,
    "httpOnly": false,
    "name": "i18n-prefs",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "INR",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
product_link="https://www.amazon.in/Boat-Airdopes-171-Functionality-Resistance/dp/B086WN6N4G/ref=sr_1_14_mod_primary_lightning_deal?crid=1YHOUOZCKZVNV&dchild=1&keywords=earbuds+wireless&qid=1613389628&sbo=Tc8eqSFhUl4VwMzbE4fw%2Fw%3D%3D&smid=A14CZOWI0VEHLG&sprefix=earb%2Caps%2C850&sr=8-14"
amazon.login_cookie(cookies=list_of_cookies)
amazon.buy(product_url=product_link)
amazon.select_payment_method(payment_method='Net Banking')
amazon.select_bank(bank='Axis Bank')
amazon.place_order()
```

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which product will be bought. To buy first login will need to be done. Login can be done either with credentials or via cookies

Complete documentation for Amazon Automation available [here](https://amazon-api.datakund.com/en/latest/)


### Installation

```sh
pip install amazon-buy-bot
```

### Import
```sh
from amazon_buy_bot import *
```

### Login with credentials
```sh
amazon.login(password='place password here', email='place email here')
```

### Login with cookies
```sh
amazon.login_cookie(cookies=list_of_cookies)
```

### Click on Buy buttom
```sh
amazon.buy(product_url='product link')
```

### Select Payment Method
```sh
amazon.select_payment_method(payment_method='payment method')
```

### Fill Cvv
```sh
amazon.fill_cvv(cvv='')
```

### Select Bank
```sh
amazon.select_bank(bank='bank name')
```

### Place order
```sh
amazon.place_order()
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Cookies
To login with cookies [Edit this Cookie Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) can be added to browser. Please check [this](https://abhishek-chaudhary.medium.com/how-to-get-cookies-of-any-website-from-browser-22b3d6348ed2) link how to get cookies to login to your amazon.
### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

