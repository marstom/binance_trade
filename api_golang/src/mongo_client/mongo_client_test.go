package mongo_client

import (
	"context"
	"fmt"
	"marstom/src/models"
	"testing"

	"go.mongodb.org/mongo-driver/bson"
)

func TestFirmtElement(t *testing.T) {
	config := MongoClient{}.Init()
	collection := config.GetCollection("BTCUSDT")
	cur, _ := collection.Find(context.TODO(), bson.M{})
	cur.Next(context.TODO())
	var book models.CurrencyPrice

	cur.Decode(&book)
	fmt.Println(book)

}
