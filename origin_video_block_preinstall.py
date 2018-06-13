import json
from shutil import copy2


# For npm install
package_file = '../../package.json'
# For testing
# package_file = 'package.json'

with open(package_file) as json_file:
    data = json.load(json_file)


###########################
# Add Dependencies to React Native project
###########################
print("\nAdding Dependencies to React Native Project")
# print("-------------------------------------------")

dependencies = data["dependencies"]
dependencies["origin-react-native-video-player"] = "git+ssh://git@github.com/turnercode/origin-video-block.git"
dependencies["mod-pbxproj"] = "git@github.com:noizetoys/mod-pbxproj.git"
data["dependencies"] = dependencies


##########################
# Add Pre and Post Install Scripts
##########################
print("\nAdding Pre and Post Install scripts")
# print("-----------------------------------")
scripts = data["scripts"]
scripts["preconfigure"] = "react-native link"
scripts["configure"] =  "python origin_video_block_postinstall.py"
scripts["postinstall"] = "npm run configure"


with open(package_file, 'w') as json_file:
    json.dump(data, json_file, indent=2)


##########################
# Move post_install script to project directory
##########################
file_to_copy ="origin_video_block_postinstall.py"  
print("\nCopying %s to project Directory" % file_to_copy)
# print("------------------------------------------------------------------")
copy2(file_to_copy, "../../" + file_to_copy)

print("\n\n------------------------------------------------------------------")
print("To complete installation of Video player, please type 'npm install'")
print("------------------------------------------------------------------\n\n")
