/*
Main file that contain the implementation of the Soccer Bet Server
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
*/

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

#define SUCCESS 1
#define FAILURE 0

#define SECRET "SoccerBeteServerSecret"

#include <iostream>
#include <restinio/all.hpp>
#include <chrono>
#include <restinio/helpers/http_field_parsers/bearer_auth.hpp>
#include <jwt-cpp/jwt.h>

using std::chrono::system_clock;
using namespace restinio;

// custom include 
#include "DBController.h"

template<typename T>
std::ostream& operator<<(std::ostream& to, const optional_t<T>& v) {
	if (v) to << *v;
	return to;
}

auto on_request(const restinio::request_handle_t& req) {
    using namespace restinio::http_field_parsers::bearer_auth;
    const auto auth_params = try_extract_params(*req,
        restinio::http_field::authorization);
    if (auth_params) {
        auto decoded = jwt::decode(auth_params->token);
        auto verifier = jwt::verify()
            .allow_algorithm(jwt::algorithm::hs256{ SECRET })
            .with_issuer("auth0");
        try {
            verifier.verify(decoded);
            return true;
        }
        catch (const jwt::token_verification_exception& e) {
            return false;
        }
    }
    else {
        return false;
    }
}

int main(void) {
	// istantiate DB controller Object
	DB_Controller ctrl = DB_Controller("mongodb://localhost:27017", "SoccerBet_DB");

	// SetUp the DB Connection
	try {
	    mongocxx::instance instance{};
	    mongocxx::uri uri(ctrl.getUri());
        mongocxx::pool pool{ uri };

	    std::cout << ctrl.getDbName() + " Running at: " + ctrl.getUri() << endl;
        Logger("ServerLogger.txt", ctrl.getDbName() + " Running at: " + ctrl.getUri());
        // SETUP CUSTOM ROUTES FOR THE SERVER
        auto router = std::make_unique<router::express_router_t<>>();
        router->http_get(
            R"(/ping)",
            [](auto req, auto) {
                return req->create_response(restinio::status_ok())
                       .set_body("Pong !!!")
                       .done();
            });

        //USERS MANAGEMENT ROUTES
        router->http_get(
            R"(/user)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json res = ctrl.FindUsers();
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /user 200");
                    return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /user 417");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }

            });

        router->http_get(
            R"(/user/:id)",
            [&ctrl, &pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindUser(id);
                    if (res.contains("_id")) {
                        auto result = res.dump();
                        Logger("ServerLogger.txt", "GET /user/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                            .set_body(result)
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "GET /user/:id 404");
                        return req->create_response(restinio::status_not_found())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("This user doesn't exist!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "GET /user/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_post(
            R"(/login)",
            [&ctrl, &pool](auto req, auto params) {
                auto client = pool.acquire();
                mongocxx::database db = (*client)[ctrl.getDbName()];
                ctrl.SetDB(db);

                json body = json::parse(req->body());
                json result = ctrl.FindUserByMailPass(body["email"], body["password"]);
                if (!result.contains("_id")) {
                    Logger("ServerLogger.txt", "POST /login 404");
                    return req->create_response(restinio::status_not_found())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("User not found!!")
                        .done();
                }
                else {
                    json tkn_payload = { { "email",result["email"] } , { "password", result["password"] } };
                    auto token = jwt::create()
                        .set_issuer("auth0")
                        .set_issued_at(std::chrono::system_clock::now())
                        .set_expires_at(std::chrono::system_clock::now() + std::chrono::seconds{ 3600 })
                        .set_type("JWS")
                        .set_payload_claim("sample", jwt::claim())
                        .sign(jwt::algorithm::hs256{ SECRET });

                    json res = { { "id",result["_id"]["$oid"] }, {"admin",result["admin"]} , {"token", token} };
                    string result = res.dump();
                        Logger("ServerLogger.txt", "POST /login 200");
                        return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
            });

        router->http_post(
            R"(/register)",
            [&ctrl,&pool](auto req, auto params) {
                auto client = pool.acquire();
                mongocxx::database db = (*client)[ctrl.getDbName()];
                ctrl.SetDB(db);

                json body = json::parse(req->body());
                User user;
                if (body.contains("admin")) {
                    user = { body["name"] ,body["surname"] , body["email"] , body["password"] , 0.0 , user.admin = body["admin"] };
                }
                else {
                    user = { body["name"] ,body["surname"] , body["email"] , body["password"] , 0.0 , user.admin = false };
                }
         
                json user_check = ctrl.FindUserByMailPass(user.email, user.password);
                if (!user_check.contains("_id")) {
                    int result = ctrl.InsertUser(user);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "POST /register 201");
                        return req->create_response(restinio::status_created())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("User inserted correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "POST /register 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: User not inserted!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "POST /register 417");
                    return req->create_response(restinio::status_expectation_failed())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Registration failed: this user already exist!!")
                        .done();
                }
            });

        router->http_put(
            R"(/user/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json body = json::parse(req->body());
                    User user;
                    if (body.contains("admin")) {
                        user = { body["name"] ,body["surname"] , body["email"] , body["password"] , body["balance"] , user.admin = body["admin"] };
                    }
                    else {
                        user = { body["name"] ,body["surname"] , body["email"] , body["password"] , body["balance"] , user.admin = false };
                    }

                    string id = restinio::cast_to<std::string>(params["id"]);
                    int result = ctrl.UpdateUser(id, user);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "PUT /user/:id 201");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("User updated correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "PUT /user/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: User not updated!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "PUT /user/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_delete(
            R"(/user/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    int result = ctrl.DeleteUser(id);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "DELETE /user/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("User deleted correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "DELETE /user/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: User not deleted!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "DELETE /user/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }

            });

        router->http_put(
            R"(/user/balance/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json body = json::parse(req->body());
                    string id = restinio::cast_to<std::string>(params["id"]);
                    int upd_b_res = ctrl.UpdateUserBalance(id, body["update_quantity"]);
                    if (upd_b_res == SUCCESS) {
                        Logger("ServerLogger.txt", "PUT /user/balance/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Balance updated correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "PUT /user/balance/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: balance not updated!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "PUT /user/balance/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        //EVENT MANAGEMENT ROUTES
        router->http_get(
            R"(/event)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json res = ctrl.FindEvents();
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /event 200");
                    return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /event 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_get(
            R"(/event/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindEvent(id);
                    if (res.contains("_id")) {
                        auto result = res.dump();
                        Logger("ServerLogger.txt", "GET /event 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                            .set_body(result)
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "GET /event 404");
                        return req->create_response(restinio::status_not_found())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: this event doesn't exist!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "GET /event/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_post(
            R"(/event)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json body = json::parse(req->body());
                    Event evento;
                    evento.name = body["name"];
                    evento.start_date.d = body["start_date"]["d"];
                    evento.start_date.m = body["start_date"]["m"];
                    evento.start_date.y = body["start_date"]["y"];
                    evento.start_date.h = body["start_date"]["h"];
                    evento.start_date.mm = body["start_date"]["mm"];
                    evento.end_date.d = body["end_date"]["d"];
                    evento.end_date.m = body["end_date"]["m"];
                    evento.end_date.y = body["end_date"]["y"];
                    evento.end_date.h = body["end_date"]["h"];
                    evento.end_date.mm = body["end_date"]["mm"];
                    evento.odds[0] = body["odds"]["1"];
                    evento.odds[1] = body["odds"]["X"];
                    evento.odds[2] = body["odds"]["2"];
                    evento.odds[3] = body["odds"]["GG"];
                    evento.odds[4] = body["odds"]["NG"];
                    evento.odds[5] = body["odds"]["Over_2,5"];
                    evento.odds[6] = body["odds"]["Under_2,5"];
                    int result = ctrl.InsertEvent(evento);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "POST /event 201");
                        return req->create_response(restinio::status_created())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Event inserted correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "POST /event 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: Event not inserted!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "POST /event 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_put(
            R"(/event/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json body = json::parse(req->body());
                    Event evento;
                    evento.name = body["name"];
                    evento.start_date.d = body["start_date"]["d"];
                    evento.start_date.m = body["start_date"]["m"];
                    evento.start_date.y = body["start_date"]["y"];
                    evento.start_date.h = body["start_date"]["h"];
                    evento.start_date.mm = body["start_date"]["mm"];
                    evento.end_date.d = body["end_date"]["d"];
                    evento.end_date.m = body["end_date"]["m"];
                    evento.end_date.y = body["end_date"]["y"];
                    evento.end_date.h = body["end_date"]["h"];
                    evento.end_date.mm = body["end_date"]["mm"];
                    evento.odds[0] = body["odds"]["1"];
                    evento.odds[1] = body["odds"]["X"];
                    evento.odds[2] = body["odds"]["2"];
                    evento.odds[3] = body["odds"]["GG"];
                    evento.odds[4] = body["odds"]["NG"];
                    evento.odds[5] = body["odds"]["Over_2,5"];
                    evento.odds[6] = body["odds"]["Under_2,5"];
                    string id = restinio::cast_to<std::string>(params["id"]);
                    int result = ctrl.UpdateEvent(id, evento);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "PUT /event/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Event updated correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "PUT /event/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: Event not updated!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "PUT /event/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_delete(
            R"(/event/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    //Set to 1.00 value all bet's odds related to the event that we have to eliminate
                    int result = ctrl.DeleteEventOperation(id);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "Delete /event/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Event deleted correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "Delete /event/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: Event not deleted!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "DELETE /event/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        //BET MANAGEMENT ROUTES
        router->http_get(
            R"(/bet)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json res = ctrl.FindBets();
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /bet 200");
                    return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /bet 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_get(
            R"(/bet/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindBet(id);
                    if (res.contains("_id")) {
                        auto result = res.dump();
                        Logger("ServerLogger.txt", "GET /bet/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                            .set_body(result)
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "GET /bet/:id 404");
                        return req->create_response(restinio::status_not_found())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: this bet doesn't exist!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "GET /bet/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_get(
            R"(/bet/user/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindBetsPerUser(id);
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /bet/user/:id 200");
                    return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /bet/user/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_post(
            R"(/bet)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json body = json::parse(req->body());
                    json res = ctrl.FindUser(body["user_id"]);
                    int result;
                    if (res["balance"] >= body["betted_amount"]) {
                        Bet bet;
                        for (int i = 0; i < body["event_outcomes"].size(); i++) {
                            bet.event_outcomes[i].event_id = body["event_outcomes"][i]["event_id"];
                            bet.event_outcomes[i].event_name = body["event_outcomes"][i]["event_name"];
                            bet.event_outcomes[i].outcome_name = body["event_outcomes"][i]["outcome_name"];
                            bet.event_outcomes[i].odd = body["event_outcomes"][i]["odd"];
                        }
                        bet.user_id = body["user_id"];
                        bet.betted_amount = body["betted_amount"];
                        bet.potential_win = body["potential_win"];

                        //Compare actual time with every event date before insert bet
                        Date actual_time;
                        Date event_time;
                        bool validation_flag = true;
                        system_clock::time_point now = system_clock::now();
                        time_t tt = system_clock::to_time_t(now);
                        tm local_tm;
                        localtime_s(&local_tm, &tt);
                        actual_time = { local_tm.tm_mday, local_tm.tm_mon, local_tm.tm_year, local_tm.tm_hour, local_tm.tm_sec };
                        for (int i = 0; i < body["event_outcomes"].size(); i++) {
                            json event_res = ctrl.FindEvent(body["event_outcomes"][i]["event_id"]);
                            event_time = { event_res["start_date"]["day"], event_res["start_date"]["month"], event_res["start_date"]["year"], event_res["start_date"]["hour"], event_res["start_date"]["minute"] };
                            if (actual_time > event_time) {
                                validation_flag = false;
                                break;
                            }
                        }
                        // InsertBetOperation insert the bet and update the user balance
                        if (validation_flag) result = ctrl.InsertBetOperation(bet);
                        else {
                            Logger("ServerLogger.txt", "POST /bet 417");
                            return req->create_response(restinio::status_expectation_failed())
                                .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                                .set_body("Error: One or more event already started!!")
                                .done();
                        };

                        if (result == SUCCESS) {
                            Logger("ServerLogger.txt", "POST /bet 201");
                            return req->create_response(restinio::status_created())
                                .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                                .set_body("Bet inserted correctly!!")
                                .done();
                        }
                        else {
                            Logger("ServerLogger.txt", "POST /bet 417");
                            return req->create_response(restinio::status_expectation_failed())
                                .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                                .set_body("Error: Bet not inserted!!")
                                .done();
                        }
                    }
                    else {
                        Logger("ServerLogger.txt", "POST /bet 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: You don't have enogh money!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "POST /bet 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_delete(
            R"(/bet/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    int result = ctrl.DeleteBet(id);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "DELETE /bet/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Bet deleted correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "DELETE /bet/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: Bet not deleted!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "DELETE /bet/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        //WON BET MANAGEMENT ROUTES
        router->http_get(
            R"(/endedbet/won)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json res = ctrl.FindWonBets();
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /endedbet/won 200");
                    return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /endedbet/won 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_get(
            R"(/endedbet/lost)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json res = ctrl.FindLostBets();
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /endedbet/lost 200");
                    return req->create_response(restinio::status_ok())
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /endedbet/lost 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }

            });

        router->http_get(
            R"(/endedbet/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindEndedBet(id);
                    if (res.contains("_id")) {
                        auto result = res.dump();
                        Logger("ServerLogger.txt", "GET /endedbet/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                            .set_body(result)
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "GET /endedbet/:id 417");
                        return req->create_response(restinio::status_not_found())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: This bet doesn't exist!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "GET /endedbet/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_get(
            R"(/endedbet/won/user/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindWonBetsPerUser(id);
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /endedbet/won/user/:id 200");
                    return req->create_response()
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /endedbet/won/user/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_get(
            R"(/endedbet/lost/user/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    json res = ctrl.FindLostBetsPerUser(id);
                    auto result = res.dump();
                    Logger("ServerLogger.txt", "GET /endedbet/lost/user/:id 200");
                    return req->create_response()
                        .append_header(restinio::http_field::content_type, "text/json; charset=utf-8")
                        .set_body(result)
                        .done();
                }
                else {
                    Logger("ServerLogger.txt", "GET /endedbet/lost/user/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->http_post(
            R"(/endedbet)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    json body = json::parse(req->body());
                    EndedBet ebet;
                    json res = ctrl.FindBet(body["bet_id"]);
                    if (res.contains("_id")) {
                        if (body["won"] == true) ebet = { res["user_id"], body["bet_id"] , res["potential_win"], body["won"] };
                        else ebet = { res["user_id"], body["bet_id"] , 0.00 , body["won"] };
                        // Insert won bet , insert the won bet and delete the bet 
                        int result = ctrl.InsertEndedBetOperation(ebet);
                        if (result == SUCCESS) {
                            Logger("ServerLogger.txt", "POST /endedbet/ 201");
                            return req->create_response(restinio::status_created())
                                .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                                .set_body("Ended Bet inserted correctly!!")
                                .done();
                        }
                        else {
                            Logger("ServerLogger.txt", "POST /endedbet/ 417");
                            return req->create_response(restinio::status_expectation_failed())
                                .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                                .set_body("Error: Ended Bet not inserted!!")
                                .done();
                        }
                    }
                    else {
                        Logger("ServerLogger.txt", "POST /endedbet/ 201");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: This bet doesn't exist!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "POST /endedbet)401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }

            });

        router->http_delete(
            R"(/endedbet/:id)",
            [&ctrl,&pool](auto req, auto params) {
                if (on_request(req)) {
                    auto client = pool.acquire();
                    mongocxx::database db = (*client)[ctrl.getDbName()];
                    ctrl.SetDB(db);

                    string id = restinio::cast_to<std::string>(params["id"]);
                    int result = ctrl.DeleteEndedBet(id);
                    if (result == SUCCESS) {
                        Logger("ServerLogger.txt", "DELETE /endedbet/:id 200");
                        return req->create_response(restinio::status_ok())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Ended Bet deleted correctly!!")
                            .done();
                    }
                    else {
                        Logger("ServerLogger.txt", "DELETE /endedbet/:id 417");
                        return req->create_response(restinio::status_expectation_failed())
                            .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                            .set_body("Error: Ended Bet not deleted!!")
                            .done();
                    }
                }
                else {
                    Logger("ServerLogger.txt", "DELETE /endedbet/:id 401");
                    return req->create_response(restinio::status_unauthorized())
                        .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                        .set_body("Non Autorizzato")
                        .done();
                }
            });

        router->non_matched_request_handler(
            [](auto req) {
                return req->create_response(restinio::status_not_found())
                    .append_header(restinio::http_field::content_type, "text/plain; charset=utf-8")
                    .set_body("Not Found !!")
                    .connection_close()
                    .done();
            });

        // Launching a server with custom traits.
        struct my_server_traits : public default_traits_t {
            using request_handler_t = restinio::router::express_router_t<>;
        };

        restinio::run(
            restinio::on_thread_pool<my_server_traits>(4)
            .port(8080)
            .address("localhost")
            .request_handler(std::move(router)));
	}
	catch (const mongocxx::exception& e) {
		std::cout << "An exception occurred: " << e.what() << std::endl;
		return EXIT_FAILURE;
	}
    catch (const std::exception& ex){
        std::cerr << "Error: " << ex.what() << std::endl;
        return EXIT_FAILURE;
    }
	return EXIT_SUCCESS;
}
