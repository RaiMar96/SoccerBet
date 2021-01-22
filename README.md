# SoccerBet
Elaborato finale per il corso, Advanced Programming Languages Project  - UniCT A.A 2019/20. 

Sviluppato da Nardo Gabriele Salvatore O5500430 e Raiti Mario O55000434.

Lo scopo dell’elaborato è quello di realizzare un sistema di betting on line, sotto forma di web app, che permetta agli utenti sottoscritti  al sistema di poter piazzare scommesse calcistiche attraverso il portale

La struttura della repository è la seguente :

- **src** : contine il codice sorgente dei moduli che costutiscono l'applicazione, nello specifico è prevista una sub directory per ogni modulo,
- **docs** : contine la documentazione dettagliata dell'elaborato.

L'elaborato è realizzato in ambiente Windows

## Dipendenze
Per avviare correttamente il sistema è necessario installare sulla propria macchina oltre a **python** , **C++** ed **R** le seguenti dipendenze tramite i link forniti in basso : 

- [PyQT](https://www.learnpyqt.com/installation/) , librearia per la creazione della GUI
- [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/) , database NoSQL usato per la gestioen della persistenza

Come IDE di riferimento per il server c++ è stato utilizato Visual Studio 2019, proprio per questo per installare le successive dipendenze è stata seguita la seguete procedura:

- installare il gestore di pacchetti [vcpkg](https://github.com/Microsoft/vcpkg) seguendo la procedura linkata,
- aprire la shell nel percorso in cui si trova il file _vcpkg.exe_ e digitare i seguenti comandi

```[shell]
.\vcpkg install restinio:x64-windows
.\vcpkg install mongo-cxx-driver:x64-windows
.\vcpkg install nlohmann-json:x64-windows
.\vcpkg install jwt-cpp:x64-windows
.\vcpkg install openssl:x64-windows
.\vcpkg integrate install
```
Per quanto riguarda lo stats server è necessario installare le librerie _mongolite_ , _plumber_ e _rjson_  per una corretta esecuzione. Seguire la seguente procedura per installarle correttamente:

- Avviare l'interprete di **R** come amministratore,
- digitare i seguenti comandi :

```[R]
install.packages("mongolite")
install.packages("plumber")
install.packages("rjson")
```

Per quanto riguarda il Client è necessario installare la libreria __requests__ , __json__ usando pip.

## Avvio
Prima di avviare l'applicazione assicurarsi che le porte 8080 , 9090 e 27017 siano disponibili perchè utilizzate rispettivamente da Server , StatsServer e MongoDB.

- Avviare un'istanza di MongoDB sulla propria Macchina
- Compilare e lanciare il RestServer ( aggiungere alle direttive di compilazione in Visual Studio la seguente macro **_CRT_SECURE_NO_WARNINGS** )
- Lanciare lo **StatsServer**, digitando il seguente comando da terminale all'interno della directory del progetto
```[shell]
Rscript .\src\Stats_Server\StatsServer.R
```
- Lanciare il **Client**, digitando il seguente comando da terminale all'interno della directory src\Client\
```[shell]
python .\SoccerBet.py
```
