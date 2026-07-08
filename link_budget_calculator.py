import math
import os


class LinkBudgetCalculator:
    """
    Link Budget Calculator using only Python standard library.

    RSS (dBm) = Pt + Gt + Gr - Lc - FSPL
    FSPL (dB) = 20*log10(d) + 20*log10(f) + 32.45
    """

    def __init__(self, tx_power_dbm, tx_gain_dbi, rx_gain_dbi, cable_loss_db, frequency_mhz, distance_km):
                     
        self.tx_power_dbm = tx_power_dbm
        self.tx_gain_dbi = tx_gain_dbi
        self.rx_gain_dbi = rx_gain_dbi
        self.cable_loss_db = cable_loss_db
        self.frequency_mhz = frequency_mhz
        if isinstance(distance_km, (list, tuple)):
            self.distance_km = list(distance_km)
            self.is_array = True
        else:
            self.distance_km = [distance_km]
            self.is_array = False

    def free_space_path_loss(self):
        """Calculate FSPL for all distances. Returns list of floats."""
        results = []
        for d in self.distance_km:
            if d <= 0:
                results.append(float('inf'))
            else:
                fspl = 20 * math.log10(d) + 20 * math.log10(self.frequency_mhz) + 32.45
                results.append(fspl)
        return results

    def received_signal_strength(self):
        """Calculate RSS for all distances. Returns list of floats."""
        fspl_list = self.free_space_path_loss()
        results = []
        for fspl in fspl_list:
            rss = self.tx_power_dbm + self.tx_gain_dbi + self.rx_gain_dbi - self.cable_loss_db - fspl
            results.append(rss)
        return results

    def link_margin(self, receiver_sensitivity_dbm):
        """Calculate link margin. Returns list of floats."""
        rss_list = self.received_signal_strength()
        return [rss - receiver_sensitivity_dbm for rss in rss_list]

    def print_budget(self, receiver_sensitivity_dbm=None):
        """Print formatted link budget report to console."""
        print('=' * 62)
        print('           LINK BUDGET CALCULATION REPORT')
        print('=' * 62)
        print(f'{"Parameter":<37} {"Value":>20}')
        print('-' * 62)
        print(f'{"Transmit Power (Pt)":<37} {self.tx_power_dbm:>18.2f} dBm')
        print(f'{"Transmit Antenna Gain (Gt)":<37} {self.tx_gain_dbi:>18.2f} dBi')
        print(f'{"Receive Antenna Gain (Gr)":<37} {self.rx_gain_dbi:>18.2f} dBi')
        print(f'{"Cable/Connector Losses (Lc)":<37} {self.cable_loss_db:>18.2f} dB')
        print(f'{"Frequency (f)":<37} {self.frequency_mhz:>18.2f} MHz')

        if not self.is_array:
            d = self.distance_km[0]
            fspl = self.free_space_path_loss()[0]
            rss = self.received_signal_strength()[0]
            print(f'{"Distance (d)":<37} {d:>18.2f} km')
            print('-' * 62)
            print(f'{"Free-Space Path Loss (FSPL)":<37} {fspl:>18.2f} dB')
            print(f'{"Received Signal Strength (RSS)":<37} {rss:>18.2f} dBm')
            if receiver_sensitivity_dbm is not None:
                margin = self.link_margin(receiver_sensitivity_dbm)[0]
                print(f'{"Receiver Sensitivity":<37} {receiver_sensitivity_dbm:>18.2f} dBm')
                print(f'{"Link Margin":<37} {margin:>18.2f} dB')
        else:
            d_min = min(self.distance_km)
            d_max = max(self.distance_km)
            print(f'{"Distance range":<37} {d_min:>8.2f} - {d_max:>7.2f} km')
        print('=' * 62)


def logspace(start, stop, num):
    """Generate logarithmically spaced values (like numpy.logspace)."""
    if num < 2:
        return [start]
    log_start = math.log10(start)
    log_stop = math.log10(stop)
    step = (log_stop - log_start) / (num - 1)
    return [10 ** (log_start + i * step) for i in range(num)]


def linspace(start, stop, num):
    """Generate linearly spaced values (like numpy.linspace)."""
    if num < 2:
        return [start]
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]


def generate_svg_graphs():
    """
    Generate an HTML file containing SVG graphs.
    No external libraries needed - pure Python string manipulation.
    """
    distances = logspace(0.1, 100, 500)

    wifi = LinkBudgetCalculator(20.0, 2.0, 2.0, 1.0, 2400.0, distances)
    wifi_rss = wifi.received_signal_strength()

    cellular = LinkBudgetCalculator(43.0, 18.0, 0.0, 3.0, 900.0, distances)
    cellular_rss = cellular.received_signal_strength()

    satellite = LinkBudgetCalculator(30.0, 30.0, 25.0, 2.0, 4000.0, distances)
    satellite_rss = satellite.received_signal_strength()

    wifi_zoom_dist = linspace(0.01, 2.0, 200)
    wifi_zoom = LinkBudgetCalculator(20.0, 2.0, 2.0, 1.0, 2400.0, wifi_zoom_dist)
    wifi_zoom_rss = wifi_zoom.received_signal_strength()

    def map_x(val, x_min, x_max, svg_w):
        return 60 + (math.log10(val) - math.log10(x_min)) / (math.log10(x_max) - math.log10(x_min)) * (svg_w - 80)

    def map_x_linear(val, x_min, x_max, svg_w):
        return 60 + (val - x_min) / (x_max - x_min) * (svg_w - 80)

    def map_y(val, y_min, y_max, svg_h):
        return svg_h - 40 - (val - y_min) / (y_max - y_min) * (svg_h - 80)

    def plot_rss_vs_distance():
        w, h = 500, 300
        x_min, x_max = 0.1, 100
        y_min, y_max = -130, 10
        svg = f'<svg width="{w}" height="{h}" style="border:1px solid #ccc;background:#fff;">'
        svg += '<rect width="100%" height="100%" fill="#fafafa"/>'
        for d in [0.1, 1, 10, 100]:
            x = map_x(d, x_min, x_max, w)
            svg += f'<line x1="{x}" y1="20" x2="{x}" y2="{h-40}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="{x}" y="{h-20}" text-anchor="middle" font-size="10" fill="#666">{d}</text>'
        for yv in [-120, -100, -80, -60, -40, -20, 0]:
            y = map_y(yv, y_min, y_max, h)
            svg += f'<line x1="60" y1="{y}" x2="{w-20}" y2="{y}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="50" y="{y+4}" text-anchor="end" font-size="10" fill="#666">{yv}</text>'
        sens_lines = [(-82, 'blue', 'Wi-Fi'), (-102, 'red', 'Cellular'), (-120, 'green', 'Satellite')]
        for sens, color, label in sens_lines:
            y = map_y(sens, y_min, y_max, h)
            svg += f'<line x1="60" y1="{y}" x2="{w-20}" y2="{y}" stroke="{color}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5"/>'
        def make_path(dist_list, rss_list, color):
            pts = []
            for d, r in zip(dist_list, rss_list):
                if r < y_min or r > y_max:
                    continue
                x = map_x(d, x_min, x_max, w)
                y = map_y(r, y_min, y_max, h)
                pts.append(f'{x:.1f},{y:.1f}')
            return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>'
        svg += make_path(distances, wifi_rss, 'blue')
        svg += make_path(distances, cellular_rss, 'red')
        svg += make_path(distances, satellite_rss, 'green')
        legend_items = [('Wi-Fi (2.4 GHz)', 'blue'), ('Cellular (900 MHz)', 'red'), ('Satellite (4 GHz)', 'green')]
        for i, (text, color) in enumerate(legend_items):
            y = 30 + i * 16
            svg += f'<line x1="{w-140}" y1="{y}" x2="{w-120}" y2="{y}" stroke="{color}" stroke-width="2"/>'
            svg += f'<text x="{w-115}" y="{y+4}" font-size="9" fill="#333">{text}</text>'
        svg += f'<text x="{w/2}" y="{h-5}" text-anchor="middle" font-size="11" fill="#333">Distance (km)</text>'
        svg += f'<text x="15" y="{h/2}" text-anchor="middle" font-size="11" fill="#333" transform="rotate(-90,15,{h/2})">RSS (dBm)</text>'
        svg += f'<text x="{w/2}" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">RSS vs Distance (All Scenarios)</text>'
        svg += '</svg>'
        return svg

    def plot_wifi_zoom():
        w, h = 500, 300
        x_min, x_max = 0.0, 2.0
        y_min, y_max = -90, -30
        svg = f'<svg width="{w}" height="{h}" style="border:1px solid #ccc;background:#fff;">'
        svg += '<rect width="100%" height="100%" fill="#fafafa"/>'
        for xv in [0, 0.5, 1.0, 1.5, 2.0]:
            x = map_x_linear(xv, x_min, x_max, w)
            svg += f'<line x1="{x}" y1="20" x2="{x}" y2="{h-40}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="{x}" y="{h-20}" text-anchor="middle" font-size="10" fill="#666">{xv}</text>'
        for yv in [-90, -80, -70, -60, -50, -40, -30]:
            y = map_y(yv, y_min, y_max, h)
            svg += f'<line x1="60" y1="{y}" x2="{w-20}" y2="{y}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="50" y="{y+4}" text-anchor="end" font-size="10" fill="#666">{yv}</text>'
        y_sens = map_y(-82, y_min, y_max, h)
        svg += f'<line x1="60" y1="{y_sens}" x2="{w-20}" y2="{y_sens}" stroke="blue" stroke-width="1" stroke-dasharray="4,4" opacity="0.7"/>'
        svg += f'<text x="{w-100}" y="{y_sens-5}" font-size="9" fill="blue">Sensitivity = -82 dBm</text>'
        pts_above = []
        pts_below = []
        for d, r in zip(wifi_zoom_dist, wifi_zoom_rss):
            x = map_x_linear(d, x_min, x_max, w)
            y = map_y(r, y_min, y_max, h)
            y_s = map_y(-82, y_min, y_max, h)
            if r >= -82:
                pts_above.append(f'{x:.1f},{y:.1f}')
                pts_below.append(f'{x:.1f},{y_s:.1f}')
        if pts_above and pts_below:
            poly = ' '.join(pts_above + pts_below[::-1])
            svg += f'<polygon points="{poly}" fill="green" opacity="0.15"/>'
        pts = []
        for d, r in zip(wifi_zoom_dist, wifi_zoom_rss):
            x = map_x_linear(d, x_min, x_max, w)
            y = map_y(r, y_min, y_max, h)
            pts.append(f'{x:.1f},{y:.1f}')
        svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="blue" stroke-width="2"/>'
        svg += f'<text x="{w/2}" y="{h-5}" text-anchor="middle" font-size="11" fill="#333">Distance (km)</text>'
        svg += f'<text x="15" y="{h/2}" text-anchor="middle" font-size="11" fill="#333" transform="rotate(-90,15,{h/2})">RSS (dBm)</text>'
        svg += f'<text x="{w/2}" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Wi-Fi Link: RSS vs Distance</text>'
        svg += f'<text x="{w-130}" y="{h-80}" font-size="9" fill="green">Valid Link</text>'
        svg += '</svg>'
        return svg

    def plot_fspl_frequencies():
        w, h = 500, 300
        x_min, x_max = 0.1, 100
        y_min, y_max = 50, 160
        freqs = [100, 900, 2400, 4000, 5800]
        freq_labels = ['100 MHz', '900 MHz', '2.4 GHz', '4 GHz', '5.8 GHz']
        colors = ['purple', 'red', 'blue', 'green', 'orange']
        svg = f'<svg width="{w}" height="{h}" style="border:1px solid #ccc;background:#fff;">'
        svg += '<rect width="100%" height="100%" fill="#fafafa"/>'
        for d in [0.1, 1, 10, 100]:
            x = map_x(d, x_min, x_max, w)
            svg += f'<line x1="{x}" y1="20" x2="{x}" y2="{h-40}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="{x}" y="{h-20}" text-anchor="middle" font-size="10" fill="#666">{d}</text>'
        for yv in [60, 80, 100, 120, 140, 160]:
            y = map_y(yv, y_min, y_max, h)
            svg += f'<line x1="60" y1="{y}" x2="{w-20}" y2="{y}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="50" y="{y+4}" text-anchor="end" font-size="10" fill="#666">{yv}</text>'
        for freq, label, color in zip(freqs, freq_labels, colors):
            fspl_vals = [20 * math.log10(d) + 20 * math.log10(freq) + 32.45 for d in distances]
            pts = []
            for d, fval in zip(distances, fspl_vals):
                if fval < y_min or fval > y_max:
                    continue
                x = map_x(d, x_min, x_max, w)
                y = map_y(fval, y_min, y_max, h)
                pts.append(f'{x:.1f},{y:.1f}')
            svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>'
        for i, (label, color) in enumerate(zip(freq_labels, colors)):
            y = 30 + i * 16
            svg += f'<line x1="{w-100}" y1="{y}" x2="{w-80}" y2="{y}" stroke="{color}" stroke-width="2"/>'
            svg += f'<text x="{w-75}" y="{y+4}" font-size="9" fill="#333">{label}</text>'
        svg += f'<text x="{w/2}" y="{h-5}" text-anchor="middle" font-size="11" fill="#333">Distance (km)</text>'
        svg += f'<text x="15" y="{h/2}" text-anchor="middle" font-size="11" fill="#333" transform="rotate(-90,15,{h/2})">FSPL (dB)</text>'
        svg += f'<text x="{w/2}" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">FSPL vs Distance at Various Frequencies</text>'
        svg += '</svg>'
        return svg

    def plot_link_margin():
        w, h = 500, 300
        x_min, x_max = 0.1, 100
        y_min, y_max = -40, 130
        wifi_margin = [r - (-82) for r in wifi_rss]
        cellular_margin = [r - (-102) for r in cellular_rss]
        satellite_margin = [r - (-120) for r in satellite_rss]
        svg = f'<svg width="{w}" height="{h}" style="border:1px solid #ccc;background:#fff;">'
        svg += '<rect width="100%" height="100%" fill="#fafafa"/>'
        for d in [0.1, 1, 10, 100]:
            x = map_x(d, x_min, x_max, w)
            svg += f'<line x1="{x}" y1="20" x2="{x}" y2="{h-40}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="{x}" y="{h-20}" text-anchor="middle" font-size="10" fill="#666">{d}</text>'
        for yv in [-40, -20, 0, 20, 40, 60, 80, 100, 120]:
            y = map_y(yv, y_min, y_max, h)
            svg += f'<line x1="60" y1="{y}" x2="{w-20}" y2="{y}" stroke="#ddd" stroke-width="1"/>'
            svg += f'<text x="50" y="{y+4}" text-anchor="end" font-size="10" fill="#666">{yv}</text>'
        y0 = map_y(0, y_min, y_max, h)
        svg += f'<line x1="60" y1="{y0}" x2="{w-20}" y2="{y0}" stroke="black" stroke-width="1"/>'
        def make_margin_path(dist_list, margin_list, color):
            pts = []
            for d, m in zip(dist_list, margin_list):
                if m < y_min or m > y_max:
                    continue
                x = map_x(d, x_min, x_max, w)
                y = map_y(m, y_min, y_max, h)
                pts.append(f'{x:.1f},{y:.1f}')
            return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>'
        svg += make_margin_path(distances, wifi_margin, 'blue')
        svg += make_margin_path(distances, cellular_margin, 'red')
        svg += make_margin_path(distances, satellite_margin, 'green')
        legend_items = [('Wi-Fi Margin', 'blue'), ('Cellular Margin', 'red'), ('Satellite Margin', 'green')]
        for i, (text, color) in enumerate(legend_items):
            y = 30 + i * 16
            svg += f'<line x1="{w-130}" y1="{y}" x2="{w-110}" y2="{y}" stroke="{color}" stroke-width="2"/>'
            svg += f'<text x="{w-105}" y="{y+4}" font-size="9" fill="#333">{text}</text>'
        svg += f'<text x="{w/2}" y="{h-5}" text-anchor="middle" font-size="11" fill="#333">Distance (km)</text>'
        svg += f'<text x="15" y="{h/2}" text-anchor="middle" font-size="11" fill="#333" transform="rotate(-90,15,{h/2})">Link Margin (dB)</text>'
        svg += f'<text x="{w/2}" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Link Margin vs Distance</text>'
        svg += '</svg>'
        return svg

    html_parts = []
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html><head><meta charset="UTF-8"><title>Link Budget Analysis</title>')
    html_parts.append('<style>')
    html_parts.append('body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 20px; }')
    html_parts.append('h1 { text-align: center; color: #333; }')
    html_parts.append('.graph-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px; }')
    html_parts.append('.graph-box { background: white; padding: 10px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }')
    html_parts.append('</style></head><body>')
    html_parts.append('<h1>Link Budget Analysis: Signal Strength vs Distance</h1>')
    html_parts.append('<div class="graph-container">')
    html_parts.append('<div class="graph-box">' + plot_rss_vs_distance() + '</div>')
    html_parts.append('<div class="graph-box">' + plot_wifi_zoom() + '</div>')
    html_parts.append('<div class="graph-box">' + plot_fspl_frequencies() + '</div>')
    html_parts.append('<div class="graph-box">' + plot_link_margin() + '</div>')
    html_parts.append('</div></body></html>')
    html = '\n'.join(html_parts)

    filename = 'link_budget_graphs.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\nGraphs saved to: {os.path.abspath(filename)}')
    print('Open this HTML file in any web browser to view the graphs.')


def sample_calculations():
    print('\n' + '#' * 70)
    print('# SAMPLE CALCULATION 1: Wi-Fi Link at 2.4 GHz')
    print('#' * 70)
    wifi_link = LinkBudgetCalculator(20.0, 2.0, 2.0, 1.0, 2400.0, 0.5)
    wifi_link.print_budget(receiver_sensitivity_dbm=-82.0)

    print('\n' + '#' * 70)
    print('# SAMPLE CALCULATION 2: Cellular Base Station at 900 MHz')
    print('#' * 70)
    cellular_link = LinkBudgetCalculator(43.0, 18.0, 0.0, 3.0, 900.0, 5.0)
    cellular_link.print_budget(receiver_sensitivity_dbm=-102.0)

    print('\n' + '#' * 70)
    print('# SAMPLE CALCULATION 3: Satellite Downlink at 4 GHz')
    print('#' * 70)
    satellite_link = LinkBudgetCalculator(30.0, 30.0, 25.0, 2.0, 4000.0, 36000.0)
    satellite_link.print_budget(receiver_sensitivity_dbm=-120.0)


if __name__ == '__main__':
    sample_calculations()
    generate_svg_graphs()
