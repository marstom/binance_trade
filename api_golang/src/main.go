/*
Example:

http://localhost:8000/api/currency/BTCUSDT


*/
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"marstom/src/mongo_client"
	"marstom/src/models"
	// "go.mongodb.org/mongo-driver/mongo/options"

)

var connenction = mongo_client.MongoClient{}.Init()


func main() {
	//Init Router
	r := mux.NewRouter()

  	// // arrange our route
	r.HandleFunc("/api/currency/{symbol}", getSymbolPrices).Methods("GET")

  	// set our port address
	log.Fatal(http.ListenAndServe(":8000", r))

}

func getSymbolPrices(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)

	collection := connenction.GetCollection(vars["symbol"])

	w.Header().Set("Content-Type", "application/json")

	var currencyPrices []models.CurrencyPrice

	// bson.M{},  we passed empty filter. So we want to get all data.
	cur, err := collection.Find(context.TODO(), bson.M{})

	if err != nil {
		mongo_client.GetError(err, w)
		return
	}

	// Close the cursor once finished
	/*A defer statement defers the execution of a function until the surrounding function returns.
	simply, run cur.Close() process but after cur.Next() finished.*/
	defer cur.Close(context.TODO())

	for cur.Next(context.TODO()) {

		// create a value into which the single document can be decoded
		var currencyPrice models.CurrencyPrice
		// & character returns the memory address of the following variable.
		err := cur.Decode(&currencyPrice) // decode similar to deserialize process.
		if err != nil {
			log.Fatal(err)
		}

		// add item our array
		currencyPrices = append(currencyPrices, currencyPrice)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}

	json.NewEncoder(w).Encode(currencyPrices) // encode similar to serialize process.
}