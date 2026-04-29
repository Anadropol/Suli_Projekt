import os
import time
import serial
import serial.tools.list_ports

SSH_CONFIG_COMMANDS = [
    "hostname [hostname]",
    "ip domain-name guugl.com",
    "crypto key generate rsa general-keys modulus 1024",
    "ip ssh version 2",
    "username admin privilege 15 password 0 cisco",
    "enable password cisco",
    "line vty 0 4",
    "transport input ssh",
    "login local",
    "exit"
]

def send_and_check(ser, command):
    ser.write((command + '\r\n').encode())
    time.sleep(0.5)
    
    output = ""
    if ser.in_waiting > 0:
        output = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
        
    error_keywords = ["% invalid input", "% incomplete", "% ambiguous", "% bad", "% error"]
    
    for error in error_keywords:
        if error in output.lower():
            raise RuntimeError(f"Hiba a(z) '{command}' parancs kiadásakor!\nEszköz válasza:\n{output.strip()}")
            
    print(f'Elküldött parancs: {command}')
    return output

def configure_ssh(port):
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=2)
        print(f'Csatlakozva a {port} porthoz. Eszköz állapotának ellenőrzése...')

        ser.write(b'\r\n')
        time.sleep(1)
        
        output = ser.read(ser.in_waiting or 1000).decode('utf-8', errors='ignore')
        
        if "initial configuration dialog" in output.lower():
            print("Initial config dialog észlelve. 'no' parancs küldése...")
            ser.write(b'no\r\n')
            
            print("Várakozás az eszköz inicializálására (kb. 15 másodperc)...")
            time.sleep(15)
            
            ser.write(b'\r\n')
            time.sleep(1)
            
            if ser.in_waiting > 0:
                ser.read(ser.in_waiting)
        else:
            print("Nincs initial config dialog. Folytatás...")

        ser.write(b'\r\n\r\n')
        time.sleep(1)
        prompt_output = ser.read(ser.in_waiting or 1000).decode('utf-8', errors='ignore').strip()
        
        current_prompt = prompt_output.split('\n')[-1].strip() if prompt_output else ""
        print(f"Észlelt prompt: {current_prompt}")

        if '(config' in current_prompt:
            print("Már konfigurációs módban vagyunk.")
        elif current_prompt.endswith('#'):
            print("Privileged EXEC mód észlelve. Belépés Config módba...")
            send_and_check(ser, "conf t")
        elif current_prompt.endswith('>'):
            print("User EXEC mód észlelve. Belépés Privileged EXEC, majd Config módba...")
            send_and_check(ser, "enable")
            send_and_check(ser, "conf t")
        else:
            print("Ismeretlen prompt állapot. Kísérlet a belépésre...")
            send_and_check(ser, "enable")
            send_and_check(ser, "conf t")

        print("Konfiguráció indítása...")
        
        current_hostname = ""

        for command in SSH_CONFIG_COMMANDS:
            if '[hostname]' in command:
                current_hostname = input('Add meg az eszköz hostname-jét: ').strip()
                command = command.replace('[hostname]', current_hostname)
            
            send_and_check(ser, command)
        
        if current_hostname:
            config_file = f"configs/{current_hostname}.conf"
            if os.path.isfile(config_file):
                print(f"\nTovábbi konfiguráció betöltése innen: {config_file}...")
                
                # Felesleges parancsok kiszűrése a külső fájlból
                ignore_commands = ['enable', 'conf t', 'configure terminal']
                
                with open(config_file, 'r') as f:
                    for line in f:
                        cmd = line.strip()
                        if cmd and not cmd.startswith('#'):
                            if cmd.lower() in ignore_commands:
                                print(f"[*] Felesleges parancs kihagyva a .conf fájlból: {cmd}")
                                continue
                            send_and_check(ser, cmd)
            else:
                print(f"\nFigyelmeztetés: A(z) {config_file} nem található, további parancsok kihagyva.")

        print('Teljes konfiguráció befejeződött.')
        ser.close()
        
    except Exception as e:
        print(f'\n[!] VÉGREHAJTÁSI HIBA: {e}')
        print('A konfiguráció megszakadt.')
        if 'ser' in locals() and ser.is_open:
            ser.close()

while True:
    ports = serial.tools.list_ports.comports()
    if len(ports) > 0:
        print('\nSoros portok találhatók!')

        for port in ports:
            print(f'{port.device}: {port.description}')
        
        selected_port = input('Add meg a csatlakozni kívánt soros portot (vagy "q" a kilépéshez): ')
        
        if selected_port.lower() == 'q':
            break
            
        if selected_port in [port.device for port in ports]:
            print(f'Csatlakozás a(z) {selected_port} porthoz...')
            configure_ssh(selected_port)
            break
        else:
            print('Érvénytelen port lett kiválasztva. Kérlek, próbáld újra.')
    else:
        print('Nem található soros port.')
        break