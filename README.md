# origin-config

## Prerequisites:
* React Native:
  * https://www.npmjs.com/package/react-native
  * https://facebook.github.io/react-native/docs/getting-started.html
* React Native CLI:
  * https://www.npmjs.com/package/react-native-cli
* npm:
  * https://www.npmjs.com/get-npm
* Python 2.7.xx:
  * *Should already be installed on you machine...*
  * https://www.python.org/downloads/
* you.i engine 4.7.xx (5.0 compatibilty forthcoming):
  * Talk to you Tech Lead



## Installation:

0. Open your favorite Terminal Emulator

1. Create a new React Native project
  * **`react-native init <App_Name>`**

2. Change directory into the newly created React Native project 
* **`cd <App_Name>`**

3. Install this module (origin-config)
 * **`npm install https://github.com/noizetoys/origin-config.git`**
 * ***Note:  You will need to enter your password.  The Python library used to edit the Xcode project needs access to install its dependencies***
  
4. Run the python script that moves everything around for you (magically)
* **`python $(npm bin)/update_ios_project`**
* ***Note:  You will need to drag-and-drop the folder containing the you.i engine on the Terminal window and press 'Enter'***

5. Have React Native resolve any symlinks, etc.
* **`react-native link`**

6. Open the project in Xcode
* **`open ../<App_Name>.xcodeproj`

7. Change the Swift Language Version
* Navigate to `Build Settings`
* Under `Swift Compiler - Language`, Select `Swift 4.1` under the Project icon
  
8. Build the iOS project
* **Press the `Run` button in Xcode


## Troubleshooting
