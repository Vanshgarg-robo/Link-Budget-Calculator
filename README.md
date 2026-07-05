# Link Budget Calculator

A Python-based **Link Budget Calculator** for wireless communication systems. This project calculates **Free-Space Path Loss (FSPL)**, **Received Signal Strength (RSS)**, and **Link Margin**, while generating interactive HTML/SVG graphs to visualize signal performance over distance.

## Features

- Calculates **Free-Space Path Loss (FSPL)**
- Estimates **Received Signal Strength (RSS)**
- Computes **Link Margin**
- Supports configurable:
  - Transmit Power
  - Transmit Antenna Gain
  - Receive Antenna Gain
  - Cable Loss
  - Frequency
  - Distance
- Generates interactive **HTML + SVG** graphs
- Pure Python implementation (No external dependencies)

---

## Formula Used

### Free-Space Path Loss (FSPL)

\[
FSPL(dB)=20\log_{10}(d)+20\log_{10}(f)+32.45
\]

Where:

- **d** = Distance (km)
- **f** = Frequency (MHz)

### Received Signal Strength (RSS)

\[
RSS = P_t + G_t + G_r - L_c - FSPL
\]

Where:

- **Pt** = Transmit Power (dBm)
- **Gt** = Transmit Antenna Gain (dBi)
- **Gr** = Receive Antenna Gain (dBi)
- **Lc** = Cable Loss (dB)

---

## Project Structure

```
Link-Budget-Calculator/
│
├── link_budget_calculator.py
├── link_budget_graphs.html
├── README.md
```

---

## Requirements

- Python 3.8+
- No third-party libraries required

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Link-Budget-Calculator.git
```

Go to the project folder:

```bash
cd Link-Budget-Calculator
```

---

## Run

```bash
python link_budget_calculator.py
```

After execution, the program generates:

- Console report
- Interactive HTML graph (`link_budget_graphs.html`)

Open the HTML file in your browser to view the graphs.

---

## Sample Parameters

| Parameter | Value |
|-----------|------:|
| Transmit Power | 20 dBm |
| Transmit Gain | 2 dBi |
| Receive Gain | 2 dBi |
| Cable Loss | 1 dB |
| Frequency | 2400 MHz |
| Distance | 1 km |

---

## Output

The application provides:

- Free-Space Path Loss (FSPL)
- Received Signal Strength (RSS)
- Link Margin
- Signal Strength vs Distance Graph
- FSPL vs Distance Graph
- Link Margin Visualization
- Wireless Communication Analysis Report

---

## Applications

- RF Communication
- Wireless Network Planning
- Wi-Fi Coverage Analysis
- Cellular Network Analysis
- Satellite Communication
- Communication Engineering Education
- Embedded & IoT Projects

---

## Future Improvements

- GUI using Tkinter or PyQt
- CSV/Excel export
- PDF report generation
- Interactive web dashboard
- Multiple propagation models
- Antenna pattern visualization

---

## Author

**Vansh Garg**
## License

This project is licensed under the MIT License.
