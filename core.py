import os
import pygame
import requests

delta = '0.05'
map_file = "data/map.png"
clock = pygame.time.Clock()


def get_map(adress):
    cords = get_cords(adress)
    response = get_picture(cords, delta)

    with open(map_file, "wb") as file:
        file.write(response.content)


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
    get_map('Казань')

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    running = True
    image = pygame.image.load(map_file)

    while running:
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_UP:
                    delta = str(float(delta) * 1.5)
                    get_map('Казань')
                    image = pygame.image.load(map_file)

                if key == pygame.K_DOWN:
                    delta = str(float(delta) / 1.5)
                    get_map('Казань')
                    image = pygame.image.load(map_file)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    os.remove(map_file)
