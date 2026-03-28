# Projekt Leírás
###  Network Monitor
Python, Flask alapú web szolgáltatás. <br>
Kétféle felhasználás:
1. IP alapú eszköz elérés
	- A keresőbe IP címet beírva, megnézi, hogy van-e ezen az IP címet elérhető eszköz (SSH alapon)
	- Ha van eszköz, akkor megkapjuk a következő adatokat:
		- Interfészek (állapot, hozzárendelt IP cím)
		- Running Config (a teljes running config)
		- Port Security állapotok (switchekhez)
		- OSPF szomszédsági adatok
		- Spanning tree állapot
		- VLAN-ok
2. Hálózat alapú felderítés
	- Hálózatot megadva x.x.x.x/x formátumban, felderíti az adott hálózaton SSH-n elérhető eszközöket.
	- Ezután ezeket kilistázza, majd kiválasztással ismét a következő adatok lekérhetők:
		- Interfészek (állapot, hozzárendelt IP cím)
		- Running Config (a teljes running config)
		- Port Security állapotok (switchekhez)
		- OSPF szomszédsági adatok
		- Spanning tree állapot
		- VLAN-ok

###### Lossó Bálint, Pászor Dávid, Pintér Soma 13.b
