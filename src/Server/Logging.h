#pragma once
#ifndef LOGGINGFUNC
#define LOGGINFUNC

	#include <iostream>
	#include <chrono>
	#include <fstream>

	using std::chrono::system_clock;
	using namespace std;

	namespace LogUtils {

		inline string getCurrentDateTime() {
			system_clock::time_point now = system_clock::now();
			time_t tt = system_clock::to_time_t(now);
			tm local_tm;
			char buffer[80];
			localtime_s(&local_tm, &tt);
			strftime(buffer, sizeof(buffer), "%d-%m-%Y %H:%M:%S", &local_tm);
			return string(buffer);
		};

		inline void Logger(string file_name, string logMsg) {
			string filePath = "./" + file_name;
			string now = getCurrentDateTime();
			ofstream ofs(filePath.c_str(), std::ios_base::out | std::ios_base::app);
			ofs << now << '\t' << logMsg << '\n';
			ofs.close();
		}

	}

#else
#endif // !LOGGINGFUNC