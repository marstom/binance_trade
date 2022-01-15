package mongo_client

import (
	"context"

	"log"

	"os"

	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MongoClient struct {
	Client *mongo.Client
}

type Configuration struct {
	Port             string
	ConnectionString string
}

func (c MongoClient) Init() MongoClient {
	c.initializeClient()
	return c
}

func (c MongoClient) GetCollection(symbol string) *mongo.Collection {
	collection := c.Client.Database("live-prices").Collection(symbol)
	return collection
}

func (c *MongoClient) GetClient() *MongoClient {
	return c
}

func (c *MongoClient) initializeClient() {
	config := c.getConfiguration()
	clientOptions := options.Client().ApplyURI(config.ConnectionString)
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	c.Client = client
}

// getConfiguration method basically populate configuration information from .env and return Configuration model
func (c MongoClient) getConfiguration() Configuration {
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
