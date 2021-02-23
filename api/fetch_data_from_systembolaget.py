import requests
import csv

def fetch(page):
  url = "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/productsearch/search?size=30&page=" + str(page) + "&categoryLevel1=Vin"

  payload = {}
  headers = {
    'Ocp-Apim-Subscription-Key': '874f1ddde97d43f79d8a1b161a77ad31'
  }

  response = requests.request("GET", url, headers=headers, data = payload)
  if 'error' in response.json():
    return (None, False)
  else:
    return (response.json()['products'], True)

csvRow = [
  "nameBold", "nameThin", "producer", "year", "alcoholPercentage", "volume", "price", "country", "region", "district", "type", "categoryTaste",
  "usage", "taste", "tasteBitter", "tasteSweetness", "tasteFruitAcid", "tasteBody", "tasteRoughness", "url", "imageURL", "grapes"
]
with open('systembolaget_raw.csv', 'w', newline='') as file:
  writer = csv.writer(file, dialect='excel')
  writer.writerow(csvRow)

  pageNumber = 1
  (products, hasMore) = fetch(pageNumber)

  while(hasMore == True):
    for product in products:
      newProductRow = [
        product['productNameBold'],
        product['productNameThin'],
        product['producerName'],
        product['vintage'],
        product['alcoholPercentage'],
        product['volume'],
        product['price'],
        product['country'],
        product['originLevel1'],
        product['originLevel2'],
        product['categoryLevel2'],
        product['categoryLevel3'],
        product['usage'],
        product['taste'],
        str((product['tasteClockBitter'] / 12) * 100) + "%",
        str((product['tasteClockSweetness'] / 12) * 100) + "%",
        str((product['tasteClockFruitacid'] / 12) * 100) + "%",
        str((product['tasteClockBody'] / 12) * 100) + "%",
        str((product['tasteClockRoughness'] / 12) * 100) + "%",
        'https://www.systembolaget.se/produkt/' + product['categoryLevel1'].lower() + '/' + product['productNameBold'].lower().replace(r' ', '-') + '-' + str(product['productNumber'])
      ]

      image = ""
      if len(product['images']) > 0:
        image = product['images'][0]['imageUrl']
      newProductRow.append(image)

      grapesList = []
      grapes = ""
      for i in range(len(product['grapes'])):
        seperator = "---" if i != 0 else ""
        grapes += seperator + product['grapes'][i]
      newProductRow.append(grapes)

      writer.writerow(newProductRow)

    pageNumber += 1
    (products, hasMore) = fetch(pageNumber)