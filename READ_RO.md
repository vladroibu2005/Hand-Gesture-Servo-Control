## Descrierea proiectului

Acest proiect implementează un sistem de control în timp real al unui servomotor prin gesturi, folosind **Python, OpenCV, MediaPipe și un ESP32**. Poziția orizontală a vârfului degetului arătător este detectată cu ajutorul unei camere web și transformată într-un unghi al servomotorului cuprins între **0° și 180°**.

Sistemul combină procesarea imaginilor, detectarea și urmărirea mâinii, prelucrarea coordonatelor, comunicarea serială și controlul unui actuator fizic într-o singură aplicație interactivă.

### Cum funcționează

Sistemul urmează următorul flux de procesare:

**Cameră web → OpenCV → Detectarea mâinii cu MediaPipe → Detectarea landmark-urilor → Extragerea coordonatelor → Maparea coordonatei în unghi → Comunicare serială → ESP32 → Servomotor SG90**

### 1. Capturarea imaginilor de la cameră

Sistemul folosește OpenCV pentru capturarea continuă a imaginilor de la camera web.

Fiecare cadru este:

* capturat de la cameră;
* răsturnat orizontal pentru a obține o interacțiune asemănătoare unei oglinzi;
* convertit din formatul **BGR în RGB**, necesar pentru procesarea cu MediaPipe.

Cadrele sunt procesate succesiv pentru a obține o interacțiune în timp real.

### 2. Detectarea și urmărirea mâinii

Pentru detectarea și urmărirea mâinii este utilizat **MediaPipe Hand Landmarker**.

Pentru fiecare mână detectată, MediaPipe furnizează **21 de landmark-uri**, fiecare având coordonate normalizate `x`, `y` și `z`.

În cadrul proiectului sunt urmărite în special:

* Landmark `0` — încheietura mâinii;
* Landmark `5` — articulația MCP a degetului arătător;
* Landmark `8` — vârful degetului arătător;
* Landmark `12` — vârful degetului mijlociu.

Landmark-ul `8`, corespunzător vârfului degetului arătător, este utilizat ca punct principal de control.

### 3. Conversia coordonatelor normalizate în pixeli

MediaPipe furnizează coordonatele într-un sistem normalizat, cu valori între `0` și `1`.

Aceste coordonate sunt transformate în coordonate de pixeli folosind dimensiunile curente ale imaginii:

```python
x = int(point.x * w)
y = int(point.y * h)
```

Astfel, poziția degetului poate fi afișată direct pe imagine și utilizată pentru calculele ulterioare.

### 4. Determinarea poziției vârfului degetului arătător

Coordonatele tuturor landmark-urilor detectate sunt stocate într-un dicționar folosind ID-ul fiecărui landmark.

Ulterior este extras landmark-ul `8`:

```python
x8, y8 = coordonate_puncte[8]
```

Valoarea `x8` reprezintă poziția orizontală a vârfului degetului în cadrul imaginii capturate.

### 5. Transformarea poziției mâinii în unghiul servomotorului

Poziția orizontală a degetului este transformată într-un unghi cuprins între **0° și 180°**.

Maparea este realizată în funcție de lățimea cadrului:

```python
angle = int(x8 / w * 180)
```

Astfel:

* partea stângă a imaginii corespunde aproximativ valorii de **0°**;
* centrul imaginii corespunde aproximativ valorii de **90°**;
* partea dreaptă a imaginii corespunde aproximativ valorii de **180°**.

În acest mod, poziția degetului funcționează asemenea unui **slider virtual**.

### 6. Afișarea sliderului virtual

Pentru a oferi feedback vizual utilizatorului, pe imagine este desenat un slider orizontal folosind OpenCV.

Sliderul reprezintă întregul interval de control al servomotorului:

```text
0° ─────────────────────────────── 180°
            ↑
       Poziția curentă
```

Poziția indicatorului este calculată pe baza unghiului curent al servomotorului.

Pe ecran sunt afișate în timp real:

* coordonata X a vârfului degetului;
* coordonata Y;
* unghiul calculat;
* poziția curentă pe slider.

### 7. Comunicarea serială

Unghiul calculat în Python este transmis către ESP32 prin comunicare serială, la o viteză de **115200 baud**.

În loc să fie transmis sub forma unui șir de caractere, unghiul este transmis ca un singur byte:

```python
esp32.write(angle.to_bytes(1, 'little'))
```

Deoarece unghiul este limitat la intervalul `0–180`, întreaga valoare poate fi reprezentată printr-un singur byte.

Acest lucru oferă un protocol de comunicare simplu între aplicația Python și microcontroler.

### 8. Controlul servomotorului prin ESP32

ESP32 primește byte-ul transmis de aplicația Python prin interfața serială.

Valoarea primită este interpretată ca unghiul dorit și transmisă funcției de control a servomotorului:

```cpp
int angle = Serial.read();

if (angle >= 0 && angle <= 180) {
    servo.write(angle);
}
```

Servomotorul SG90 este conectat la un GPIO al ESP32 configurat pentru controlul servomotorului.

ESP32 funcționează astfel ca interfață hardware între aplicația de computer vision și actuatorul fizic.

### 9. Rezultatul fizic

Rezultatul final este controlul în timp real al unui **servomotor SG90**.

Deplasarea degetului arătător pe orizontală modifică unghiul calculat, care este transmis către ESP32 și aplicat servomotorului.

Rezultatul este o interacțiune directă între mișcarea mâinii și un actuator fizic:

**degetul spre stânga → servomotorul se deplasează spre 0°**

**degetul în centru → servomotorul se deplasează spre 90°**

**degetul spre dreapta → servomotorul se deplasează spre 180°**

### Tehnologii utilizate

* **Python 3**
* **OpenCV**
* **MediaPipe**
* **PySerial**
* **ESP32**
* **Arduino IDE**
* **ESP32Servo**
* **SG90 Servo Motor**

### Concepte implementate

Proiectul combină mai multe concepte din domeniul computer vision și embedded systems:

* Procesare video în timp real;
* Detectarea și urmărirea mâinii;
* Landmark-uri MediaPipe;
* Conversia coordonatelor normalizate în pixeli;
* Prelucrarea coordonatelor;
* Maparea liniară a valorilor;
* Comunicare serială;
* Programarea ESP32;
* Controlul unui servomotor;
* Comunicare Python–microcontroler;
* Integrarea computer vision cu un actuator fizic.
