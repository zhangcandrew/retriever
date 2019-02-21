import requests
from retriever.lib.scripts import SCRIPT_LIST, get_script
from retriever.lib.defaults import SCRIPTS_REPOSITORY

def datasets(keywords=None, licenses=None):
    """Search all datasets by keywords and licenses."""
    script_list = SCRIPT_LIST()

    if not keywords and not licenses:
        return sorted(script_list, key=lambda s: s.name.lower())

    result_scripts = set()
    if licenses:
        licenses = [l.lower() for l in licenses]
    for script in script_list:
        if script.name:
            if licenses:
                script_license = [licence_map['name'].lower()
                                  for licence_map in script.licenses
                                  if licence_map['name']]
                if script_license and set(script_license).intersection(set(licenses)):
                    result_scripts.add(script)
                    continue
            if keywords:
                script_keywords = script.title + ' ' + script.name
                if script.keywords:
                    script_keywords = script_keywords + ' ' + '-'.join(script.keywords)
                script_keywords = script_keywords.lower()
                for k in keywords:
                    if script_keywords.find(k.lower()) != -1:
                        result_scripts.add(script)
                        break
    return sorted(list(result_scripts), key=lambda s: s.name.lower())


def dataset_names():
    """Return list of all available dataset names."""
    version_file = requests.get(SCRIPTS_REPOSITORY + "version.txt").text
    version_file = version_file.splitlines()[1:]
    scripts_name = []

    for line in version_file:
        filename = line.strip('\n').split(',')[0]
        clean_name = filename.split('.')[0].replace('_', '-')
        scripts_name.append(clean_name)

    return scripts_name


def license(dataset):
    """Get the license for a dataset."""
    return get_script(dataset).licenses[0]['name']


def dataset_licenses():
    """Return set with all available licenses."""
    license_values = [str(script.licenses[0]['name']).lower()
                      for script in SCRIPT_LIST()]
    return set(license_values)
