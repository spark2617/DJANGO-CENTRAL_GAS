from django.db import models
import requests
from django.core.exceptions import ValidationError

class Endereco(models.Model):
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    tipo_moradia = models.CharField(max_length=50)

    lat = models.CharField(max_length=100, null=True, blank=True)
    lon = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.rua}, {self.numero}, {self.bairro}, {self.cidade} - {self.estado}"
    
    def buscar_coordenadas(self):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        endereco_completo = f"rua {self.rua} {self.numero}, {self.cidade}, {self.estado}"
        params = {
            "country":"BR",
            "address": endereco_completo,
            "key": "AIzaSyAxdMXQxHynfCEUF1D9w9Ezn3VdEFwXc7E"
        }
        response = requests.get(url, params=params)
    
        if response.status_code == 200:
            data = response.json()

            if data["status"] == "OK" and data["results"]:
                location = data["results"][0]["geometry"]["location"]
                return location.get("lat"), location.get("lng")
            
        elif response.status_code != 200:
            print("erro na requisição")

        return None, None

    def save(self, *args, **kwargs):
        
        if not self.lat or not self.lon:
            self.lat, self.lon = self.buscar_coordenadas()

        if not self.lat or not self.lon:
            raise ValidationError("O usuário não será criado. verifique o endereço")

        super().save(*args, **kwargs)