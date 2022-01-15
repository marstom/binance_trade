/*
Example:

http://localhost:8000/api/currency/BTCUSDT


*/
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"marstom/src/models"
	"marstom/src/mongo_client"
	// "go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	mongoClient := mongo_client.MongoClient{}.Init()
	fmt.Println(mongoClient)
	pricesView := PricesView{mongoClient: &mongoClient}

	r := mux.NewRouter()
	r.HandleFunc("/api/currency/{symbol}", pricesView.getSymbolPrices).Methods("GET")
	err := http.ListenAndServe(":8000", r)

	if err != nil {
		log.Fatal(err)
	}

}

type PricesView struct {
	mongoClient *mongo_client.MongoClient
}

func (p *PricesView) getSymbolPrices(w http.ResponseWriter, r *http.Request) {

	fmt.Println(p.mongoClient)
	vars := mux.Vars(r)

	collection := p.mongoClient.GetCollection(vars["symbol"])

	w.Header().Set("Content-Type", "application/json")

	var currencyPrices []models.CurrencyPrice
	cur, err := collection.Find(context.TODO(), bson.M{})

	if err != nil {
		mongo_client.GetError(err, w)
		return
	}

	defer cur.Close(context.TODO())

	for cur.Next(context.TODO()) {
		var currencyPrice models.CurrencyPrice
		err := cur.Decode(&currencyPrice) // decode similar to deserialize process.
		if err != nil {
			log.Fatal(err)
		}

		currencyPrices = append(currencyPrices, currencyPrice)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}

	json.NewEncoder(w).Encode(currencyPrices) // encode similar to serialize process.
}
