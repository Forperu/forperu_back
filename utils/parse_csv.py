import csv
from .calculate import parse_float

def parse_csv(file):
  products = []

  try:
    # Leer el archivo CSV
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
        
    # Leer encabezados
    headers = next(reader)
    header_map = {header: idx for idx, header in enumerate(headers) if header}
        
    # Validar encabezados requeridos
    required_headers = ["Nombre", "Precio", "Costo", "Cantidad"]
    for req in required_headers:
      if req not in header_map:
        raise ValueError(f"Falta el encabezado requerido: {req}")
        
    # Iterar sobre las filas
    for row in reader:
      if not any(row):  # Saltar filas vacías
        continue

      # Crear producto
      product = {
        "sku": row[header_map.get("Codigo", -1)] if header_map.get("Codigo") and row[header_map["Codigo"]] else None,
        "name": row[header_map["Nombre"]],
        "featured_pcf": parse_float(row[header_map.get("Precio(CF)", -1)]) if header_map.get("Precio(CF)") else None,
        "featured_psf": parse_float(row[header_map.get("Precio(SF)", -1)]) if header_map.get("Precio(SF)") else None,
        "featured_pbox": parse_float(row[header_map.get("Precio(Caja)", -1)]) if header_map.get("Precio(Caja)") else None,
        "cost": parse_float(row[header_map["Costo"]])
      }
            
      products.append(product)
            
  except Exception as e:
    raise ValueError(f"Error procesando archivo CSV: {str(e)}")
    
  return products