import json
from shutil import copy2


# For npm install
package_file = '../../package.json'
# For testing
# package_file = 'package.json'

with open(package_file) as json_file:
    data = json.load(json_file)
    # print(data)


###########################
# Add Dependencies to React Native project
###########################
print("\nAdding Dependencies to React Native Project")
dependencies = data["dependencies"]
dependencies["origin-react-native-video-player"] = "git+ssh://git@github.com/turnercode/origin-video-block.git"
dependencies["mod-pbxproj"] = "git@github.com:noizetoys/mod-pbxproj.git"
data["dependencies"] = dependencies
# print("Dependencies = %s" % data["dependencies"])


##########################
# Add Pre and Post Install Scripts
##########################
print("\nAdding Pre and Post Install scripts")
scripts = data["scripts"]
scripts["preconfigure"] = "react-native link"
scripts["configure"] =  "python origin_video_block_postinstall.py"
scripts["postinstall"] = "npm run configure"
# print("Scripts = %s" % data["scripts"])


with open(package_file, 'w') as json_file:
    json.dump(data, json_file, indent=2)


##########################
# Move post_install script to project directory
##########################
file_to_copy ="origin_video_block_postinstall.py"  
print("\nCopying %s to project Directory" % file_to_copy)
copy2(file_to_copy, "../../" + file_to_copy)


print("\n\nTo complete installation of Video player, please type 'npm install'\n\n")