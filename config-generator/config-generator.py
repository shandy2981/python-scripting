import argparse
import json
import yaml
import sys

def get_environment_details(environment):
    config = {}
    if environment == "development":
        config['database_url'] = input("Enter the development database URL: ")
        config['api_key'] = input("Enter the development API key: ")
    elif environment == "staging":
        config['database_url'] = input("Enter the staging database URL: ")
        config['api_key'] = input("Enter the staging API key: ")
    elif environment == "production":
        config['database_url'] = input("Enter the production database URL: ")
        config['api_key'] = input("Enter the production API key: ")
    else:
        print(f"Error: Unknown environment '{environment}'.")
        sys.exit(1)
    return config

def validate_input(environment, output_format):
    valid_environments = ["development", "staging", "production"]
    valid_formats = ["yaml", "json"]

    if environment not in valid_environments:
        print(f"Error: Invalid environment '{environment}'. Choose from: {', '.join(valid_environments)}.")
        sys.exit(1)
    
    if output_format not in valid_formats:
        print(f"Error: Invalid output format '{output_format}'. Choose from: yaml, json.")
        sys.exit(1)

def generate_config_file(config, output_format, output_path, dry_run):
    if output_format == "yaml":
        content = yaml.dump(config, default_flow_style=False)
    else:
        content = json.dumps(config, indent=4)

    if dry_run:
        print("Dry run enabled. The configuration file would be generated as follows:")
        print(content)
    else:
        with open(output_path, 'w') as file:
            file.write(content)
        print(f"Configuration file saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Configuration File Generator")

    parser.add_argument("environment", type=str, choices=["development", "staging", "production"],
                        help="The environment for which to generate the configuration file")
    parser.add_argument("output_format", type=str, choices=["yaml", "json"],
                        help="The output format of the configuration file (yaml or json)")
    parser.add_argument("output_path", type=str, help="The file path to save the configuration file")
    parser.add_argument("--dry-run", action="store_true", help="Show the output without saving the file")

    args = parser.parse_args()

    validate_input(args.environment, args.output_format)

    config = get_environment_details(args.environment)
    generate_config_file(config, args.output_format, args.output_path, args.dry_run)

if __name__ == "__main__":
    main()