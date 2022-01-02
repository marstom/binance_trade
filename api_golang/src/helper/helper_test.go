package helper

import (
	"context"
	"fmt"
	"marstom/src/models"
	"testing"

	"go.mongodb.org/mongo-driver/bson"
)

func TestFirmtElement(t *testing.T){
	config := Connection{}.Init()
	collection := config.GetCollection()
	cur, _ := collection.Find(context.TODO(), bson.M{})
	cur.Next(context.TODO())
	var book models.Book

	cur.Decode(&book)
	fmt.Println(book)

}