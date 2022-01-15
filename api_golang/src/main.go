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
	pricesView := PricesView{mongoClient: &mongoClient}

	r := mux.NewRouter()
	r.HandleFunc("/api/currency/{symbol}", pricesView.getSymbolPrices).Methods("GET")
	r.HandleFunc("/api/buy-sell/{symbol}", pricesView.getBuySellBySymbol).Methods("GET")
	fmt.Println("Server started :8000")
	err := http.ListenAndServe(":8000", r)

	if err != nil {
		log.Fatal(err)
	}

}

type PricesView struct {
	mongoClient *mongo_client.MongoClient
}

func (p *PricesView) getSymbolPrices(w http.ResponseWriter, r *http.Request) {
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

func (p *PricesView) getBuySellBySymbol(w http.ResponseWriter, r *http.Request) {
	// vars := mux.Vars(r)
	// symbol := vars["symbol"]
	collection := p.mongoClient.GetCollection("BUY_SELL")

	var buySell []models.BuySell
	entry, err := collection.Find(context.TODO(), bson.M{})

	if err != nil {
		mongo_client.GetError(err, w)
		return
	}
	defer entry.Close(context.TODO())

	w.Header().Set("Content-Type", "application/json")

	for entry.Next(context.TODO()) {
		var currencyPrice models.BuySell
		err := entry.Decode(&currencyPrice) // decode similar to deserialize process.
		if err != nil {
			log.Fatal(err)
		}

		buySell = append(buySell, currencyPrice)
	}
	if err := entry.Err(); err != nil {
		log.Fatal(err)
	}
	json.NewEncoder(w).Encode(buySell) // encode similar to serialize process.
}
