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
var collection = connenction.GetCollection()

func main() {
	//Connection mongoDB with helper class
	// var cleint = options.Client()


	//Init Router
	r := mux.NewRouter()

  	// // arrange our route
	r.HandleFunc("/api/books", getBooks).Methods("GET")
	// r.HandleFunc("/api/books/{id}", getBook).Methods("GET")
	// r.HandleFunc("/api/books", createBook).Methods("POST")
	// r.HandleFunc("/api/books/{id}", updateBook).Methods("PUT")
	// r.HandleFunc("/api/books/{id}", deleteBook).Methods("DELETE")

  	// set our port address
	log.Fatal(http.ListenAndServe(":8000", r))

}

func getBooks(w http.ResponseWriter, r *http.Request) {


	w.Header().Set("Content-Type", "application/json")

	// we created Book array
	var books []models.CurrencyPrice

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
		books = append(books, currencyPrice)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}

	json.NewEncoder(w).Encode(books) // encode similar to serialize process.
}