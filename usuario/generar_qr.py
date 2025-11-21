# generar_qr.py
import qrcode
import uuid

token = uuid.uuid4()
url = f"https://tusitio.com/turno/generar/{token}/"

img = qrcode.make(url)
img.save("qr_dinamico.png")
print("QR generado correctamente")
