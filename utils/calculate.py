import json
from enum import Enum

class PriceType(Enum):
  CF = "CF"
  SF = "SF"
  BOX = "BOX"

# Margenes de precio (similar al PriceMargins en Go)
PRICE_MARGINS = {
  "CF": {
    "price_1": 1.01,
    "price_2": 1.02,
    "price_3": 1.03,
    "price_4": 1.04,
    "price_5": 1.05,
    "price_6": 1.06,
    "price_7": 1.07,
    "price_8": 1.08,
    "price_9": 1.09,
    "price_10": 1.10,
    "price_11": 1.11,
    "price_12": 1.12,
    "price_13": 1.13,
    "price_14": 1.14,
    "price_15": 1.15,
    "price_16": 1.16,
    "price_17": 1.17,
    "price_18": 1.18,
    "price_19": 1.19,
    "price_20": 1.2
  },
  "SF": {
    "price_1": 1.01,
    "price_2": 1.02,
    "price_3": 1.03,
    "price_4": 1.04,
    "price_5": 1.05,
    "price_6": 1.06,
    "price_7": 1.07,
    "price_8": 1.08,
    "price_9": 1.09,
    "price_10": 1.10,
    "price_11": 1.11,
    "price_12": 1.12,
    "price_13": 1.13,
    "price_14": 1.14,
    "price_15": 1.15,
    "price_16": 1.16,
    "price_17": 1.17,
    "price_18": 1.18,
    "price_19": 1.19,
    "price_20": 1.2
  },
  "BOX": {
    "price_1": 1.01,
    "price_2": 1.02,
    "price_3": 1.03,
    "price_4": 1.04,
    "price_5": 1.05,
    "price_6": 1.06,
    "price_7": 1.07,
    "price_8": 1.08,
    "price_9": 1.09,
    "price_10": 1.10,
    "price_11": 1.11,
    "price_12": 1.12,
    "price_13": 1.13,
    "price_14": 1.14,
    "price_15": 1.15,
    "price_16": 1.16,
    "price_17": 1.17,
    "price_18": 1.18,
    "price_19": 1.19,
    "price_20": 1.2
  }
}

def calculate_prices(prices, price_type, cost):
  result = []
  
  try:
    margin_type = PriceType(price_type).value
  except ValueError:
    return result
  
  for p in prices:
    margin = PRICE_MARGINS[margin_type].get(p['name'], 1.01)  # Margen por defecto
    
    if price_type == PriceType.CF:
      calculated_price = (((cost / 1.18) * 1.06 * margin) * 1.18)
    else:
      calculated_price = cost * margin
    
    result.append({
      'id': p['id'],
      'name': p['name'],
      'price': calculated_price
    })
  
  return result

def find_price_by_name(prices, name):
  for price in prices:
    if price['name'] == name:
      return price, True
  return None, False

def parse_float(value):
  try:
    return float(value)
  except (ValueError, TypeError):
    return 0.0