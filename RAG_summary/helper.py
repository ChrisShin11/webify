import os
import json

def save_json_objects_as_text_files(json_data, output_dir):
    if json_data is None:
        raise ValueError('No documents available.')

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    key_list = []
    for key, value in json_data.items():
        name = value.get("name", f"entry_{key}").replace(" ", "_")  # Use name or fallback to entry_<key>
        file_path = os.path.join(output_dir, f"{name}.txt")
        
        key_list.append(name)
        # Convert JSON object to formatted string
        value_str = json.dumps(value, indent=4)
        
        # Write the string to a text file
        with open(file_path, 'w') as file:
            file.write(value_str)
        
        print(f"Saved {file_path}")
        
    return key_list

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)