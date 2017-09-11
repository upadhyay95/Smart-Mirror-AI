# Smart-Mirror-AI
Download the stable version of Node.js: https://nodejs.org/en/

Navigate inside the MagicMirror folder

cd MagicMirror
Install MagicMirror dependencies

sudo npm install
Verify it starts

npm start
Navigate out of the MagicMirror folder

cd ..
Clone this repository (AI Smart Mirror)


AI

Make sure Ruby is installed: https://www.ruby-lang.org/en/documentation/installation/

Install Homebrew: http://brew.sh/

Navigate to the AI-Smart-Mirror folder

cd AI-Smart-Mirror
Install ffmpeg

brew install ffmpeg
Use setup.sh to create a virtual environment and install dependencies

sudo ./setup.sh
Activate the virual evironment

source hhsmartmirror/bin/activate
Replace wit.ai and darksky.net tokens in the bot.py file

Make sure MagicMirror is running, then start the AI

python bot.py
Setup Facial Recognition

Refer to this guide: https://www.learnopencv.com/install-opencv-3-on-yosemite-osx-10-10-x/

Install openCV with

brew tap homebrew/science
brew install opencv
Open a new terminal tab with command+t

Check the version with

cd /usr/local/Cellar/opencv
ls
Return to the tab with AI-Smart-Mirror

Deactivate the virtual environment

deactivate
Navigate to the site-packages folder in the virtual environment

cd abhismartmirror/lib/python2.7/site-packages
Link the cv.py and cv2.so files and replace $VERSION with the version you found

ln -s /usr/local/Cellar/opencv/$VERSION/lib/python2.7/site-packages/cv.py cv.py
ln -s /usr/local/Cellar/opencv/$VERSION/lib/python2.7/site-packages/cv2.so cv2.s
Check that the files are there

ls
Return the the AI-Smart-Mirror directory

cd ../../../..
Reactivate the virtual evironment

source hhsmartmirror/bin/activate
Start the app

python bot.py
