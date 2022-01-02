package helper

import (
	"context"
	"encoding/json"
	// "fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Connection struct {
	Client              *mongo.Client
	// Port             string
	// ConnectionString string
}



// Configuration model
type Configuration struct {
	Port             string
	ConnectionString string
}

func (c Connection) Init() Connection{
	c.GetClient()
	return c
}

func (c *Connection) GetClient() {
	config := c.GetConfiguration()
	clientOptions := options.Client().ApplyURI(config.ConnectionString)
	client , err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	c.Client = client
}

// GetConfiguration method basically populate configuration information from .env and return Configuration model
func (c Connection) GetConfiguration() Configuration {
	err := godotenv.Load("./.env")

	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	configuration := Configuration{
		os.Getenv("PORT"),
		os.Getenv("CONNECTION_STRING"),
	}

	return configuration
}

func (c Connection) GetCollection() *mongo.Collection {
	collection := c.Client.Database("live-prices").Collection("BTCUSDT")
	return collection
}

// ErrorResponse : This is error model.
type ErrorResponse struct {
	StatusCode   int    `json:"status"`
	ErrorMessage string `json:"message"`
}

// GetError : This is helper function to prepare error model.
// If you want to export your function. You must to start upper case function name. Otherwise you won't see your function when you import that on other class.
func GetError(err error, w http.ResponseWriter) {

	log.Fatal(err.Error())
	var response = ErrorResponse{
		ErrorMessage: err.Error(),
		StatusCode:   http.StatusInternalServerError,
	}

	message, _ := json.Marshal(response)

	w.WriteHeader(response.StatusCode)
	w.Write(message)
}

