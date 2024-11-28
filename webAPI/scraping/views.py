from functools import reduce
from django.http import JsonResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def get_content(product):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "es-CO,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://listado.mercadolibre.com.co/{product}').text # https://listado.mercadolibre.com.co/cafetera
    return html_content

def filter_products(product_list):
    
    min_price_value = 99999999999999
    max_price_value = 0
    max_desc_value = 0
    best_rating_value = 0
    
    min_price = product_list[0]
    max_price = product_list[0]
    max_desc = product_list[0]
    best_rating = product_list[0]
    sum_prices = 0
    
    for product in product_list:
        if(isinstance(product['discounted_price'], float)):
            sum_prices += product['discounted_price']
            if(product['discounted_price'] < min_price_value):
                min_price = product
                min_price_value = product['discounted_price']
            if product['discounted_price'] > max_price_value:
                max_price = product
                max_price_value = product['discounted_price']
        if(isinstance(product['discount_percentage'], float)):
            if product['discount_percentage'] > max_desc_value:
                max_desc = product
                max_desc_value = product['discount_percentage']
        if(isinstance(product['rating'], float)):
            if product['rating'] > best_rating_value:
                best_rating = product
                best_rating_value = product['rating']
    prom = sum_prices / len(product_list)
    return {'min_price': min_price, 'max_price': max_price, 'max_desc': max_desc, 'best_rating': best_rating, 'prom': prom}
    

def get_mercadoLibre_products(request):
    product_info_list = []

    if 'query' in request.GET:
        query = request.GET.get('query')
        if not query:
            return JsonResponse({"error": "El parámetro 'query' es requerido."}, status=400)
        html_content = get_content(query)
        soup = BeautifulSoup(html_content, 'html.parser')

        product_items = soup.find_all("div", class_="ui-search-result__wrapper")
        
        for item in product_items:
            is_promoted = item.find("div", class_="poly-footer")
            if not (is_promoted and item.find("a", class_="poly-component__ads-promotions")):
                title_tag = item.find("h2", class_="poly-box poly-component__title")
                if title_tag:
                    title = title_tag.text.strip()
                    product_url = title_tag.find("a")["href"]
                else:
                    title = "No especificado"
                    product_url = "No disponible"
            
                
                current_price_tag = item.find("div", class_="poly-price__current").find("span", class_="andes-money-amount__fraction")
                current_price = float(current_price_tag.text.strip().replace('.', '').replace(',', '.')) if current_price_tag else "No especificado"
            
                previous_price_tag = item.find("s", class_="andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma")
                previous_price = float(previous_price_tag.find("span", class_="andes-money-amount__fraction").text.strip().replace('.', '').replace(',', '.')) if previous_price_tag else "No especificado"
                
                discount_tag = item.find("span", class_="andes-money-amount__discount")
                discount = float(discount_tag.text.strip().replace('% OFF', '')) if discount_tag else "Sin descuento"

                seller_tag = item.find("span", class_="poly-component__seller")
                seller = seller_tag.text.strip() if seller_tag else "No especificado"

                rating_tag = item.find("span", class_="poly-reviews__rating")
                rating = float(rating_tag.text.strip()) if rating_tag else "Sin calificación"
                
                image_tag = item.find("img", class_="poly-component__picture")
                if image_tag:
                    image_url = (
                        image_tag.get("src") if "http" in image_tag.get("src", "") else
                        image_tag.get("data-src") or
                        image_tag.get("srcset") or
                        "No disponible"
                    )
                else:
                    image_url = "No disponible"
                
                product_info = {'name':title, 'original_price': previous_price, 'discounted_price': current_price, 'discount_percentage': discount, 'seller': {'name': seller}, 'rating': rating,'image_url': image_url, 'product_url': product_url}
                product_info_list.append(product_info)
                
    recommendations = filter_products(product_info_list)
               
    return JsonResponse({
        'search_term': query,
        'results': product_info_list,
        'recommendations': recommendations
        }, safe=False)
    
