const axios = require('axios');
const Pokemon = require('../models/pokemon');

const get_abilities = (data) => {
    abilities = []
    data.forEach(i => {
        ability = {
            name: i.ability.name,
            is_hidden: i.is_hidden
        }
        abilities.push(ability)
    });
    return abilities
}

const get_stats = (data) => {
    stats = []

    data.forEach(i => {
        stat = {
            name: i.stat.name,
            base_stat: i.base_stat
        }
        stats.push(stat)
    })

    return stats
}

const get_types = (data) => {
    types = []

    data.forEach(i => {
        type = i.type.name
        types.push(type)
    })

    return types
}

const get_sprites = (data) => {
    sprites = []
    selected = ["front_default", "front_shiny"]
    selected.forEach(i => {
        sprite = {
            name: i,
            url: data[i]
        }
        sprites.push(sprite)
    })
    return sprites
}

const get_pokemons = async () => {
    const ENDPOINT = "https://pokeapi.co/api/v2/pokemon/";

    pokemons = []
    last_pokemon_id = 1025

    try {
        for (var i = 1; i < last_pokemon_id + 1; i++) {
            const result = await axios.get(ENDPOINT + i);
            if (result.status === 200) {
                const data = result.data

                // console.log(data)
                
                const p = new Pokemon({
                    name: data.name,
                    pokedex_id: data.id, 
                    abilities: get_abilities(data.abilities),
                    based_experience: data.based_experience,
                    species: data.species.name,
                    height: data.height,
                    weight: data.weight,
                    stats: get_stats(data.stats),
                    types: get_types(data.types),
                    sprites: get_sprites(data.sprites)
                })
                
                const new_pokemon = await p.save()
                pokemons.push(new_pokemon)


            }
        }

        return pokemons
    }

    catch (err) {
        console.error("Error fetching data:", err);
        throw err;
    }
}

module.exports = get_pokemons;