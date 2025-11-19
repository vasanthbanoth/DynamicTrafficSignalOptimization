import xml.etree.ElementTree as ET

# Configuration parameters for traffic light update
NET_FILE = "ace1.net.xml"
REQUIREMENTS_FILE = "predicted_times.txt"
NET_OUTPUT_FILE = "updated.net.xml"
ROUTES_OUTPUT_FILE = "updated.rou.xml"
PARAMETERS_FILE = "sumo_parameters.txt"

def read_durations(req_file):
    """Read durations from input file and return as list of integers."""
    durations = []
    with open(req_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                durations.append(int(line))
            except ValueError:
                print(f"Skipping invalid duration: {line}")
    return durations

def repeat_durations(durations, repeat_count):
    """Repeat durations list specified number of times."""
    return durations * repeat_count

def update_tlogic_durations(net_filename, durations, tlogic_id="clusterJ7_clusterJ3_J5"):
    """Update traffic light durations in SUMO network file."""
    tree = ET.parse(net_filename)
    root = tree.getroot()
    
    if (tlLogic := root.find(f".//tlLogic[@id='{tlogic_id}']")) is None:
        raise ValueError(f"Traffic light logic '{tlogic_id}' not found")
    
    for phase in tlLogic.findall("phase"):
        if (old_dur := int(phase.get("duration"))) not in [120, 3] and durations:
            phase.set("duration", str(durations.pop(0)))
            print(f"Updated phase {old_dur} -> {phase.get('duration')}")
    
    return tree

def update_traffic_lights():
    """Main function for updating traffic light durations."""
    if not (base_durations := read_durations(REQUIREMENTS_FILE)):
        print("No valid durations found")
        return

    try:
        updated_tree = update_tlogic_durations(
            NET_FILE, 
            repeat_durations(base_durations, 3)
        )
        updated_tree.write(NET_OUTPUT_FILE, encoding="UTF-8", xml_declaration=True)
        print(f"Network file updated: {NET_OUTPUT_FILE}")
    except Exception as e:
        print(f"Traffic light update error: {e}")

def generate_routes():
    """Generate vehicle routes XML file from parameters."""
    try:
        with open(PARAMETERS_FILE, "r") as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        if len(numbers) != 4:
            raise ValueError("Exactly 4 numbers required in parameters file")
        
        num1, num2, num3, num4 = numbers
        
        routes_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <vType id="car" accel="2.6" decel="4.0" sigma="0.5" length="5.0" minGap="1.5" maxSpeed="70" color="0,1,1"/>
    <vType id="bus" accel="2.5" decel="4.0" sigma="0.5" length="6.0" minGap="1.5" maxSpeed="70" color="0,1,0"/>
    <vType id="truck" accel="2.5" decel="4.0" sigma="0.5" length="7" minGap="1" maxSpeed="70" color="1,1,0"/>
    
    <flow id="f_0" type="car" begin="0.00" from="E0" to="E2" end="90.00" number="{num1}"/>
    <flow id="f_1" type="bus" begin="0.00" from="E0" to="E0.156" end="90.00" number="{num1}"/>
    <flow id="f_2" type="DEFAULT_TAXITYPE" begin="0.00" from="-E1" to="-E00" end="90.00" number="{num2}"/>
    <flow id="f_3" type="car" begin="0.00" from="-E1" to="E2" end="90.00" number="{num2}"/>
    <flow id="f_4" type="bus" begin="0.00" from="-E0" to="E2" end="90.00" number="{num3}"/>
    <flow id="f_5" type="DEFAULT_TAXITYPE" begin="0.00" from="-E0" to="-E00" end="90.00" number="{num3}"/>
    <flow id="f_6" type="car" begin="0.00" from="-E2" to="-E00" end="90.00" number="{num4}"/>
    <flow id="f_7" type="bus" begin="0.00" from="-E2" to="E1" end="90.00" number="{num4}"/>
</routes>'''
        
        with open(ROUTES_OUTPUT_FILE, "w") as f:
            f.write(routes_xml)
            
        print(f"Routes file generated: {ROUTES_OUTPUT_FILE}")
    
    except Exception as e:
        print(f"Route generation error: {e}")

def main():
    """Main execution flow for combined operations."""
    print("=== Starting Traffic Light Update ===")
    update_traffic_lights()
    
    print("\n=== Starting Route Generation ===")
    generate_routes()
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()