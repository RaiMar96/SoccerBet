# Main file that contain the implementation of the Stats Server APIs
#Created by:
#Raiti Mario O55000434
#Nardo Gabriele Salvatore O55000430
library(mongolite)
library(rjson)

# Logger Function
log_func <- function(call_info) {
    conn <- file("./StatsServerLogger.txt","a")
    msg <- c(paste(as.character(Sys.time()),call_info))
    writeLines(msg, con = conn)
    close(conn)
}

log_func("Stats Server Running at 127.0.0.1:9090")

#* @param msg The message to echo
#* @get /ping
function(msg="pong") {
    list(msg = paste0("The message is: '", msg, "'"))
    log_func("GET /ping 200")
}

#APIs to obtain User Stats

#* @post /userstats
function(req,res) {
    user.stats <- mongo("userstats","SoccerBet")
    body <- rjson::fromJSON(req$postBody)
    temp <- as.data.frame(body)
    result <- user.stats$insert(temp)
    if(result$nInserted == 1){
        log_func("POST /userststas 201")
        res$status <- 201
    } else {
        log_func("POST /userststas 500")
        res$status <- 500
    }
}

#* @delete /userstats/<id>
function(id) {
    user.stats <- mongo("userstats","SoccerBet")
    user.stats$remove(paste0('{"user_id" : "',id, '"}'))
    log_func("DELETE /userstats/id 200")
}


#* @get /userstats
function() {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find('{}')
    log_func("GET /userstats 200")
    return(user.data)
}

#* @get /userstats/<id>
function(id) {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))
    log_func("GET /userstats/id 200")
    return(user.data)
}

#* @get /userstats/<id>/piegraph
#* @serializer contentType list(type='image/png')
function(id) {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))

    tmp <- tempfile()
    png(tmp)
    
    pie <- pie(c(user.data$num_wbet,user.data$num_fbet),
    main = "Rapporto Vittorie Sconfitte",
    labels = c('Scommesse Vinte ',"Scommesse Perse"),
    col=c("green","red"),
    clockwise=TRUE,
    border="black"
    )
    legend("topleft",
    c('Scommesse Vinte ',"Scommesse Perse"),
    fill = c("green","red"))
    dev.off()
    
    log_func("GET /userstats/id/piegrap 200")
    readBin(tmp, "raw", n=file.info(tmp)$size)
}

#* @get /userstats/<id>/bargraph
#* @serializer contentType list(type='image/png')
function(id) {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))

    tmp <- tempfile()
    png(tmp)
    
    bar <- barplot(c(user.data$betted_money,user.data$won_money),
    main="Finanze",
    ylab= "Ammontare in €",
    xlab = paste0('user_id : ',id, ''),
    names.arg=c(round(user.data$betted_money,2),round(user.data$won_money,2)),
    col=c("red","green")
    )
    legend("topleft",
    c('Totale Scommesso €','Totale Vincite €'),
    fill = c("red","green"))
    dev.off()
    
    log_func("GET /userstats/id/bargrap 200")
    readBin(tmp, "raw", n=file.info(tmp)$size)
}

#* @put /userstats/<id>/paid
function(id,req,res) {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))
    new.paid.money <- user.data$paid_money + req$body$paid_money
    result <- user.stats$update(paste0('{"user_id" : "',id, '"}'),paste0('{"$set":{"paid_money": ',new.paid.money,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /userstats/id/paid 200")
        res$status <- 200
    } else  {
        log_func("PUT /userstats/id/paid 500")
        res$status <- 500
    }  
}
#* @put /userstats/<id>/won
function(id,req,res) {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))
    new.won.money <- user.data$won_money + req$body$won_money
    new.num.wbet <- user.data$num_wbet + 1
    result <- user.stats$update(paste0('{"user_id" : "',id, '"}'),paste0('{"$set":{"won_money": ',new.won.money,'},"$set":{"num_wbet": ',new.num.wbet,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /userstats/id/won 200")
        res$status <- 200
    } else  {
        log_func("PUT /userstats/id/won 500")
        res$status <- 500
    }   
}

#* @put /userstats/<id>/lose
function(id,res) {
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))
    new.num.fbet <- user.data$num_fbet + 1
    result <- user.stats$update(paste0('{"user_id" : "',id, '"}'),paste0('{"$set":{"num_fbet": ',new.num.fbet,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /userstats/id/lose 200")
        res$status <- 200
    } else {
        log_func("PUT /userstats/id/lose 500")
        res$status <- 500
    }
}

#* @put /userstats/<id>/bet
function(id,req,res){
    user.stats <- mongo("userstats","SoccerBet")
    user.data <- user.stats$find(paste0('{"user_id" : "',id, '"}'))
    new.user.betted_amount <- user.data$betted_money + req$body$betted_money
    result <- user.stats$update(paste0('{"user_id" : "',id, '"}'),paste0('{"$set":{"betted_money": ',new.user.betted_amount,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /userstats/id/bet 500")
        res$status <- 200
    } else {
        log_func("PUT /userstats/id/bet 500")
        res$status <- 500
    }
}

#APIs to obtain Sistem Stats

#* @post /sistemstats
function(req,res) {
    sis.stats <- mongo("sistemstats","SoccerBet")
    body <- rjson::fromJSON(req$postBody)
    temp <- as.data.frame(body)
    result <- sis.stats$insert(temp)
    if(result$nInserted == 1){
        log_func("POST /sistemstats 201")
        res$status <- 201
    } else {
        log_func("POST /sistemstats 500")
        res$status <- 500
    }
}

#* @put /sistemstats/user/register
function(req,res){
    sis.stats <- mongo("sistemstats","SoccerBet")
    data <- sis.stats$find(query= '{}',   limit = 1)
    new.registered.users <- data$registered_users + 1
    result <- sis.stats$update('{}',paste0('{"$set":{"registered_users": ',new.registered.users,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /sistemstats/user/register 200")
        res$status <- 200
    } else {
        log_func("PUT /sistemstats/user/register 500")
        res$status <- 500
    }
}

#* @put /sistemstats/user/delete
function(req,res){
    sis.stats <- mongo("sistemstats","SoccerBet")
    data <- sis.stats$find(query= '{}',   limit = 1)
    new.registered.users <- data$registered_users - 1
    result <- sis.stats$update('{}',paste0('{"$set":{"registered_users": ',new.registered.users,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /sistemstats/user/delete 200")
        res$status <- 200
    } else {
        log_func("PUT /sistemstats/user/delete 500")
        res$status <- 500
    }
}

#* @put /sistemstats/bet
function(req,res){
    sis.stats <- mongo("sistemstats","SoccerBet")
    data <- sis.stats$find(query= '{}',   limit = 1)
    new.bet.count <- data$bet_count + 1
    new.money.gained <- data$money_gained + req$body$money_gained
    result <- sis.stats$update('{}',paste0('{"$set":{"bet_count":',new.bet.count,'},"$set":{"money_gained":',new.money.gained,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /sistemstats/bet 200")
        res$status <- 200
    } else {
        log_func("PUT /sistemstats/bet 500")
        res$status <- 500
    }
}

#* @put /sistemstats/wbet
function(req,res){
    sis.stats <- mongo("sistemstats","SoccerBet")
    data <- sis.stats$find(query= '{}',   limit = 1)
    new.wbet.count <- data$wbet_count + 1
    new.money.paid <- data$money_paid + req$body$money_paid
    result <- sis.stats$update('{}', paste0('{"$set":{"wbet_count":',new.wbet.count,'},"$set":{"money_paid": ',new.money.paid,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /sistemstats/wbet 200")
        res$status <- 200
    } else {
        log_func("PUT /sistemstats/wbet 500")
        res$status <- 500
    }
}

#* @put /sistemstats/fbet
function(req,res){
    sis.stats <- mongo("sistemstats","SoccerBet")
    data <- sis.stats$find(query= '{}',   limit = 1)
    new.fbet.count <- data$fbet_count + 1
    result <- sis.stats$update('{}',paste0('{"$set":{"fbet_count":',new.fbet.count,'}}'))
    if(result$modifiedCount == 1){
        log_func("PUT /sistemstats/fbet 200")
        res$status <- 200
    } else {
        log_func("PUT /sistemstats/fbet 500")
        res$status <- 500
    }
}

#* @get /sistemstats
function(req) {
    sis.stats <- mongo("sistemstats","SoccerBet")
    alldata <- sis.stats$find(query= '{}',   limit = 1)
    log_func("GET /sistemstats 200")
    return(alldata)
}

#* @delete /sistemstats
function(req) {
    sis.stats <- mongo("sistemstats","SoccerBet")
    sis.stats$drop()
    log_func("DELETE /sistemstats 200")
}

#* @get /sistemstats/piegraph
#* @serializer contentType list(type='image/png')
function(id) {
    sis.stats <- mongo("sistemstats","SoccerBet")
    sis.data <- sis.stats$find(query= '{}',   limit = 1)

    tmp <- tempfile()
    png(tmp)
    
    pie <- pie(c(sis.data$wbet_count,sis.data$fbet_count),
    main = "Rapporto Vittorie Sconfitte",
    labels = c('Scommesse Vinte',"Scommesse Perse"),
    col=c("green","red"),
    clockwise=TRUE,
    border="black"
    )
    legend("topleft",
    c('Scommesse Vinte dagli utenti ',"Scommesse Perse dagli utenti"),
    fill = c("green","red"))
    dev.off()
    
    log_func("GET /sistemstats/piegraph 200")
    readBin(tmp, "raw", n=file.info(tmp)$size)
}

#* @get /sistemstats/bargraph
#* @serializer contentType list(type='image/png')
function(id) {
    sis.stats <- mongo("sistemstats","SoccerBet")
    sis.data <- sis.stats$find(query= '{}',   limit = 1)

    tmp <- tempfile()
    png(tmp)
    
    bar <- barplot(c(sis.data$money_paid,sis.data$money_gained),
    main="Bilancio di Sistema",
    ylab= "Ammontare in €",
    names.arg=c(round(sis.data$money_paid,2),round(sis.data$money_gained,2)),
    col=c("red","green")
    )
    legend("topleft",
    c('Totale Uscite €','Totale Ingressi €'),
    fill = c("red","green"))
    dev.off()
    
    log_func("GET /sistemstats/bargraph 200")
    readBin(tmp, "raw", n=file.info(tmp)$size)
}
