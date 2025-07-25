# Dodaj swoje niestandardowe ikony do Home Assistant!

[![hacs_badge](https://img.shields.io/badge/HACS-Integracja-41BDF5.svg)](https://github.com/hacs/integration)
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/Licencja-CC%20BY--NC--SA%204.0-lightgrey.svg

Na podstawie niesamowitej pracy z [Custom Brand Icons](https://github.com/elax46/custom-brand-icons) autorstwa @elax46

Dzięki temu repozytorium będziesz mógł dodać niestandardowe ikony z własnego zestawu do Home Assistant i używać ich na pulpicie Lovelace:

![Niestandardowe ikony](https://github.com/robertbigk/rbk-icons/blob/main/custom-icons.png)

## Wymagania wstępne i ograniczenia

Obowiązkowe:
* Musisz mieć zainstalowanego Pythona 3 na swoim komputerze
* Twoje ikony muszą być w formacie SVG
* Węzeł `svg` musi zawierać tylko właściwość `viewBox`. Wszelkie inne właściwości, takie jak `transform`, `translate` lub `scale`, będą ignorowane
* Element `svg` musi zawierać jeden lub kilka z następujących elementów: `path`, `circle`, `ellipse`, `polygon`, `polyline` lub `rect`
* Kształty mogą być wewnątrz węzła `g`, ale wszelkie właściwości z węzła `g` są ignorowane

Zalecane:
* Twoje ikony są kwadratowe: właściwość viewBox będzie czymś w rodzaju `viewBox="0 0 128 128"`
* Twoje ikony są wyśrodkowane poziomo i pionowo wewnątrz viewBox
* Twoje ikony zawierają tylko jeden element SVG (idealnie jeden `path`) LUB tylko elementy tego samego typu: możesz użyć [tego konwertera online, aby to zrobić](https://thednp.github.io/svg-path-commander/convert.html)

Ograniczenia:
* Właściwości `style` lub `fill` są ignorowane: ikony mogą być tylko monochromatyczne. Home Assistant zarządza kolorami ikon na podstawie motywu i stanu encji.

Aby stworzyć lub edytować ikonę w formacie SVG, możesz użyć różnych programów, takich jak Illustrator, Inkview lub [Inkscape](https://inkscape.org/).

## Jak używać

### 1. Pobierz lub zrób fork tego repozytorium

Jeśli zrobisz fork tego repozytorium, będzie ono publiczne na GitHubie i nie będzie mogło być zmienione.
Jeśli nie chcesz udostępniać swoich ikon publicznie, pobierz to repozytorium zamiast robić fork.

### 2. Dodaj swoje ikony SVG

Dodaj wszystkie swoje ikony SVG do folderu `icon-svg`. Nazwa pliku będzie nazwą ikony w Home Assistant.

Możesz usunąć pliki SVG już obecne do celów demonstracyjnych.

### 3. Wygeneruj plik ikon .js dla Home Assistant

Użyj `python svg-to-js.py`, aby przekonwertować swoje ikony SVG na format Home Assistant. Ten skrypt stworzy plik `rbk-icons.js` zawierający wszystkie Twoje ikony.

Sprawdź wyjście skryptu, jeśli niektóre ikony nie zostały przetworzone. Popraw SVG i uruchom skrypt ponownie.

### 4. Dodaj swoje ikony do Home Assistant

#### Za pomocą HACS

Ta metoda jest dostępna tylko, jeśli zrobiłeś fork tego repozytorium lub skopiowałeś jego zawartość do innego **publicznego** repozytorium na GitHubie.

1. Zatwierdź wygenerowany plik `rbk-icons.js` do głównej gałęzi Twojego repozytorium
2. Upewnij się, że HACS jest zainstalowany.
3. Przejdź do HACS > Frontend > Trzy kropki > Repozytoria niestandardowe.
4. Dodaj URL Twojego repozytorium GitHub jako repozytorium niestandardowe (kategoria: lovelace).
5. Zainstaluj "Moje Niestandardowe Ikony", które pojawiły się w zakładce Interfejs. Możesz dostosować nazwę, edytując `hacs.json`.

Po instalacji przez HACS:
1. Dodaj następujące linie do Twojego `configuration.yaml`:

    ```yaml
    frontend:
      extra_module_url:
        - /local/community/rbk-icons/rbk-icons.js