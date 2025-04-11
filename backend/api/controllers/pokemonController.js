const Pokemon = require("../../models/pokemon")

const get_all_pokemons = async (req, res) => {
    try {
        const pokemons = await Pokemon.find()
        res.status(200).send(pokemons)
    }

    catch (err) {
        console.log(err)
        res.status(400).send(err)
    }
}

const get_pokemon_by_id = async (req, res) => {
    try {
        const pokemon = await Pokemon.find({pokedex_id: req.params.id})
        res.status(200).send(pokemon)
    }

    catch (err) {
        console.log(err)
        res.status(400).send(err)
    }
}

module.exports = {
    get_all_pokemons,
    get_pokemon_by_id
}