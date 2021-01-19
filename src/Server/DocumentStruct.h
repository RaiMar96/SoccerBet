/*
Definition Document Struct
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
*/

#ifndef DATASTRUCT
#define DATASTRUCT

	#include <iostream>
	using namespace std;

	namespace DataModel {

	#define ODDS_DIM 7
	#define EVENT_OUTCOME_DIM 20

		struct User {
			string name;
			string surname;
			string email;
			string password;
			float balance;
			bool admin;
		};

		struct Date {
			int d;
			int m;
			int y;
			int h;
			int mm;

			inline bool operator>(Date d1) {
				if (d >= d1.d && m >= d1.m && y >= d1.y && h >= d1.h && mm > d1.mm) {
					return true;
				}
				else return false;
			};

			inline bool operator<(Date d1) {
				if (d <= d1.d && m <= d1.m && y <= d1.y && h <= d1.h && mm < d1.mm) {
					return true;
				}
				else return false;
			};

			inline bool operator==(Date d1) {
				if (d == d1.d && m == d1.m && y == d1.y && h == d1.h && mm == d1.mm) {
					return true;
				}
				else return false;
			};

			std::string to_string() {
				std::string to_string_date = std::to_string(d) + "/" + std::to_string(m) + "/" + std::to_string(y) + "," + std::to_string(h) + ":" + std::to_string(mm);
				return to_string_date;
			}
		};

		struct Event {
			string name;
			Date start_date;
			Date end_date;
			float odds[ODDS_DIM];
		};

		struct Event_Outcome {
			string event_id;
			string event_name;
			string outcome_name;
			float odd;
		};

		struct Bet {
			string user_id;
			Event_Outcome event_outcomes[EVENT_OUTCOME_DIM];
			float betted_amount;
			float potential_win;
		};

		struct EndedBet {
			string user_id;
			string bet_id;
			float won_amount;
			bool won;

		};
	}
#else
#endif // !DATASTRUCT
