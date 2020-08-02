from models.item import Item
from models.alert import Alert


#url = "https://www.johnlewis.com/2018-apple-ipad-pro-12-9-inch-a12x-bionic-ios-wi-fi-cellular-1tb/p3834587"
url2 = "https://www.johnlewis.com/house-by-john-lewis-bonn-child-compliant-upholstered-bed-frame-single-saga-grey/p4395568"
url3 = "https://www.johnlewis.com/john-lewis-partners-warner-faux-leather-office-chair/p1891692"
url4 = "https://www.johnlewis.com/bosch-wan28201gb-freestanding-washing-machine-8kg-load-a-energy-rating-1400rpm-spin-white/p3208218"
url5 = "https://www.johnlewis.com/sony-bravia-kd55ag8-2019-oled-hdr-4k-ultra-hd-smart-android-tv-55-inch-with-freeview-hd-youview-acoustic-surface-audio-black/p4123133"
tag_name = "p"
tag_name2 = "span"
query = {"class": "price price--large"}
query2 = {"class" : "ProductPrice__item--1p_iL"}
#ipad = Item("iPad", url, tag_name, query)
bed = Item("Bed", url2, tag_name, query)
chair = Item("Chair", url3, tag_name, query)
washing_machine = Item("Bosch Washing Machine", url4, tag_name2, query2)
sonyTV = Item("Sony TV", url5, tag_name, query)
#print(f"PRICE of {ipad.item_name} = {ipad.load_price()}")
print(f"PRICE of {bed.item_name} = {bed.load_price()}")
print(f"PRICE of {chair.item_name} = {chair.load_price()}")
print(f"PRICE of {washing_machine.item_name} = {washing_machine.load_price()}")
print(f"PRICE of {sonyTV.item_name} = {sonyTV.load_price()}")

# ipad.save_to_mongodb()
# bed.save_to_mongodb()
# chair.save_to_mongodb()

items_present = Item.all()

#genre = ("Python","C","C++","Java")
print("Prices of Items available on MongoDB are:")
for x in items_present:
   print (f"PRICE of {x.item_name} = {x.load_price()}")

#alert_ipad = Alert("bfdcc40e66744bae985d767899fb30ff", 2000)
alert_bed = Alert("b3f3bdf935a64eb0b362e9fc2d3685ba", 200)
alert_chair = Alert("195d394b528944c2b1d22f4327de7054", 175)
alert_washmachine = Alert("75cd56537bf44763af44917ad759e910", 500)
alert_sonyTv = Alert("edbf0fc0b64a4bfbaea82436acf0e369", 1500)

# alert_ipad.save_to_mongo()
# alert_bed.save_to_mongo()
# alert_chair.save_to_mongo()
#alert_washmachine.save_to_mongo()
#alert_sonyTv.save_to_mongo()



"""
app = Flask(__name__)

if __name__ == '__main__':
    app.run()
"""
