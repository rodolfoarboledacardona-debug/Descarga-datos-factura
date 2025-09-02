import fitz  # PyMuPDF
import re

def extract_data_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    results = []

    for page in doc:
        text = page.get_text()
        data = {
            "Número de Factura": extract_field(r"Factura Nro\.?\s*(\d+)", text),
            "Fecha de Expedición": extract_field(r"Fecha Expedición:?\s*(\d{1,2} de \w+ de \d{4})", text),
            "Propietario": extract_field(r"Propietario\s*(.*?)\s*Ficha Catastral", text),
            "Dirección del Predio": extract_field(r"Dirección del Predio\s*(.*?)\s*Dirección de Cobro", text),
            "Ficha Catastral": extract_field(r"Ficha Catastral\s*([\d\s]+)", text),
            "Valor a Pagar al Trimestre": extract_field(r"VALOR A PAGAR AL TRIMESTRE\s*\$[\s]*([\d,.]+)", text),
            "Valor Total a Pagar": extract_field(r"TOTAL A PAGAR SIN DESCUENTO\s*\$[\s]*([\d,.]+)", text),
            "Fecha Límite de Pago": extract_field(r"PAGUESE HASTA\s*(\d{1,2} de \w+ de \d{4})", text),
        }
        results.append(data)
    return results

def extract_field(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""
