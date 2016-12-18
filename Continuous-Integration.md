Here you will find snippets to use Meson with various CI such as Travis and Appveyor.

Please [file an issue](https://github.com/mesonbuild/meson/issues/new) if these instructions don't work for you.

## Travis for OS X and Linux (with Docker)

Travis for Linux provides ancient versions of Ubuntu which will likely cause problems building your projects regardless of which build system you're using. We recommend using Docker to get a more-recent version of Ubuntu and installing Ninja, Python3, and Meson inside it.

This `yml` file is derived from the [configuration used by Meson for running its own tests](https://github.com/mesonbuild/meson/blob/master/.travis.yml).

```
sudo: false

os:
  - linux
  - osx

language:
  - cpp

services:
  - docker

before_install:
  - if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then brew update; fi
  - if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then brew install ninja python3; fi
  - if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then pip3 install meson; fi
  - if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then docker pull YOUR/REPO:yakkety; fi

script:
  - if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then echo FROM YOUR/REPO:yakkety > Dockerfile; fi
  - if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then echo ADD . /root >> Dockerfile; fi
  - if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then docker build -t withgit .; fi
  - if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then docker run withgit /bin/sh -c "cd /root && TRAVIS=true CC=$CC CXX=$CXX meson build && ninja -C build test"; fi
  - if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then SDKROOT=$(xcodebuild -version -sdk macosx Path) meson build && ninja -C build test; fi
```