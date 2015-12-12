In order to generate Visual Studio projects, Meson needs to know the settings of your installed version of Visual Studio. The only way to get this information is to run Meson under the Visual Studio Command Prompt. The steps to set it up are as follows:

1. Click on start menu and select "Visual Studio Command Prompt"
1. cd into your source directory
1. mkdir build
1. python3 path/to/meson.py build --backend vs2010

If you wish to use the Ninja backend instead of vs2010, just leave out `--backend vs2010`. At the time of writing the Ninja backend is more mature than the VS backend so you might want to use it for serious work.

This assumes Python3 is in your <tt>PATH</tt>, which is highly recommended.