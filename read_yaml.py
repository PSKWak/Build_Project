import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Example usage
if __name__ == "__main__":
    file_path = "config.yaml"
    config = read_yaml(file_path)
    print(config)