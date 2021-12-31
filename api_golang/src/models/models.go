package models

import "go.mongodb.org/mongo-driver/bson/primitive"

//Create Struct
type Book struct {
	ID       primitive.ObjectID               `json:"id,omitempty" bson:"_id,omitempty"`
	Symbol   string                           `json:"symbol,omitempty" bson:"symbol,omitempty"`
	Time     primitive.DateTime               `json:"time" bson:"time,omitempty"`
	Price    float64                          `json:"price" bson:"price,omitempty"`
}

