// docker run --name AmpDexDB -p 27017:27017 -d mongo

const express = require('express')
const app = express();
const cors = require('cors')
const morgan = require('morgan')
const mongoose = require('mongoose');
const get_pokemons = require("./utils/init_data");
const Pokemon = require('./models/pokemon');
require('dotenv').config();

// middleware
app.use(morgan('dev')) //logging
app.use(express.urlencoded( {extended: true}))
app.use(express.json()); 
app.use(cors({origin: true}))

const checkIfDataExistAndFetchData = async () => {
    try {
        const pokemonCount = await Pokemon.countDocuments();
        console.log(`Found ${pokemonCount} pokemons in the database.`);

        if (pokemonCount === 0) {
            console.log("No pokemons found in the database. Fetching data...");
            const pokemons = await get_pokemons();
            console.log(`${pokemons.length} pokemons fetched and saved to the database.`);
        } else {
            console.log("Pokemons data already exists. Skipping data fetch.");
        }
    } catch (err) {
        console.error("Error checking pokemons in the database:", err);
    }
};

// connect to database
const init = async () => {
    try {
        mongoose.set('bufferCommands', false)
        await mongoose.connect(`${process.env.DATABASE}`)
        console.log("Connected to database")

        // Check if schools data exists and fetch if necessary
        checkIfDataExistAndFetchData();

        app.listen(process.env.PORT)
        console.log(`Service is ready to listen on port ${process.env.PORT}`)
    }
    catch(err){
        console.log("Error connecting to database")
    }
}

init()

// ROUTES
const pokemonRoutes = require('./api/routes/pokemonRoutes')
app.use('/pokemon', pokemonRoutes)



// UNKNOWN ROUTES
app.use((req, res) => res.send(null))