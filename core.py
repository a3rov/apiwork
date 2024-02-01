import os
import pygame
import requests


def get_map(adress, delta=0.05):
    cords = get_cords(adress)
    return get_picture(cords, delta)


def get_picture(centre, delta):
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    map_params = {
        "ll": centre,
        "spn": ",".join([str(delta), str(delta)]),
        "l": "map",
    }

    return requests.get(map_api_server, params=map_params)


def get_cords(toponym):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split()

    return ','.join([str(toponym_longitude), str(toponym_lattitude)])


if __name__ == '__main__':
    response = get_map('Казань')

    map_file = "data/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    os.remove(map_file)
