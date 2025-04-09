use aerospike::{Bins, Client, ClientPolicy, Key, ReadPolicy, Value, WritePolicy};
use anyhow::Result;
use axum::{
    extract::{Path, State},
    http::{Method, StatusCode},
    response::{IntoResponse, Response},
    routing::get,
    Router,
};
use serde::{Deserialize, Serialize};
use tokio::net::TcpListener;
use std::sync::Arc;
use tower_http::trace::TraceLayer;

// Constants
const HOST: &str = "localhost";
const PORT: u16 = 3000;
const NAMESPACE: &str = "test";

// Response types
#[derive(Serialize)]
struct ErrorResponse {
    message: String,
}

#[derive(Serialize)]
struct SuccessResponse {
    value: serde_json::Value,
}

// Application state
#[derive(Clone)]
struct AppState {
    client: Arc<Client>,
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt::init();

    // Connect to Aerospike
    let policy = ClientPolicy::default();
    let hosts = vec![aerospike::Host::new("127.0.0.1", 3000)]; // Define the hosts vector with default Aerospike port
    let client = match Client::new(&policy, &hosts) {
        Ok(client) => client,
        Err(err) => return Err(anyhow::anyhow!("Failed to connect to Aerospike: {}", err)),
    };
    let state = AppState {
        client: Arc::new(client),
    };

    // Build router
    let app = Router::new()
        .route("/api/v1/retrieve/:set/:key", get(retrieve_handler))
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    // Start server
    let addr = "0.0.0.0:8080";
    tracing::info!("Server starting on {}", addr);
    axum::serve(TcpListener::bind(addr).await?, app.into_make_service()).await?;

    Ok(())
}

// Handler for retrieving data from Aerospike
async fn retrieve_handler(
    State(state): State<AppState>,
    Path((set, key)): Path<(String, String)>,
) -> Response {
    // Create Aerospike key
    let aero_key = match Key::new(NAMESPACE, &set, Value::String(key)) {
        Ok(k) => k,
        Err(_) => {
            return (
                StatusCode::BAD_REQUEST,
                "Invalid key",
            )
                .into_response();
        }
    };

    // Read policy
    let mut read_policy = ReadPolicy::default();
    read_policy.timeout = Some(std::time::Duration::from_millis(5000));

    // Get record
    match state.client.get(&read_policy, &aero_key, ["name"]) {
        Ok(record) => {
            // Extract the "name" bin value
            let value = record.bins.get("name").cloned();
            let value = serde_json::Value::String(value.unwrap().to_string());
            
            // Return success response
            let response = SuccessResponse { value };
            (
                StatusCode::OK,
                [(axum::http::header::CONTENT_TYPE, "application/json")],
                serde_json::to_string(&response).unwrap(),
            )
                .into_response()
        }
        Err(_) => {
            // Return error response
            let response = ErrorResponse {
                message: "could not find value in aerospike".to_string(),
            };
            (
                StatusCode::NOT_FOUND,
                [(axum::http::header::CONTENT_TYPE, "application/json")],
                serde_json::to_string(&response).unwrap(),
            )
                .into_response()
        }
    }
}
