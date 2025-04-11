const express = require('express')
const router = express.Router()
const pokemonController = require('../controllers/pokemonController')

router.get('/', pokemonController.get_all_pokemons)

router.get('/:id', pokemonController.get_pokemon_by_id)

module.exports = router