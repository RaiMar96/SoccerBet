/*
Implementation DBController
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
*/
#include "DBController.h"

#define SUCCESS 0
#define FAILURE 1

// Costructor and Distructor 
DB_Controller::DB_Controller(const string uri, const string DB_name) {
	this->actual_uri = uri;
	this->db_name = DB_name;
};

DB_Controller::~DB_Controller() {
	std::clog << "DEBUG: DB_CONTROLLER DELETED \n";
};

// Getter Methods
string DB_Controller::getDbName() {
	return this->db_name;
}

string DB_Controller::getUri() {
	return this->actual_uri;
}

// Setter Methods
void DB_Controller::SetDB(const mongocxx::database db) {
	this->db = db;
}


// CRUD METHOD FOR USERS
int DB_Controller::InsertUser(const User user) {
	try {
		bsoncxx::document::value user_doc = make_document(
			kvp("name", user.name),
			kvp("surname", user.surname),
			kvp("email", user.email),
			kvp("password", user.password),
			kvp("balance", user.balance),
			kvp("admin", user.admin));
		auto res = this->db["users"].insert_one(std::move(user_doc));
		if (res) {
			std::cout << "Insert User: User Correctly inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert User: User Correctly inserted");
			return SUCCESS;
		} 
		else return FAILURE;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Insert User: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Insert User: an exception occurred");
		throw e;
		return FAILURE;
	}
}

int DB_Controller::UpdateUser(const string user_id, const User user) {
	try {
		json res_user = FindUser(user_id);
		if (res_user.contains("_id")){
			auto res = this->db["users"].replace_one(
				make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(user_id) })),
				make_document(
					kvp("name", user.name),
					kvp("surname", user.surname),
					kvp("email", user.email),
					kvp("password", user.password),
					kvp("balance", user.balance),
					kvp("admin", user.admin)));
			if (res->modified_count() == 1) {
				std::cout << "Update User: User Correctly Updated" << std::endl;
				Logger("DbControllerLogger.txt", "Update User: User Correctly Updated");
				return SUCCESS;
			}
			else {
				std::cout << "Update User: User not Updated" << std::endl;
				Logger("DbControllerLogger.txt", "Update User: User not Updated");
				return FAILURE;
			}
		}
		else {
			std::cout << "Update User: User not found!" << std::endl;
			Logger("DbControllerLogger.txt", "Update User: User not found!");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Update User: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Update User: an exception occurred");
		throw e;
		return FAILURE;
	}
}

const json DB_Controller::FindUser(const string user_id) {
	try {
		auto res = this->db["users"].find_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(user_id) })));
		json j;
		if (res) {
			std::cout << "Find User: User found!" << std::endl;
			Logger("DbControllerLogger.txt", "Find User: User found!");
			j = json::parse(bsoncxx::to_json(res->view()));
		}
		else {
			std::cout << "Find User: User not found!" << std::endl;
			Logger("DbControllerLogger.txt", "Find User: User not found!");
			j = NULL;
		}
		return j;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find User: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Find User : an exception occurred");
		throw e;
	}
}

const json DB_Controller::FindUserByMailPass(const string mail, const string pass) {
	try {
		auto res = this->db["users"].find_one(
			make_document(
				kvp("email", mail),
				kvp("password", pass)
			));
		json j;
		if (res) {
			std::cout << "Find User by Mail and Pass: User found!" << std::endl;
			Logger("DbControllerLogger.txt", "Find User: User found!");
			j = json::parse(bsoncxx::to_json(res->view()));
		}
		else {
			std::cout << "Find User by Mail and Pass: User not found!" << std::endl;
			Logger("DbControllerLogger.txt", "Find User: User not found!");
			j = NULL;
		}
		return j;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find User by Mail and Pass: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Find User by Mail and Pass : an exception occurred");
		throw e;
	}

}

const json DB_Controller::FindUsers() {
	try {
		auto res = this->db["users"].find({});
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Users: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

int  DB_Controller::DeleteUser(const string user_id) {
	try {
		auto res = this->db["users"].delete_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(user_id) })));
		if (res->deleted_count() == 1) {
			std::cout << "Delete User: user correctly deleted" << std::endl;
			Logger("DbControllerLogger.txt", "Delete User: user correctly deleted");
			return SUCCESS;
		}
		else {
			std::cout << "Delete User: user not deleted!" << std::endl;
			Logger("DbControllerLogger.txt", "Delete User: user not deleted!");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Delete User: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Delete User: an exception occurred");
		throw e;
		return FAILURE;
	}
}

int DB_Controller::UpdateUserBalance(const string user_id, const float update_quantity) {
	try {
		auto res = this->db["users"].find_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(user_id) })));
		json j;
		User u;

		if (res) {
			j = json::parse(bsoncxx::to_json(res->view()));
			u.balance = j["balance"] + update_quantity;
			if (u.balance < 0) {
				return FAILURE;
			}
			else {
				auto upd_res = this->db["users"].update_one(
					make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(user_id) })),
					make_document(kvp("$set", make_document(kvp("balance", u.balance)))));
				if ( (u.balance != j["balance"] && upd_res->modified_count() == 1) || (u.balance == j["balance"] && upd_res->matched_count() == 1)) { 
					std::cout << "Update User Balance: Balance correctly updated "<< std::endl;
					Logger("DbControllerLogger.txt", "Update User Balance: Balance correctly updated");
					return SUCCESS; 
				}
				else {
					std::cout << "Update User Balance: Balance not updated " << std::endl;
					Logger("DbControllerLogger.txt", "Update User Balance: Balance not updated");
					return FAILURE; 
				}
			}
		}
		else {
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Update User Balance: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Update User Balance: an exception occurred");
		throw e;
		return FAILURE;
	}
}

// CRUD METHOD FOR EVENTS
int DB_Controller::InsertEvent(const Event evento){
	try {
		bsoncxx::document::value event_doc = make_document(
			kvp("name", evento.name),
			kvp("start_date", 
				make_document(
					kvp("day",evento.start_date.d),
					kvp("month", evento.start_date.m),
					kvp("year", evento.start_date.y),
					kvp("hour", evento.start_date.h),
					kvp("minute", evento.start_date.mm)
				)),
			kvp("end_date",
				make_document(
					kvp("day", evento.end_date.d),
					kvp("month", evento.end_date.m),
					kvp("year", evento.end_date.y),
					kvp("hour", evento.end_date.h),
					kvp("minute", evento.end_date.mm)
				)),
			kvp("odds", 
				make_document(
					kvp("1",evento.odds[0]),
					kvp("X", evento.odds[1]),
					kvp("2", evento.odds[2]),
					kvp("GG", evento.odds[3]),
					kvp("NG", evento.odds[4]),
					kvp("OVER_2,5", evento.odds[5]),
					kvp("UNDER_2,5", evento.odds[6])
				)));
		auto res = this->db["events"].insert_one(std::move(event_doc));
		if (res) {
			std::cout << "Insert Event: Event Correctly inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Event: Event Correctly inserted");
			return SUCCESS;
		}
		else {
			std::cout << "Insert Event: Event NOT inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Event: Event NOT inserted");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Insert Event: An exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Insert Event: An exception occurred");
		throw e;
		return FAILURE;
	}
}

int DB_Controller::UpdateEvent(const string event_id,const Event evento) {
	try {
		auto res = this->db["events"].replace_one(
			make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(event_id) })),
			make_document(
				kvp("name", evento.name),
				kvp("start_date",
					make_document(
						kvp("day", evento.start_date.d),
						kvp("month", evento.start_date.m),
						kvp("year", evento.start_date.y),
						kvp("hour", evento.start_date.h),
						kvp("minute", evento.start_date.mm)
					)),
				kvp("end_date",
					make_document(
						kvp("day", evento.end_date.d),
						kvp("month", evento.end_date.m),
						kvp("year", evento.end_date.y),
						kvp("hour", evento.end_date.h),
						kvp("minute", evento.end_date.mm)
					)),
				kvp("odds",
					make_document(
						kvp("1", evento.odds[0]),
						kvp("X", evento.odds[1]),
						kvp("2", evento.odds[2]),
						kvp("GG", evento.odds[3]),
						kvp("NG", evento.odds[4]),
						kvp("OVER_2,5", evento.odds[5]),
						kvp("UNDER_2,5", evento.odds[6])
					))));
		if (res->modified_count() == 1) {
			std::cout << "Update Event: Event Correctly updated" << std::endl;
			Logger("DbControllerLogger.txt", "Update Event : Event Correctly updated");
			return SUCCESS;
		}
		else {
			std::cout << "Update Event: Event NOT updated" << std::endl;
			Logger("DbControllerLogger.txt", "Update Event: Event NOT updated");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Update Event: An exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Update Event: An exception occurred");
		throw e;
		return FAILURE;
	}
}

const json DB_Controller::FindEvent(const string event_id) {
	try {
		auto res = this->db["events"].find_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(event_id) })));
		json j;
		if (res) {
			std::cout << "Find Event: Event Found" << std::endl;
			Logger("DbControllerLogger.txt", "Find Event: Event Found");
			j = json::parse(bsoncxx::to_json(res->view()));
		}
		else {
			std::cout << "Find Event: Event Not Found" << std::endl;
			Logger("DbControllerLogger.txt", "Find Event: Event Not Found");
			j = NULL;
		}
		return j;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Event: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Find Event: an exception occurred");
		throw e;
	}
}

const json DB_Controller::FindEvents() {
	try {
		auto res = this->db["events"].find({});
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Events: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

int DB_Controller::DeleteEvent(const string  event_id) {
	try {
		auto res = this->db["events"].delete_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(event_id) })));
		if (res->deleted_count() == 1) {
			std::cout << "Delete Events: event deleted" << std::endl;
			Logger("DbControllerLogger.txt", "Delete Events: event deleted");
			return SUCCESS;
		}
		else {
			std::cout << "Delete Events: event not deleted " << std::endl;
			Logger("DbControllerLogger.txt", "Delete Events: event not deleted ");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Delete Event: an exception occurred: " << e.what() << std::endl;
		Logger("DbControllerLogger.txt", "Delete Event: an exception occurred");
		throw e;
		return FAILURE;
	}
}

int DB_Controller::DeleteEventOperation(const string event_id) {
	try {
		json search_res = this->FindBets();
		int upd_odd_res = FAILURE; 
		if (!search_res.is_null()) {
			for (json elem : search_res) {
				upd_odd_res = this->UpdateBetOdd(elem, event_id);
					if (upd_odd_res == FAILURE) {
						std::cout << "Delete Event Operation: Failure" << std::endl;
							Logger("DbControllerLogger.txt", "Delete Event Operation: Failure");
							return FAILURE;
					}
			}
			if (upd_odd_res == SUCCESS) {
				int res_del = this->DeleteEvent(event_id);
					if (res_del == SUCCESS) {
						std::cout << "Delete Event Operation: Success" << std::endl;
						Logger("DbControllerLogger.txt", "Delete Event Operation: Success");
						return SUCCESS;
					}
					else {
						std::cout << "Delete Event Operation: Failure" << std::endl;
						Logger("DbControllerLogger.txt", "Delete Event Operation: Failure");
						return FAILURE;
					}
			}
			else {
				std::cout << "Delete Event Operation: Failure" << std::endl;
				Logger("DbControllerLogger.txt", "Delete Event Operation: Failure");
				return FAILURE;
			}
		}
		else {
			int res_del = this->DeleteEvent(event_id);
			if (res_del == SUCCESS) {
				std::cout << "Delete Event Operation: Success" << std::endl;
				Logger("DbControllerLogger.txt", "Delete Event Operation: Success");
				return SUCCESS;
			}
			else {
				std::cout << "Delete Event Operation: Failure" << std::endl;
				Logger("DbControllerLogger.txt", "Delete Event Operation: Failure");
				return FAILURE;
			}
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Delete Event Operation: an exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

// CRUD METHOD FOR BET
int DB_Controller::InsertBetOperation(const Bet bet) {
	try {
		int update_res = this->UpdateUserBalance(bet.user_id, -bet.betted_amount);
		if (update_res == SUCCESS) {
			int insert_res = this->InsertBet(bet);
			if (insert_res == SUCCESS) {
				std::cout << "Insert Bet Operation: Success" << std::endl;
				Logger("DbControllerLogger.txt", "Insert Bet Operation: Success");
				return SUCCESS;
			}
			else {
				std::cout << "Insert Bet Operation: Failure" << std::endl;
				Logger("DbControllerLogger.txt", "Insert Bet Operation: Failure");
				return FAILURE;
			}
		}
		else {
			std::cout << "Insert Bet Operation: Failure" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Bet Operation: Failure");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Insert Bet Operation An exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

int DB_Controller::InsertBet(const Bet bet) {
	try {
		int size = sizeof(bet.event_outcomes) / sizeof(bet.event_outcomes[0]);

		bsoncxx::builder::basic::document basic_builder{};
		for (int i = 0; i < size; ++i) {
			if (bet.event_outcomes[i].event_id != "") {
				string event_id = "Event_id_";
				string event_outcome = "Event_outcome_";
				string outcome_name = "Outcome_name_";
				string event_name = "Event_name_";
				event_id = event_id + to_string(i + 1);
				event_outcome = event_outcome + to_string(i + 1);
				outcome_name = outcome_name + to_string(i + 1);
				event_name = event_name + to_string(i + 1);
				basic_builder.append(
					kvp(event_id, bet.event_outcomes[i].event_id),
					kvp(outcome_name, bet.event_outcomes[i].outcome_name),
					kvp(event_name, bet.event_outcomes[i].event_name),
					kvp(event_outcome, bet.event_outcomes[i].odd)
				);
			}
		}
		bsoncxx::document::value event_outcome_doc = basic_builder.extract();

		bsoncxx::document::value bet_doc = make_document(
			kvp("user_id", bet.user_id),
			kvp("event_outcomes", event_outcome_doc),
			kvp("betted_amount", bet.betted_amount),
			kvp("potential_win", bet.potential_win));

		auto res = this->db["bets"].insert_one(std::move(bet_doc));
		if (res) {
			std::cout << "Insert Bet: Bet correctly inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Bet: Bet correctly inserted");
			return SUCCESS;
		}
		else {
			std::cout << "Insert Bet: Bet Not inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Bet: Bet Not inserted");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Insert Bet: An exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

int DB_Controller::UpdateBetOdd(const json bet, const string search_event_id) {
	try {
		bsoncxx::builder::basic::document basic_builder{};
		float new_potential_win = bet["betted_amount"]; //init to old betted amount

		for (int i = 0; i < (bet["event_outcomes"].size()/4) ; ++i) {
				string event_id = "Event_id_";
				string event_outcome = "Event_outcome_";
				string outcome_name = "Outcome_name_";
				string event_name = "Event_name_";
				event_id = event_id + to_string(i + 1);
				event_outcome = event_outcome + to_string(i + 1);
				outcome_name = outcome_name + to_string(i + 1);
				event_name = event_name + to_string(i + 1);
				string ev_name_str = bet["event_outcomes"][event_name];
				string ev_id_str = bet["event_outcomes"][event_id];
				string out_name_str = bet["event_outcomes"][outcome_name];
				if (ev_id_str == search_event_id) {
					basic_builder.append(
						kvp(event_id, ev_id_str),
						kvp(outcome_name, out_name_str),
						kvp(event_name, ev_name_str),
						kvp(event_outcome, 1.00)
					);
				}
				else {
					float old_outcome = bet["event_outcomes"][event_outcome];
					basic_builder.append(
						kvp(event_id, ev_id_str),
						kvp(outcome_name, out_name_str),
						kvp(event_name, ev_name_str),
						kvp(event_outcome, old_outcome)
					);
					new_potential_win = new_potential_win * old_outcome;
				}
			
		}

		bsoncxx::document::value event_outcome_doc = basic_builder.extract();
		string bet_id = bet["_id"]["$oid"];
		bet_id.erase(std::remove(bet_id.begin(), bet_id.end(), '"'), bet_id.end());

		auto upd_res = this->db["bets"].update_one(
			make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(bet_id) })),
			make_document(kvp("$set", make_document(kvp("event_outcomes", std::move(event_outcome_doc)), kvp("potential_win", new_potential_win)))));
		if ((new_potential_win != float(bet["potential_win"]) && upd_res->modified_count() == 1) || (new_potential_win == float(bet["potential_win"]) && upd_res->matched_count() == 1)) {
			std::cout << "UpdateBetOdd: SUCCESS " << std::endl;
			Logger("DbControllerLogger.txt", "UpdateBetOdd: SUCCESS ");
			return SUCCESS; 
		}
		else {
			std::cout << "UpdateBetOdd: FAILURE " << std::endl;
			Logger("DbControllerLogger.txt", "UpdateBetOdd: FAILURE ");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Update Bet Odd: An exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

const json DB_Controller::FindBet(const string bet_id) {
	try {
		auto res = this->db["bets"].find_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(bet_id) })));
		json j;
		if (res) {
			std::cout << "Find Bet: Success" << std::endl;
			Logger("DbControllerLogger.txt", "Find Bet: Success");
			j = json::parse(bsoncxx::to_json(res->view()));
		}
		else {
			std::cout << "Find Bet: Failure" << std::endl;
			Logger("DbControllerLogger.txt", "Find Bet: Failure");
			j = NULL;
		}
		return j;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Bet: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

const json DB_Controller::FindBets() {
	try {
		auto res = this->db["bets"].find({});
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Update User: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

const json DB_Controller::FindBetsPerUser(const string user_id) {
	try {
		auto res = this->db["bets"].find(make_document(kvp("user_id", user_id)));
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Bet per User: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

int DB_Controller::DeleteBet(const string  bet_id) {
	try {
		auto res = this->db["bets"].delete_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(bet_id) })));
		if (res->deleted_count() == 1) {
			std::cout << "Delete Bet: bet correctly deleted" << std::endl;
			Logger("DbControllerLogger.txt", "Delete Bet: bet correctly deleted");
			return SUCCESS;
		}
		else {
			std::cout << "Delete Bet: bet NOT deleted" << std::endl;
			Logger("DbControllerLogger.txt", "Delete Bet: bet NOT deleted");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Delete Bet: an exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

// CRUD METHOD FOR WONBET
int DB_Controller::InsertEndedBetOperation(const EndedBet ebet) {
	try {
		int insert_res = this->InsertEndedBet(ebet);
		if (insert_res == SUCCESS) {
			int update_res = this->UpdateUserBalance(ebet.user_id, ebet.won_amount);
			if (update_res == SUCCESS) {
				int delete_res = this->DeleteBet(ebet.bet_id);
				if (delete_res == SUCCESS) {
					std::cout << "Insert Ended Bet Operation: Success" << std::endl;
					Logger("DbControllerLogger.txt", "Insert Ended Bet Operation: Success");
					return SUCCESS;
				}
				else {
					std::cout << "Insert Ended Bet Operation: Failure" << std::endl;
					Logger("DbControllerLogger.txt", "Insert Ended Bet Operation: Failure");
					return FAILURE;
				}
			}
			else {
				std::cout << "Insert Ended Bet Operation: Failure" << std::endl;
				Logger("DbControllerLogger.txt", "Insert Ended Bet Operation: Failure");
				return FAILURE;
			}
		}
		else {
			std::cout << "Insert Ended Bet Operation: Failure" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Ended Bet Operation: Failure");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Insert Ended Bet: an exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

int DB_Controller::InsertEndedBet(const EndedBet ebet) {
	try {
		bsoncxx::document::value ebet_doc = make_document(
			kvp("user_id", ebet.user_id),
			kvp("bet_id", ebet.bet_id),
			kvp("won_amount", ebet.won_amount),
			kvp("won", ebet.won));
		auto res = this->db["ebets"].insert_one(std::move(ebet_doc));
		if (res) {
			std::cout << "Insert Ended Bet: bet correctly inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Ended Bet: bet correctly inserted");
			return SUCCESS;
		}
		else {
			std::cout << "Insert Ended Bet: bet NOT inserted" << std::endl;
			Logger("DbControllerLogger.txt", "Insert Ended Bet: bet NOT inserted");
			return FAILURE;
		}
		
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Insert Ended Bet: an exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}

const json DB_Controller::FindEndedBet(const string ebet_id) {
	try {
		auto res = this->db["ebets"].find_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(ebet_id) })));
		json j;
		if (res) {
			std::cout << "Find Ended Bet: Success" << std::endl;
			Logger("DbControllerLogger.txt", "Find Ended Bet: Success");
			j = json::parse(bsoncxx::to_json(res->view()));
		}
		else {
			std::cout << "Find Ended Bet: Failure" << std::endl;
			Logger("DbControllerLogger.txt", "Find Ended Bet: Failure");
			j = NULL;
		}
		return j;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Ended Bet: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

const json DB_Controller::FindWonBets() {
	try {
		auto res = this->db["ebets"].find(make_document(kvp("won", true)));
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Won Bets: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

const json DB_Controller::FindWonBetsPerUser(const string user_id) {
	try {
		auto res = this->db["ebets"].find(make_document(kvp("user_id", user_id), kvp("won", true)));
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Won Bet per User: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

const json DB_Controller::FindLostBets() {
	try {
		auto res = this->db["ebets"].find(make_document(kvp("won", false)));
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Lost Bets: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

const json DB_Controller::FindLostBetsPerUser(const string user_id) {
	try {
		auto res = this->db["ebets"].find(make_document(kvp("user_id", user_id), kvp("won", false)));
		json results;
		for (auto&& doc : res) {
			json j = json::parse(bsoncxx::to_json(doc));
			results.push_back(j);
		}
		return results;
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Find Lost Bet per User: an exception occurred: " << e.what() << std::endl;
		throw e;
	}
}

int DB_Controller::DeleteEndedBet(const string ebet_id) {
	try {
		auto res = this->db["ebets"].delete_one(make_document(kvp("_id", bsoncxx::types::b_oid{ bsoncxx::oid(ebet_id) })));
		if (res->deleted_count() == 1) {
			std::cout << "Delete Ended Bet: bet correctly deleted" << std::endl;
			Logger("DbControllerLogger.txt", "Delete Ended Bet: bet correctly deleted");
			return SUCCESS;
		}
		else {
			std::cout << "Delete Ended Bet: bet NOT deleted" << std::endl;
			Logger("DbControllerLogger.txt", "Delete Ended Bet: bet NOT deleted");
			return FAILURE;
		}
	}
	catch (const mongocxx::exception& e) {
		std::cout << "Delete Ended Bet: an exception occurred: " << e.what() << std::endl;
		throw e;
		return FAILURE;
	}
}





