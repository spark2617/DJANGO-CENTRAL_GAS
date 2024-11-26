import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class HttpRequestException(Exception):
    pass

def enviar_mensagem_wppconnect(numero_destino, mensagem):
    """
    Envia uma mensagem de WhatsApp usando o servidor WppConnect.
    """
    # Configurações do WppConnect
    url = getattr(settings, "WPP_CONNECT_URL", "http://localhost:21465/api/test/send-message")
    token = getattr(settings, "WPP_CONNECT_TOKEN", "")


    if not token:
        logger.error("Token de autenticação para o WppConnect não configurado.")
        return {"error": "Token de autenticação não configurado."}

    # Dados da mensagem
    payload = {
        "phone": numero_destino,
        "message": mensagem
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"Enviando mensagem para {numero_destino} com payload: {payload}")
        response = requests.post(url, json=payload, headers=headers)

        # Inspeção detalhada da resposta
        logger.info(f"Status Code: {response.status_code}, Response: {response.text}")
        
        # Verifica resposta de sucesso
        if response.status_code in [200, 201]:
            logger.info("Mensagem enviada com sucesso")
            return response.json()
        

        raise HttpRequestException(f"Erro: {response.status_code} - {response.text}")

    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição ao WppConnect: {str(e)}")
        return {"error": "Erro na requisição ao WppConnect", "details": str(e)}
