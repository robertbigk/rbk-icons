# Convert SVG icons to JS format for HomeAssistant
import os
import re
import shutil
from pathlib import Path
from xml.dom import Node
from xml.dom.minidom import parseString

# Konfiguracja
ICONS_PREFIX = "rbk"  # Prefix dla ikon w Home Assistant
CLEAN_ORIGINAL_SVG = True  # Ustaw True aby usunąć oryginalne SVG po konwersji
CLEAN_CONVERTED_FOLDER = False  # Ustaw True aby wyczyścić folder converted przed konwersją

def clean_svg(svg_content):
    """Remove empty or irrelevant elements from SVG"""
    svg_content = re.sub(r'<style[^>]*>(\s*)</style>', '', svg_content)
    svg_content = re.sub(r'<defs[^>]*>(\s*)</defs>', '', svg_content)
    svg_content = re.sub(r'<title>[^<]*</title>', '', svg_content)
    svg_content = re.sub(r'<desc>[^<]*</desc>', '', svg_content)
    svg_content = re.sub(r'<!--.*?-->', '', svg_content, flags=re.DOTALL)
    return svg_content

def circle_to_path(circle):
    cx = float(circle.getAttribute('cx') or 0)
    cy = float(circle.getAttribute('cy') or 0)
    r = float(circle.getAttribute('r'))
    return f"M {cx - r}, {cy} a {r},{r} 0 1,0 {r * 2},0 a {r},{r} 0 1,0 -{r * 2},0"

def polygon_to_path(polygon):
    points = polygon.getAttribute('points').strip()
    return f"M{points}z"

def polyline_to_path(polyline):
    points = polyline.getAttribute('points').strip()
    return f"M{points}"

def rect_to_path(rect):
    x = float(rect.getAttribute('x') or 0)
    y = float(rect.getAttribute('y') or 0)
    w = float(rect.getAttribute('width'))
    h = float(rect.getAttribute('height'))
    rx = rect.getAttribute('rx')
    rx = float(rx) if rx else 0
    ry = rect.getAttribute('ry')
    ry = float(ry) if ry else rx
    
    if rx == 0 and ry == 0:
        return f"M{x},{y} h{w} v{h} h{-w} z"
    else:
        return (f"M{x+rx},{y} h{w-2*rx} "
                f"a{rx},{ry} 0 0 1 {rx},{ry} "
                f"v{h-2*ry} "
                f"a{rx},{ry} 0 0 1 {-rx},{ry} "
                f"h{-w+2*rx} "
                f"a{rx},{ry} 0 0 1 {-rx},{-ry} "
                f"v{-h+2*ry} "
                f"a{rx},{ry} 0 0 1 {rx},{-ry} z")

def ellipse_to_path(ellipse):
    cx = float(ellipse.getAttribute('cx') or 0)
    cy = float(ellipse.getAttribute('cy') or 0)
    rx = float(ellipse.getAttribute('rx'))
    ry = float(ellipse.getAttribute('ry'))
    return (f"M{cx+rx},{cy} "
            f"A{rx},{ry} 0 0 1 {cx},{cy+ry} "
            f"A{rx},{ry} 0 0 1 {cx-rx},{cy} "
            f"A{rx},{ry} 0 0 1 {cx+rx},{cy} z")

def process_group(group):
    """Process <g> elements and their children"""
    data = ""
    
    for node in group.childNodes:
        if node.nodeType != Node.ELEMENT_NODE:
            continue
            
        node_name = node.nodeName
        if node_name == "path":
            data += node.getAttribute('d') + " "
        elif node_name == "circle":
            data += circle_to_path(node) + " "
        elif node_name == "polygon":
            data += polygon_to_path(node) + " "
        elif node_name == "polyline":
            data += polyline_to_path(node) + " "
        elif node_name == "rect":
            data += rect_to_path(node) + " "
        elif node_name == "ellipse":
            data += ellipse_to_path(node) + " "
        elif node_name == "g":
            data += process_group(node) + " "
    
    return data

# Główna funkcja konwersji
def convert_svg_to_js():
    # Utwórz folder converted jeśli nie istnieje
    converted_dir = os.path.join("icon-svg", "converted")
    os.makedirs(converted_dir, exist_ok=True)
    
    # Wyczyść folder converted jeśli wymagane
    if CLEAN_CONVERTED_FOLDER:
        for file in os.listdir(converted_dir):
            file_path = os.path.join(converted_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    # Rozpocznij plik JS
    with open("custom-icons.js", 'w', encoding='utf-8') as js:
        js.write("var icons = {\n")

        # Przetwórz wszystkie ikony w folderze icon-svg
        for filename in sorted(os.listdir("icon-svg")):
            if filename.startswith('.') or not filename.lower().endswith('.svg'):
                continue
                
            icon_path = os.path.join("icon-svg", filename)
            if not os.path.isfile(icon_path):
                continue
                
            try:
                # Wczytaj i wyczyść SVG
                with open(icon_path, 'r', encoding='utf-8') as f:
                    svg = clean_svg(f.read())
                
                # Parsuj SVG jako XML
                xml = parseString(svg)
                svg_element = xml.getElementsByTagName("svg")[0]
                
                # Pobierz viewBox
                viewbox = svg_element.getAttribute('viewBox')
                if not viewbox:
                    width = svg_element.getAttribute('width') or '24'
                    height = svg_element.getAttribute('height') or '24'
                    viewbox = f"0 0 {width} {height}"
                
                # Podziel viewBox
                vb_parts = viewbox.split()
                if len(vb_parts) < 4:
                    vb_parts = ['0', '0', '24', '24']
                
                # Konwertuj na floaty
                try:
                    vb_floats = [float(vb_parts[0]), float(vb_parts[1]), float(vb_parts[2]), float(vb_parts[3])]
                except:
                    vb_floats = [0, 0, 24, 24]
                
                # Przetwórz wszystkie elementy
                data = ""
                for node in svg_element.childNodes:
                    if node.nodeType != Node.ELEMENT_NODE:
                        continue
                        
                    node_name = node.nodeName
                    if node_name == "path":
                        data += node.getAttribute('d') + " "
                    elif node_name == "circle":
                        data += circle_to_path(node) + " "
                    elif node_name == "polygon":
                        data += polygon_to_path(node) + " "
                    elif node_name == "polyline":
                        data += polyline_to_path(node) + " "
                    elif node_name == "rect":
                        data += rect_to_path(node) + " "
                    elif node_name == "ellipse":
                        data += ellipse_to_path(node) + " "
                    elif node_name == "g":
                        data += process_group(node) + " "
                
                # Oczyść dane ścieżki
                data = re.sub(r'\s+', ' ', data).strip()
                
                # Zapisz do JS
                icon_name = Path(filename).stem
                js.write(f'  "{icon_name}":[{vb_floats[0]},{vb_floats[1]},{vb_floats[2]},{vb_floats[3]},"{data}"],\n')
                
                # Utwórz testowe SVG
                with open(os.path.join(converted_dir, filename), 'w', encoding='utf-8') as test_svg:
                    test_svg.write(f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg"><path d="{data}"/></svg>')
                
                # Usuń oryginał jeśli wymagane
                if CLEAN_ORIGINAL_SVG:
                    os.remove(icon_path)
                    print(f"Usunięto oryginalny plik: {icon_path}")
                    
            except Exception as e:
                print(f"Błąd przetwarzania {filename}: {str(e)}")

        # Zakończ plik JS
        js.write("""};

async function getIcon(name) {
  if (!(name in icons)) {
    console.log(`Icon "${name}" not available`);
    return '';
  }

  var svgDef = icons[name];
  return {
    path: svgDef[4],
    viewBox: `${svgDef[0]} ${svgDef[1]} ${svgDef[2]} ${svgDef[3]}`
  };
}

async function getIconList() {
  return Object.keys(icons).map(name => ({ name }));
}

window.customIconsets = window.customIconsets || {};
window.customIconsets["rbk"] = getIcon;

window.customIcons = window.customIcons || {};
window.customIcons["rbk"] = { getIcon, getIconList };
""")

    print("Konwersja zakończona pomyślnie!")

# Uruchom konwersję
if __name__ == "__main__":
    convert_svg_to_js()