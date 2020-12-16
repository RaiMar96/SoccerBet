# Main file that contain the implementation of the Stats Server
#Created by:
#Raiti Mario O55000434
#Nardo Gabriele Salvatore O55000430

library(plumber)

apis.Path <- ".\\src\\Stats_Server\\StatsAPIs.R"
stats_api <- plumber::plumb(apis.Path)
stats_api$run(host = '127.0.0.1', port = 9090)