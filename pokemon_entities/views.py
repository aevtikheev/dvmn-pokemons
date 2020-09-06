from typing import Union

import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = ("https://vignette.wikia.nocookie.net/pokemon/images/"
                     "6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/"
                     "width/240/height/240?cb=20130525215832&fill=transparent")


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    if image_url is None:
        image_url = DEFAULT_IMAGE_URL
    icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))
    folium.Marker([lat, lon], tooltip=name, icon=icon).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        image_url = _get_pokemon_image_url(pokemon_entity.pokemon)
        if image_url is not None:
            image_url = request.build_absolute_uri(image_url)
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            name=pokemon_entity.pokemon.title_ru,
            image_url=image_url
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = _get_pokemon_image_url(pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.entities.all():
        image_url = _get_pokemon_image_url(pokemon_entity.pokemon)
        if image_url is not None:
            image_url = request.build_absolute_uri(image_url)
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            name=pokemon.title_ru,
            image_url=image_url
        )

    pokemon_data = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title_ru,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": _get_pokemon_image_url(pokemon),
    }
    if pokemon.previous_evolution is not None:
        pokemon_data['previous_evolution'] = {
            "title_ru": pokemon.previous_evolution.title_ru,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": _get_pokemon_image_url(pokemon.previous_evolution),
        }
    if pokemon.next_evolution.all():
        next_evolution = pokemon.next_evolution.all()[0]
        pokemon_data['next_evolution'] = {
            "title_ru": next_evolution.title_ru,
            "pokemon_id": next_evolution.id,
            "img_url": _get_pokemon_image_url(next_evolution),
        }

    return render(
        request, "pokemon.html",
        context={'map': folium_map._repr_html_(), 'pokemon': pokemon_data}
    )


def _get_pokemon_image_url(pokemon: Pokemon) -> Union[str, None]:
    if pokemon.picture:
        return pokemon.picture.url
    else:
        return None
