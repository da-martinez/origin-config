import os
import cmd
import sys
from shutil import copy2
from distutils.dir_util import copy_tree
sys.path.insert(0, './mod-pbxproj')
from pbxproj import XcodeProject
from pbxproj.pbxextensions import FileOptions


##########################
# If delivered in an npm module
##########################
# module_path = os.getcwd()
# print("Module Path = %s" % module_path)
# module_parts = module_path.split('/')
# print("Module Parts = %s" % module_parts)
# project_path_minus_node_module = module_parts[:len(module_parts)-2]
# print("Project Path without Module Parts = %s" % project_path_minus_node_module)
# project_path = '/'.join(project_path_minus_node_module)
# End NPM adjustment


##########################
# If NOT delivered in an npm module
##########################
project_path = os.getcwd()


##########################
# Non-location relative code
##########################
 
# print("Project Path = %s" % project_path)
path_array = project_path.split('/')
# print("Path name = ", path_array)
project_name = path_array[-1]
print("\n\n------------------------------------------")
print("Project Name = %s" % project_name)
print("------------------------------------------")
dummy_project_path = '/ios/project_name.xcodeproj/project.pbxproj'
path_to_xcode_project = dummy_project_path.replace("project_name", project_name)
# print("Path to Xcode Project = %s" % path_to_xcode_project)
full_path = project_path + path_to_xcode_project
# print("Full Path = %s" % full_path)
ios_project_path = project_path + '/ios/'
# print("ios_project_path = %s" % ios_project_path)


##########################
# create symlink to 'youiengine' folder
##########################
symlink_path = project_path + '/youiengine'
print(symlink_path)
if os.path.exists(symlink_path):
    os.unlink(symlink_path)


# Create Symlink to youiengine.
input_string = '\n\nWhere is the you.i engine located?' \
'\n----------------------------------\n' \
'\nDrag-and-Drop the folder containing the you.i engine here, then press "Enter" ->  '
 
engine_source = raw_input(input_string)
symlink_command = 'ln -s ' + engine_source + ' youiengine'
os.system(symlink_command)
print("\nyouiengine symlink created to '%s'" % engine_source)


# Create project to manipulate
project = XcodeProject.load(full_path)

# Back up the file just in case
project_back_up = project.backup()
print("\nOriginal Project backed up to '%s'" % project_back_up)


##########################
# Add Frameworks from origin-player-block example
##########################
embedded_framework_path = '/node_modules/origin-react-native-video-player/example/ios/FILE_NAME'
full_embedded_path = project_path + embedded_framework_path


##########################
# Turner (TOP) Related frameworks
# EMBEDDED
# Source: <Project_Path>/node_modules/origin-react-native-video-player/example/ios/...
##########################
turner_frameworks = ['AccessEnabler.framework', 'TurnerAdKit.framework', 'TurnerPlayerKit.framework']

print("\n\nAdding Turner Frameworks:")
print("-------------------------")

for framework in turner_frameworks:
    print("Adding:  %s" % framework)
    framework_path = full_embedded_path.replace('FILE_NAME', framework)
    target_path = ios_project_path + framework
    # copy file to local directory
    copy_tree(framework_path, target_path)
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=True)
    blah = project.add_file(target_path, parent=frameworks, target_name=project_name, file_options=file_options)


##########################
# AdManager.framework
# NOT EMBEDDED
# Source: <Project_Path>/node_modules/origin-react-native-video-player/example/ios/...
##########################
ad_manager = 'AdManager.framework'
print("Adding:  %s" % ad_manager)

framework_path = full_embedded_path.replace('FILE_NAME', ad_manager)
target_path = ios_project_path + ad_manager
# copy file to local directory
copy_tree(framework_path, target_path)
frameworks = project.get_or_create_group('Frameworks')
file_options = FileOptions(embed_framework=False)
blah = project.add_file(target_path, parent=frameworks, target_name=project_name, file_options=file_options)


##########################
# Auth Services framework
# Embedded
# Source: <Project_Path>/node_modules/origin-react-native-video-player/ios/libAuthServices_3.5.2.a
##########################
auth_services = project_path + '/node_modules/origin-react-native-video-player/ios/libAuthServices_3.5.2.a'
print("Adding:  libAuthServices_3.5.2.a")
frameworks = project.get_or_create_group('Frameworks')
file_options = FileOptions(embed_framework=False)
blah = project.add_file(auth_services, parent=frameworks, target_name=project_name, file_options=file_options)


##########################
# Copy into project
# Source: <Project_Path>/node_modules/origin-react-native-video-player/example/ios
##########################
app_factory_files = ['AppFactory.cpp', 'AppFactory.h']

print("\n\nCopying files:")
print("--------------")

for file_to_copy in app_factory_files:
    print("Copying:  %s" % file_to_copy)
    file_path = full_embedded_path.replace('FILE_NAME', file_to_copy)
    target_path = ios_project_path + file_to_copy
    # copy file to local directory
    copy2(file_path, target_path)
    blah = project.add_file(target_path, target_name=project_name)
 

##########################
# 'dummy.swift' & '<Project_Name>_Bridging_Header.h
# Empty files created for Swift Briding purposes
##########################
print("\n\nCreating and Adding files to Xcode:")
print("-----------------------------------")
dummy_swift_file_path = ios_project_path + 'dummy.swift'
bridging_header_file = project_name + '_Bridging_Header.h'
bridging_header_path = ios_project_path + bridging_header_file
print("Adding file:  dummy.swift")
print("Adding file:  %s" % bridging_header_file)

# Create swift file
swift_file = open(dummy_swift_file_path, 'w')
swift_file.write("//\n//  dummy.swift\n//  %s\n//\n\nimport Foundation" % project_name)
swift_file.close()

# Create bridging header
bridging_header_file = open(bridging_header_path, 'w')
bridging_header_file.write("//\n//  Use this file to import your target's public headers that you would like to expose to Swift.\n//")
bridging_header_file.close()

project.add_file(dummy_swift_file_path, force=False, target_name=project_name)
project.add_file(bridging_header_path, force=False, target_name=project_name)


##########################
# Add System FrameWorks
##########################
apple_frameworks = [
    'AVFoundation.framework',
    'CoreAudio.framework',
    'CoreGraphics.framework',
    'CoreImage.framework',
    'CoreLocation.framework',
    'CoreMedia.framework',
    'EventKit.framework',
    'GLKit.framework',
    'MediaPlayer.framework',
    'MessageUI.framework',
    'WebKit.framework'
]

system_frameworks_path = '/System/Library/Frameworks/'

print("\n\nAdding Apple Frameworks:")
print("------------------------")

for framework in apple_frameworks: 
    print("Adding:  %s" % framework)
    apple_path = system_frameworks_path + framework
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=False, weak=True)
    blah = project.add_file(apple_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)


##########################
# Apple Framework located in different Directory
##########################
ad_support_framework_path = '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks/AdSupport.framework'
print("Adding:  AdSupport.framework")
frameworks = project.get_or_create_group('Frameworks')
file_options = FileOptions(embed_framework=False, weak=True)
blah = project.add_file(ad_support_framework_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)


##########################
# Add you.i frameworks
##########################
youi_frameworks = [
    'libcrypto.a',
    'libfreetype.a',
    'libicudata.a',
    'libicui18n.a',
    'libicule.a' ,
    'libiculx.a',
    'libicuuc.a',
    'libjpeg.a',
    'libpng.a',
    'libprotobuf.a',
    'libssl.a',
    'libwebp.a',
    'libyouiengine.a',
    'libz.a'
]

##########################
# <youi_engine_symlink>/libs/ios/Debug/
##########################
youi_library_path = project_path + '/youiengine/libs/ios/Debug/' 

print("\n\nAdding you.i frameworks:")
print("------------------------")

for framework in youi_frameworks: 
    print("Adding:  %s" % framework)
    youi_framework_path = youi_library_path + framework
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=False, weak=True)
    blah = project.add_file(youi_framework_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)


##########################
# Change Header Search paths
##########################
youi_base_path = '${PROJECT_DIR}/../youiengine/include/'
video_player_path = '${SRCROOT}/../node_modules/origin-react-native-video-player/ios'
youi_sdks = youi_base_path + 'sdk'
youi_thirdparty_sdks = youi_base_path + 'thirdparty/ios'
print("\n\nUpdating Header Search Paths with:")
print("----------------------------------")
print("%s\n%s\n%s" % (video_player_path, youi_sdks, youi_thirdparty_sdks))
project.add_header_search_paths([video_player_path, youi_sdks, youi_thirdparty_sdks], recursive=True, target_name=project_name)


##########################
# Change Framework Search paths
##########################
project.add_framework_search_paths('${PROJECT_DIR}', recursive=True)
print("\n\nUpdating Framework Search Paths with:")
print("-------------------------------------")
print("${PROJECT_DIR}\n\n") 


##########################
# Required
##########################
project.save()
