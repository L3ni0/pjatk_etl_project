# PJATK ETL Project
![Diagram](/images/Diagram.png)

Projekt ETL (Extract, Transform, Load) stworzony dla PJATK. Projekt wykorzystuje Docker do uruchomienia w izolowanym środowisku, co gwarantuje spójność między róznymi systemami operacyjnymi (Windows, macOS, Linux).

## 📋 Spis treści

- [Instalacja WSL2 (jeśli masz windowsa)](#windows-z-wsl2)
- [Instalacja](#instalacja)
- [Uruchamianie projektu](#uruchamianie)




##  Instalacja WSL

### jeśli masz Windows:

#### Krok 1: Instalacja WSL2

1. **Otwórz PowerShell jako administrator**
   - Kliknij Start, wpisuW "PowerShell"
   - Kliknij prawym przyciskiem na "Windows PowerShell"
   - Wybierz "Uruchom jako administrator"

2. **Zainstaluj WSL2:**
   ```powershell
   wsl --install
   ```

3. **Uruchom ponownie komputer**

4. **Po restarcie zainstaluje się Ubuntu**
   - Czekaj na komunikat "Installation successful"
   - Podaj nazwę użytkownika i hasło dla Ubuntu

#### Krok 2: Aktualizacja WSL2 do najnowszej wersji

```powershell
wsl --update
wsl --set-default-version 2
```

### Instalacja

#### Krok 1: Instalacja Dockera

https://www.docker.com/get-started/

#### Krok 2: Klonowanie repozytorium

```bash
git clone https://github.com/L3ni0/pjatk_etl_project.git
cd pjatk_etl_project
```

#### Krok 3: Budowanie i uruchamianie kontenera

```bash
# Zbuduj obraz Airflowa
docker build . --tag extended_airflow:latest

# Zainicjuj baze danych
docker compose up airflow-init
```


### Uruchamianie

```bash
# Uruchom wszystkie serwisy
docker-compose up

# Uruchom w tle
docker-compose up -d

# Zatrzymaj serwisy
docker-compose down

# Wyświetl logi
docker-compose logs -f
```

