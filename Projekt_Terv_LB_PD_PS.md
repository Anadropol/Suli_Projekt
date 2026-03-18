# Projekt terv - Lossó Bálint, Pásztor Dávid, Pintér Soma

**Topológia**

![](topologia.webp "Topológia")

**Címzési Táblázat**

| Eszköz | Interface | Cím | Gateway |
| :--- | :--- | :--- | :--- |
| ISP | g0/0 | 9.11.69.65/30 | - |
| ISP | g0/1 | 9.11.69.69/30 | - |
| ISP | g0/2 | 9.11.69.73/30 | - |
| KR1 | s0/0/0 | 192.168.50.1/30 | - |
| KR1 | g0/0 | 9.11.69.66/30 | - |
| KR1 | g0/2 | 192.168.0.1/30 | - |
| KR1 | fa0/1/1.10 | 192.168.10.2/24 | - |
| KR1 | fa0/1/1.20 | 192.168.20.2/24 | - |
| KR1 | fa0/1/1.30 | 192.168.30.2/24 | - |
| KR1 | fa0/1/1.88 | 192.168.88.2/24 | - |
| KR1 | fa0/1/1.100 | 192.168.100.2/24 | - |
| KR1 | fa0/1/2.10 | 192.168.10.3/24 | - |
| KR1 | fa0/1/2.20 | 192.168.20.3/24 | - |
| KR1 | fa0/1/2.30 | 192.168.30.3/24 | - |
| KR1 | fa0/1/2.88 | 192.168.88.3/24 | - |
| KR1 | fa0/1/2.100 | 192.168.100.3/24 | - |
| KR2 | g0/0 | 9.11.69.74/30 | - |
| KR2 | g0/2 | 192.168.0.2/30 | - |
| KR2 | fa0/0/1.10 | 192.168.10.4/24 | - |
| KR2 | fa0/0/1.20 | 192.168.20.4/24 | - |
| KR2 | fa0/0/1.30 | 192.168.30.4/24 | - |
| KR2 | fa0/0/1.88 | 192.168.88.4/24 | - |
| KR2 | fa0/0/1.100 | 192.168.100.4/24 | - |
| KR2 | fa0/0/2.10 | 192.168.10.5/24 | - |
| KR2 | fa0/0/2.20 | 192.168.20.5/24 | - |
| KR2 | fa0/0/2.30 | 192.168.30.5/24 | - |
| KR2 | fa0/0/2.88 | 192.168.88.5/24 | - |
| KR2 | fa0/0/2.100 | 192.168.100.5/24 | - |
| IR1 | s0/0/0 | 192.168.50.2/30 | - |
| IR1 | g0/0.10 | 192.168.10.6/24 | - |
| IR1 | g0/0.20 | 192.168.20.6/24 | - |
| IR1 | g0/0.30 | 192.168.30.6/24 | - |
| IR1 | g0/0.60 | 192.168.60.6/24 | - |
| IR1 | g0/0.88 | 192.168.88.6/24 | - |
| UR1 | g0/1 | 9.11.69.70/30 | - |
| UR1 | g0/0.10 | 192.168.10.1/24 | - |
| UR1 | g0/0.20 | 192.168.20.1/24 | - |
| ISOHO | wan | 192.168.60.2/24 | - |
| ISOHO | wlan | 192.168.101.1 | - |
| USOHO | wan | 192.168.20.2/24 | - |
| USOHO | wlan | 192.168.101.1 | - |
| SEWIN | eth0 | 192.168.100.253 | - |
| SELIN | eth0 | 192.168.100.254 | - |
| KS1 | vlan88 | 192.168.88.7/24 | - |
| KS2 | vlan88 | 192.168.88.8/24 | - |
| AS1 | vlan88 | 192.168.88.9/24 | - |
| US1 | vlan88 | 192.168.88.10/24 | - |
| IPC1 | eth0 | DHCP | DHCP |
| IPC2 | eth0 | DHCP | DHCP |
| IPC3 | eth0 | DHCP | DHCP |
| KPC1 | eth0 | DHCP | DHCP |
| KPC2 | eth0 | DHCP | DHCP |
| KPC3 | eth0 | DHCP | DHCP |
| KPC4 | eth0 | DHCP | DHCP |
| KPC5 | eth0 | DHCP | DHCP |
| KPC6 | eth0 | DHCP | DHCP |
| UPC1 | eth0 | DHCP | DHCP |
| UPC2 | eth0 | DHCP | DHCP |
| UPC3 | eth0 | DHCP | DHCP |
| IL | w0 | DHCP | DHCP |
| US | w0 | DHCP | DHCP |

**Telephelyek**
- Központ
	- Feladata kiszolgálni a többi telephelyet, a folyamatos szolgáltatás elérés érdekében, 2. és 3. rétegbeli redundanciával rendelkezik.
	- A biztonságos WAN kapcsolat érdekében, minden telephely *tűzfallal* csatlakozik az *ISP* felé.
	- Az *ISP* felé történő, illetve az onnan befelé jövő kommunikáció *tűzfal*lal van védve, illetve a határforgalomirányítón *BGP* fut.
	- Az irodai és központi felhasználók bejelentkezését a *Windows Szerver* szolgálja ki.
	- A *Linux szerver*en *webszerver* fut, mely a *Windows Szerveren* futó *DNS*-en keresztül elérhető.
	- A Windows szerveren DHCP szolgáltatás is fut, mely kiszolgál IPv4 illetve IPv6 címeket egyaránt.
	- A forgalomirányítást OSPFv3-al oldottuk meg.
	- A szerverek ISP felé történő kommunikációjáért statikus címfordíást alkalmazunk, a többi kliens dinamikusan kapja a címet.
	- A központban található *VLAN*-ok:
		- Management **88**
		- HR **10**
		- Sales **20**
		- Marketing **30**
		- Blackhole **100**
- Iroda
	- Az éppen a cég által fejlesztett projektek, a központban elhelyezkedő *Linux szerver*en találhatók, melyek kizárólag *VPN* kapcsolaton keresztül érhetők el.
	- A rendszergazda számítógépén futtathatóak a Linux szerveren mentett konfigurációs fájlok, a hálózati eszközök automatizált konfigurációjára.
	- Az irodában található *VLAN*-ok:
		- Management **88**
		- HR **10**
		- Sales **20**
		- Marketing **30**
		- Blackhole **100**
	- A központi *Linux szerver*hez a hozzáférést *ACL* szabályozza.
- Üzlet
 	- Az üzletben a bankkártyás fizetés elérése érdekében *WI-FI* hálózat működik.
	- Az üzleti hálózat automatikus konfigurációval rendelkezik.
	- Az üzletben található *VLAN*-ok:
		- Guest
		- Desktop
	- Az ISP felé történő kommunikációhoz PAT-ot alkalmazunk.

**Windows Szerveren futó szolgáltatások**
- Active Directory, DNS, DHCP, Automatizált szoftvertelepítés, Webszerver

**Linux Szerveren futó szolgáltatások**
- Webszerver, FTP, Adatbázis, Automatizált mentés
