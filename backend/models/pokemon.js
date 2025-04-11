const mongoose = require('mongoose')
const Schema = mongoose.Schema;
const {v4 : uuidv4} = require('uuid')

const pokemonSchema = new Schema({
    _id: {
        type:String,
        default: ()=>uuidv4()
    },
    name: {
        type: String,
        required: true
    },
    species: {
        type: String
    },
    pokedex_id: {
        type: Number,
        required: true
    },
    abilities: {
        type: [{
            name: {
                type: String,
                ref: "Ability"
            },
            is_hidden: {
                type: Boolean
            }
        }]
    },
    based_experience: {
        type: Number,
    },
    height: {
        type: Number
    },
    weight: {
        type: Number
    },
    stats: {
        type: [{
            name: {
                type: String
            },
            base_stat: {
                type: Number
            }
        }]
    },
    types: {
        type: [{
            type: String
        }]
    },
    sprites: {
        type: [{
            name: {
                type: String
            },
            url: {
                type: String
            }
        }]
    }
    
    
},{timestamps: true});

const Pokemon = mongoose.model('Pokemon', pokemonSchema);
module.exports = Pokemon