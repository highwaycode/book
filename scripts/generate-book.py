import os.path
import re
import subprocess

file_list = """markdown/the-highway-code.md
markdown/the-highway-code/introduction.md
markdown/the-highway-code/rules-for-pedestrians-1-to-35.md
markdown/the-highway-code/rules-for-users-of-powered-wheelchairs-and-mobility-scooters-36-to-46.md
markdown/the-highway-code/rules-about-animals-47-to-58.md
markdown/the-highway-code/rules-for-cyclists-59-to-82.md
markdown/the-highway-code/rules-for-motorcyclists-83-to-88.md
markdown/the-highway-code/rules-for-drivers-and-motorcyclists-89-to-102.md
markdown/the-highway-code/general-rules-techniques-and-advice-for-all-drivers-and-riders-103-to-158.md
markdown/the-highway-code/using-the-road-159-to-203.md
markdown/the-highway-code/road-users-requiring-extra-care-204-to-225.md
markdown/the-highway-code/driving-in-adverse-weather-conditions-226-to-237.md
markdown/the-highway-code/waiting-and-parking-238-to-252.md
markdown/the-highway-code/motorways-253-to-273.md
markdown/the-highway-code/breakdowns-and-incidents-274-to-287.md
markdown/the-highway-code/road-works-level-crossings-and-tramways-288-to-307.md
markdown/the-highway-code/light-signals-controlling-traffic.md
markdown/the-highway-code/signals-to-other-road-users.md
markdown/the-highway-code/signals-by-authorised-persons.md
markdown/the-highway-code/traffic-signs.md
markdown/the-highway-code/road-markings.md
markdown/the-highway-code/vehicle-markings.md
markdown/the-highway-code/annex-1-you-and-your-bicycle.md
markdown/the-highway-code/annex-2-motorcycle-licence-requirements.md
markdown/the-highway-code/annex-3-motor-vehicle-documentation-and-learner-driver-requirements.md
markdown/the-highway-code/annex-4-the-road-user-and-the-law.md
markdown/the-highway-code/annex-5-penalties.md
markdown/the-highway-code/annex-6-vehicle-maintenance-safety-and-security.md
markdown/the-highway-code/annex-7-first-aid-on-the-road.md
markdown/the-highway-code/annex-8-safety-code-for-new-drivers.md
markdown/the-highway-code/other-information.md
markdown/the-highway-code/index.md"""
file_list = file_list.split("\n")
# print(file_list)

buffer = """<html>
<head>
<title>The Highway Code</title>
<meta name="author" content="bob">
</head>
<body>
"""

hrefs = set()

def mapped_href(match):
    hrefs.add(match.group(1))
    return "href='" + match.group(1) + "'"

for path in file_list:
    name = os.path.splitext(os.path.basename(path))[0]
    with open(path, 'r') as file:
        page = file.read()
        page = re.sub(r" id='section-title'", f" id='{name}'", page)
        page = re.sub(r"href='[^']*?\.md#", "href='#", page)
        page = re.sub(r"href='[^']*?([^/]*?)\.md'", "href='#\\1'", page)
        page = re.sub(r"href='#(\d+)'", "href='#rule\\1'", page)
        page = re.sub(r"href='#rule%20", "href='#rule", page)
        page = re.sub(r"href='#rule160%5D'", "href='#rule160'", page)
        page = re.sub(r"<h2 id='([^'])'>\n([^\n])\n</h2>", "<h3 id='\\1'>\\2</h3>", page)
        page = re.sub(r"href='([^']+)'", mapped_href, page)
        buffer += page

for href in sorted(hrefs):
    print(href)

# print(hrefs)

subprocess.run(['mkdir', '-p', 'build'])
with open('build/the-highway-code.html', 'w') as file:
    file.write(buffer)

subprocess.run(['pandoc', 'build/the-highway-code.html', '-o', 'build/the-highway-code.epub'])