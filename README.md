# Project

Il progetto è stato realizzato con lo scopo di attuare delle predizioni di crisi epilettiche su tracciati EEG che registrano le attività del  cervello umano a livello neurale.
La predizione viene effettuata attraverso una rete neurale allenata per riconoscere le varie crisi presenti.
Queste predizioni vengono eseguite su file .edf (European Data Format) i quali permettono un'archiviazione di segnali biologici e fisici multicanale.
Il tool non solo permette di predirre le crisi presenti in un tracciato EEG, ma dispone di altre funzionalità come la definizione di alcune statistiche che riguardano tutti i segnali e tutti i canali presenti nel tracciato.
Viene fornita all'utente l'opportunità di creare il proprio dataset di allenamento che poi sarà usato sulla rete neurale che esso stesso potrà definirsi. 
Il progetto è stato suddiviso in:

- studio EEG e teoria delle crisi
- studio per la creazione del dataset (segnali ictali, preictali e postictali)
- bilanciamento dataset
- studio teorico cnn
- applicazione CNN con relativo allenamento
- costruzione architettura web con beckend e frontend 

Il progetto è correlato da una relazione dettagliata (report.pdf) e una presentazione 
