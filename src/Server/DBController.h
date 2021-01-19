/*
Header File DBController
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
*/
#ifndef DBCTRL
#define DBCTRL

	#include <cstdint>
	#include <iostream>
	#include <vector>
	#include <bsoncxx/json.hpp>
	#include <mongocxx/client.hpp>
	#include <mongocxx/client_session.hpp>
	#include <mongocxx/exception/operation_exception.hpp>
	#include <mongocxx/stdx.hpp>
	#include <mongocxx/uri.hpp>
	#include <mongocxx/instance.hpp>
	#include <mongocxx/pool.hpp>
	#include <bsoncxx/builder/basic/document.hpp>
	#include <mongocxx/exception/exception.hpp>
	#include <bsoncxx/builder/basic/kvp.hpp>
	#include <nlohmann/json.hpp>
	#include <algorithm>

	#include "DocumentStruct.h"
	#include "Logging.h"

	#define SUCCESS 1
	#define FAILURE 0

	using bsoncxx::builder::basic::kvp;
	using bsoncxx::builder::basic::make_document;
	using json = nlohmann::json;

	using namespace std;
	using namespace DataModel;
	using namespace LogUtils;

	class DB_Controller {
	private:
		string actual_uri;
		string db_name;
		mongocxx::database db;
	public:
		// costructor
		DB_Controller(const string uri = "mongodb://localhost:27017", const string DB_name ="SoccerBet_DB");
	
		// distructor
		~DB_Controller();

		// setter method
		void SetDB(const mongocxx::database db);

		// getter methods
		string getUri();
		string getDbName();

		// CRUD method
		int InsertUser(const User& user);
		int UpdateUser(const string& user_id, const User& user);
		const json FindUser(const string& user_id) const;
		const json FindUserByMailPass(const string& mail, const string& pass) const;
		const json FindUsers() const;
		int DeleteUser(const string& user_id);
		int UpdateUserBalance(const string& user_id, const float& update_quantity);

		int InsertEvent(const Event& event);
		int UpdateEvent(const string& event_id, const Event& event);
		const json FindEvent(const string& event_id) const;
		const json FindEvents() const;
		int DeleteEvent(const string& event_id);
		int DeleteEventOperation(const string& event_id);

		int InsertBet(const Bet& bet);
		int InsertBetOperation(const Bet& bet);
		const json FindBet(const string& bet_id) const;
		const json FindBets() const;
		const json FindBetsPerUser(const string& user_id) const;
		int UpdateBetOdd(const json& bet, const string& event_id);
		int DeleteBet(const string& bet_id);

		int InsertEndedBet(const EndedBet& ebet);
		int InsertEndedBetOperation(const EndedBet& ebet);
		const json FindEndedBet(const string& ebet_id) const;
		const json FindWonBets() const;
		const json FindWonBetsPerUser(const string& user_id) const;
		const json FindLostBets() const;
		const json FindLostBetsPerUser(const string& user_id) const;
		int DeleteEndedBet(const string& bet_id);

	};

#else
#endif
