package main

import (
	"encoding/json"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/aerospike/aerospike-client-go"
)

const (
	host      = "localhost"
	port      = 3000
	namespace = "test"
)

type ErrorResponse struct {
	Message string `json:"message"`
}

type SuccessResponse struct {
	Value interface{} `json:"value"`
}

func main() {
	db, err := aerospike.NewClient(host, port)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	http.HandleFunc("/api/v1/retrieve/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		// Extract path parameters
		parts := strings.Split(r.URL.Path, "/")
		if len(parts) != 6 {
			http.Error(w, "Invalid path", http.StatusBadRequest)
			return
		}

		set := parts[4]
		key := parts[5]

		// Create Aerospike key
		aeroKey, err := aerospike.NewKey(namespace, set, key)
		if err != nil {
			http.Error(w, "Invalid key", http.StatusBadRequest)
			return
		}

		// Read policy
		readPolicy := aerospike.NewPolicy()
		readPolicy.TotalTimeout = 5000 * time.Millisecond

		// Get record
		record, err := db.Get(readPolicy, aeroKey)
		if err != nil {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusNotFound)
			json.NewEncoder(w).Encode(ErrorResponse{
				Message: "could not find value in aerospike",
			})
			return
		}

		// Return success response
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(SuccessResponse{
			Value: record.Bins["name"],
		})
	})

	log.Printf("Server starting on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
