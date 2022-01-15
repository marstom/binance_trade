/*
Mongo response structure
*/
package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type CurrencyPrice struct {
	ID     primitive.ObjectID `json:"id,omitempty" bson:"_id,omitempty"`
	Symbol string             `json:"symbol,omitempty" bson:"symbol,omitempty"`
	Time   primitive.DateTime `json:"time" bson:"time,omitempty"`
	Price  float64            `json:"price" bson:"price,omitempty"`
}

type BuySell struct {
	ID     primitive.ObjectID `json:"id,omitempty" bson:"_id,omitempty"`
	Symbol string             `json:"symbol,omitempty" bson:"symbol,omitempty"`
	Time   primitive.DateTime `json:"time" bson:"time,omitempty"`
	Price  float64            `json:"price" bson:"price,omitempty"`
	Side   string             `json:"side,omitempty" bson:"side,omitempty"`
}
