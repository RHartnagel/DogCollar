mod models;
mod config;

use crate::models::Status;
use actix_web::{HttpServer, App, web, Responder, HttpResponse};
use std::io;
use dotenv::dotenv;

async fn status() -> impl Responder {
    HttpResponse::Ok()
        .json(Status{status: "Ok".to_string()})
}
#[actix_rt::main]
async fn main() -> io::Result<()> {

    dotenv().ok();

    let config = crate::config::Config::from_env().unwrap();

    println!("Starting server at http://{}:{}/", config.serer.host, config.serer.port);

    HttpServer::new(||{

        App::new()
            .route("/", web::get().to(status))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}