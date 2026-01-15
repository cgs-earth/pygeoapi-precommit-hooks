# hooks/cli_command.py
import sys
from pathlib import Path
import yaml

PASS = 0
FAIL = 1


def valid_yaml_with_links(config_path: str) -> bool:

    with open(config_path, "r") as f:
        try:
            pygeoapi_config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading pygeoapi config file: {e}")
            return False

    if "resources" not in pygeoapi_config:
        print("pygeoapi config file does not contain 'resources'")
        return False

    for resource in pygeoapi_config["resources"]:

        resource_block = pygeoapi_config["resources"][resource]
        if "links" not in resource_block:
            print(f"pygeoapi resource {resource} does not contain 'links'; each resource must have at least one link")
            return False
        
        foundDocumentationLink = False
        foundSourceLink = False

        for link in resource_block["links"]:
            if "href" not in link:
                print(
                    f"pygeoapi resource {resource_block['title']} link {link['rel']} does not contain 'href'"
                )
                return False
            if link["rel"] == "documentation":
                foundDocumentationLink = True
            if link["rel"] == "canonical":
                foundSourceLink = True

        if not foundDocumentationLink and not foundSourceLink:
            print(
                f"pygeoapi resource {resource_block['title']} does not contain 'documentation' or 'source' links"
            )
            return False

    return True

def main(mocked_config_path: str | None = None) -> int:
    """Validate that pygeoapi resources have proper links."""
    pygeoapi_config = sys.argv[1] if not mocked_config_path else mocked_config_path

    if not pygeoapi_config:
        print("No pygeoapi config file provided")
        return FAIL

    try: 
        config = Path(pygeoapi_config)
    except Exception as e:
        print(f"Error making path to pygeoapi config file: {e}")
        return FAIL

    if not config.exists():
        print(f"pygeoapi config file does not exist at {config.absolute()}")
        return FAIL

    return PASS if valid_yaml_with_links(pygeoapi_config) else FAIL


if __name__ == "__main__":
    raise SystemExit(main())
