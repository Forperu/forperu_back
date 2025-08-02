import openpyxl
import json
from .calculate import calculate_prices, find_price_by_name, parse_float, PriceType

def parse_excel(file, user_id):
  products = []
    
  try:
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active
    
    # Leer encabezados
    headers = [cell.value for cell in sheet[1]]
    header_map = {header: idx for idx, header in enumerate(headers) if header}
    
    # Validar encabezados requeridos
    required_headers = ["Codigo", "Nombre", "Precio(CF)", "Precio(SF)", "Precio(Caja)", "Costo"]
    for req in required_headers:
      if req not in header_map:
        raise ValueError(f"Falta el encabezado requerido: {req}")
    
    # Simulación de precios originales (similar al código Go)
    prices = [
      {"id": 1, "name": "price_1"},
      {"id": 2, "name": "price_2"},
      {"id": 3, "name": "price_3"},
      {"id": 4, "name": "price_4"},
      {"id": 5, "name": "price_5"},
      {"id": 6, "name": "price_6"},
      {"id": 7, "name": "price_7"},
      {"id": 8, "name": "price_8"},
      {"id": 9, "name": "price_9"},
      {"id": 10, "name": "price_10"},
      {"id": 11, "name": "price_11"},
      {"id": 12, "name": "price_12"},
      {"id": 13, "name": "price_13"},
      {"id": 14, "name": "price_14"},
      {"id": 15, "name": "price_15"},
      {"id": 16, "name": "price_16"},
      {"id": 17, "name": "price_17"},
      {"id": 18, "name": "price_18"},
      {"id": 19, "name": "price_19"},
      {"id": 20, "name": "price_20"},
    ]
    
    # Iterar sobre las filas
    for row in sheet.iter_rows(min_row=2, values_only=True):
      if not any(row):  # Saltar filas vacías
        continue
            
      cost = parse_float(row[header_map["Costo"]])
        
      # Calcular precios
      calculated_cf = calculate_prices(prices, PriceType.CF, cost)
      calculated_sf = calculate_prices(prices, PriceType.SF, cost)
      calculated_box = calculate_prices(prices, PriceType.BOX, cost)
        
      # Obtener precios destacados
      def get_featured_price(price_type, price_key, calculated_prices):
        try:
          price_number = int(row[header_map[price_key]])
          price_name = f"price_{price_number}"
          found_price, exists = find_price_by_name(calculated_prices, price_name)
          return found_price['price'] if exists else 0.0
        except (ValueError, TypeError):
          return 0.0
        
      price_cf = get_featured_price(PriceType.CF, "Precio(CF)", calculated_cf)
      price_sf = get_featured_price(PriceType.SF, "Precio(SF)", calculated_sf)
      price_box = get_featured_price(PriceType.BOX, "Precio(Caja)", calculated_box)
        
        # Crear producto
      product = {
        "sku": row[header_map["Codigo"]] if row[header_map["Codigo"]] else None,
        "name": row[header_map["Nombre"]],
        "prices_cf": calculated_cf,
        "prices_sf": calculated_sf,
        "prices_box": calculated_box,
        "featured_pcf": price_cf if row[header_map["Precio(CF)"]] else None,
        "featured_psf": price_sf if row[header_map["Precio(SF)"]] else None,
        "featured_pbox": price_box if row[header_map["Precio(Caja)"]] else None,
        "cost": cost,
        "created_by": user_id
      }
        
      products.append(product)
            
  except Exception as e:
    raise ValueError(f"Error procesando archivo Excel: {str(e)}")
    
  return products