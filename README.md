# 🛍️ Alkosto Alert Price

Un sistema automatizado para hacer seguimiento a la evolución de precios de productos tecnológicos en el sitio web de **Alkosto** (Colombia), con alertas vía Telegram y una interfaz web con Streamlit.

---

## 🔧 ¿Qué hace este proyecto?

✅ Hace scraping de precios de productos a partir de una lista de códigos GTIN (EAN13).  
✅ Almacena el histórico de precios en un archivo `productos.csv` y `productos.json`.  
✅ Envía una **alerta por Telegram** si el precio de algún producto baja.  
✅ Genera una **app interactiva con Streamlit** para visualizar gráficas y comparar precios.  
✅ Está diseñado para ejecutarse automáticamente dos veces por semana (martes y viernes) usando `cron`.

---

## 📁 Estructura del proyecto

scraping_alkosto/
├── app_alkosto.py # App web con Streamlit
├── alkosto_gtin_v4.py # Script de scraping + alertas
├── gtins.csv # Lista de GTINs a monitorear
├── productos.csv # Histórico acumulado de precios
├── productos.json # (opcional) Versión en JSON
├── requirements.txt # Dependencias para Streamlit Cloud
└── README.md # Este archivo


---

## 🚀 Cómo usar

### 1. Ejecutar el scraping (manual o automático)

Desde terminal:

`bash
python3 alkosto_gtin_v4.py`




El script:

Lee los GTIN desde gtins.csv

Extrae nombre, precio y fecha desde el sitio web de Alkosto

Guarda los datos en productos.csv y productos.json

Envía alerta por Telegram si hay una baja de precio

2. Ver la app web en Streamlit
https://alkostoalertprice.streamlit.app
(URL de ejemplo: cámbiala si tu app tiene otra dirección)

Desde esta app puedes:

Ver la evolución de precios de cada producto

Filtrar por fechas

Comparar múltiples productos en un mismo gráfico

Detectar visualmente caídas de precio

📅 Automatización
Usa un cron job en Linux/macOS para ejecutar el script automáticamente dos veces por semana:

`bash
0 8 * * 2,5 /usr/bin/python3 /home/usuario/scraping_alkosto/alkosto_gtin_v4.py >> /home/usuario/scraping_alkosto/alkosto_logs/alkosto_cron.log 2>&1`

📬 Telegram
Para recibir alertas:

Crea un bot en @BotFather

Obtén tu BOT_TOKEN

Obtén tu CHAT_ID enviando un mensaje a tu bot y consultando la API

Configura tu token e ID en el script

📌 Notas
Este proyecto no viola los Términos de Uso de Alkosto, ya que accede a URLs públicas sin automatizar clics ni simular usuarios.

No almacena datos personales ni credenciales.

Está diseñado con fines académicos y de interés personal.

📚 Requisitos
nginx
Copiar
Editar
streamlit
pandas
beautifulsoup4
requests
matplotlib


Instálalos con:

`bash
pip install -r requirements.txt`



👤 Autor
Devin AI
Repositorio: github.com/Devin-mac/AlkostoAlertPrice











