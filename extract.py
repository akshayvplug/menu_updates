import xml.etree.ElementTree as ET
import json
import html

# Parse the XML
def parse_xml(filename, store_id):
    tree = ET.parse(filename)
    # Parse the XML data
    root = tree.getroot()
    # Initialize a list to store the extracted data
    result = []

    # Define a helper function to recursively extract products and options
    def extract_data(element, product_name=""):
        if element.tag in ['product', 'option']:
            if element.tag == "option":
                is_modifier = True
            else:
                is_modifier = False
                product_name = element.get('name', '')

            item = {
                'id': element.get('id', ''),
                'chain_id': element.get("chainid" if is_modifier else "chainproductid"),
                'is_modifier': 1 if is_modifier else 0,
                'name': (element.get('name', '')).replace('\"', '').replace('\u00ae','').replace("'", ""),
                'is_available': 1,
                'product_name': product_name  # Add product_name to the extracted data
            }
            result.append(item)

        for child in element:
            extract_data(child, product_name)

    # Start the extraction process
    extract_data(root)

    with open('data.json', 'w') as f:
        json.dump(result, f)

    return result


# parse_xml('menu_files/6155.xml', 6155)