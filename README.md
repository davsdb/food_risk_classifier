# risk_classifier

Questa repository riporta i codici Python utilizzati per addestrare una rete neurale artificiale alla valutazione del rischio associato ad eventi di pericolo nel settore agroalimentare, 
attraverso i dati presenti nel database RASFF (https://webgate.ec.europa.eu/rasff-window/screen/search).

Il file RASFF_data.csv rappresenta il dataset utilizzato per l'addestramento della rete neurale.

Il codice scraper.py è stato utilizzato per l'estrazione dei dati dal database RASFF nel periodo temporale 2020-2022 mentre i dati compresi nell'intervallo 2004-2019 sono stati gentilemente messi a disposizione da Nogales, Alberto and Garcia-Tejedor, Alvaro J. (2021): 
“Food and feed health risk notifications in the European Union: a historical dataset of the issues registered in the Rapid Alert System for Food and Feed portal.” 
Mendeley Data, V2, doi: 10.17632/yxkm4gs7zf.2

Il codice preparator.py è stato utilizzato per pre-processing dei dati nel quale sono state scelte le features di interesse ed estratte le mancanti.

Il codice model.py è stato utilizzato per l'addestramento e la valutazione delle metriche relative ad una rete neurale, con l'obiettivo di risolvere un problema di classificazione 
del rischio nel settore agroalimentare.

![risk_classifier_workflow](https://github.com/davsdb/risk_classifier/assets/131648044/560f5420-be38-4d14-9509-df698a494d81)

Attenzione: l'autore di questi codici non si ritiene responsabile in caso di uso improprio di essi e delle possibili conseguenze indesiderate.
