
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
markdown/the-highway-code/index.md
markdown/the-highway-code/updates.md"""
file_list = file_list.split("\n")
print(file_list)

buffer = ""
for path in file_list:
    with open(path, 'r') as file:
        buffer += file.read()

subprocess.run(['mkdir', '-p', 'build'])
with open('build/book.html', 'w') as file:
    file.write(buffer)

subprocess.run(['pandoc', 'build/book.html', '-o', 'build/book.pdf'])