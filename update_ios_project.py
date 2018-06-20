import os
import sys
from shutil import copy2
import subprocess
from distutils.dir_util import copy_tree
from pbxproj import XcodeProject
from pbxproj.pbxextensions import FileOptions

def get_module_path(module_path):
    try:
        module_path = subprocess.check_output("npm ls %s --parseable" % module_path, shell=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

    return module_path.split('\n')[0]


def create_symlink(project_path):
    symlink_path = os.path.join(project_path, 'youiengine')
    print symlink_path
    print("symlink_path = %s" % symlink_path)

    if os.path.exists(symlink_path):
        print "sysmlink exists"
        os.unlink(symlink_path)

    # Create Symlink to youiengine.
    input_string = '\n\nWhere is the you.i engine located?' \
                   '\n----------------------------------\n' \
                   '\nDrag-and-Drop the folder containing the you.i engine here, then press "Enter" ->  '

    engine_source = raw_input(input_string)
    symlink_command = "ln -s %(engine_source)s %(symlink_path)s" % locals()
    os.system(symlink_command)
    print("\nyouiengine symlink created to '%s'" % engine_source)

##########################
# If NOT delivered in an npm module
##########################
try:
    root_path = subprocess.check_output("npm root", shell=True, stderr=subprocess.STDOUT).strip()
except subprocess.CalledProcessError as e:
    raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

print("root_path = %s" % root_path)

project_path, _ = os.path.split(root_path)
print("project_path = %s" % project_path)

_, project_name = os.path.split(project_path)
print("project_name = %s" % project_name)

path_to_xcode_project = "ios/%s.xcodeproj/project.pbxproj" % project_name
print("path_to_xcode_project = %s" % path_to_xcode_project)

full_path = os.path.join(project_path, path_to_xcode_project)
print("full_path = %s" % full_path)

ios_project_path = os.path.join(project_path, 'ios')
print("ios_project_path = %s" % ios_project_path)


##########################
# create symlink to 'youiengine' folder
##########################

create_symlink(project_path)


# Create project to manipulate
project = XcodeProject.load(full_path)

# Back up the file just in case
project_back_up = project.backup()
print("Original Project backed up to '%s'" % project_back_up)


##########################
# Add Frameworks from origin-player-block example
##########################
origin_player_path = get_module_path("origin-react-native-video-player")
full_embedded_path = os.path.join(origin_player_path, 'example/ios')

print "origin_player_path = %s" % origin_player_path
print "full_embedded_path = %s" % full_embedded_path


##########################
# Turner (TOP) Related frameworks
# EMBEDDED
# Source: <Project_Path>/node_modules/origin-react-native-video-player/example/ios/...
##########################

# Name Framwork: Embedded
turner_frameworks = {'AccessEnabler.framework': True,
                     'TurnerAdKit.framework' : True,
                     'TurnerPlayerKit.framework': True,
                     'AdManager.framework': False}

print("\n\nAdding Turner Frameworks:")
print("-------------------------")

for framework, embed in turner_frameworks.iteritems():
    print("Adding:  %s" % framework)
    framework_path = os.path.join(full_embedded_path, framework)
    target_path = os.path.join(ios_project_path, framework)
    print "framework_path = %s" % framework_path
    print "target_path = %s" % target_path
    copy_tree(framework_path, target_path)
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=embed)
    blah = project.add_file(target_path, parent=frameworks, target_name=project_name, file_options=file_options)


##########################
# Auth Services framework
# Embedded
# Source: <Project_Path>/node_modules/origin-react-native-video-player/ios/libAuthServices_3.5.2.a
##########################
full_blocks_path = os.path.join(origin_player_path, 'ios/')

turner_blocks = {'libAuthServices_3.5.2.a': False}

for block, embed in turner_blocks.iteritems():
    block_path = os.path.join(full_blocks_path, block)
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=embed)
    blah = project.add_file(block_path, parent=frameworks, target_name=project_name, file_options=file_options)
    print "block_path = %s" % block_path


##########################
# Copy into project
# Source: <Project_Path>/node_modules/origin-react-native-video-player/example/ios
##########################
app_factory_files = ['AppFactory.cpp', 'AppFactory.h']

print("\n\nCopying files:")
print("--------------")

for file_to_copy in app_factory_files:
    print("Copying:  %s" % file_to_copy)
    file_path = os.path.join(full_embedded_path, file_to_copy)
    target_path = os.path.join(ios_project_path, file_to_copy)
    print "file_path = %s" % file_path
    print "target_path = %s" % target_path
    copy2(file_path, target_path)
    blah = project.add_file(target_path, target_name=project_name)

##########################
# 'dummy.swift' & '<Project_Name>_Bridging_Header.h
# Empty files created for Swift Briding purposes
##########################
print("\n\nCreating and Adding files to Xcode:")
print("-----------------------------------")
dummy_swift_file_path = os.path.join(ios_project_path, 'dummy.swift')
bridging_header_file = os.path.join(project_name, '_Bridging_Header.h')
bridging_header_path = os.path.join(ios_project_path, bridging_header_file)
print dummy_swift_file_path, bridging_header_file, bridging_header_path
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
    'WebKit.framework'
]

system_frameworks_path = '/System/Library/Frameworks/'

print("\n\nAdding Apple Frameworks:")
print("------------------------")

for framework in apple_frameworks:
    print("Adding:  %s" % framework)
    apple_path = os.path.join(system_frameworks_path, framework)
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=False, weak=True)
    blah = project.add_file(apple_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)

##########################
# Apple Framework located in different Directory
##########################
other_frameworks = ['AdSupport.framework',
                    'MessageUI.framework']

other_framework_path = '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks/'

for other_framework in other_frameworks:
    print "Adding: %s" % framework
    frameworks = project.get_or_create_group('Frameworks')
    framework_path = os.path.join(other_framework_path, other_framework)
    file_options = FileOptions(embed_framework=False, weak=True)
    blah = project.add_file(framework_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)

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
youi_library_path = os.path.join(project_path, 'youiengine/libs/ios/Debug/')
print "youi_library_path = %s" % youi_library_path

print("\n\nAdding you.i frameworks:")
print("------------------------")

for framework in youi_frameworks: 
    print("Adding:  %s" % framework)
    youi_framework_path = os.path.join(youi_library_path, framework)
    print "youi_framework_path = %s" % youi_framework_path
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=False, weak=False)
    blah = project.add_file(youi_framework_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)



other_libraries = ['libxml2.2.tbd']
other_library_path = '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/usr/lib'

for lib in other_libraries:
    print("Adding:  %s" % lib)
    lib_path = os.path.join(other_library_path, lib)
    print "lib_path = %s" % lib_path
    frameworks = project.get_or_create_group('Frameworks')
    file_options = FileOptions(embed_framework=False, weak=False)
    blah = project.add_file(lib_path, parent=frameworks, tree='SDKROOT', target_name=project_name, file_options=file_options)


##########################
# Change Header Search paths
##########################
youi_base_path = '${PROJECT_DIR}/../youiengine/include/'
video_player_path = '${SRCROOT}/../node_modules/origin-react-native-video-player/ios/'
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

project.add_library_search_paths('${PROJECT_DIR}/../youiengine/libs/ios', recursive=True)

print("-------------------------------------")
print "\nAdd RCTVideo project to Library"
print("-------------------------------------")
rct_video_file = 'origin-react-native-video-player/ios/RCTVideo.xcodeproj'
rct_video_path = os.path.join(root_path, rct_video_file)
print "rct_video_path = %s" % rct_video_path
libraries = project.get_or_create_group('Libraries')
blah = project.add_project(rct_video_path, parent=libraries, tree='SDKROOT', target_name=project_name)


##########################
# Set Swift Language Version Flag to 4.1
##########################





##########################
# Required
##########################
project.save()

