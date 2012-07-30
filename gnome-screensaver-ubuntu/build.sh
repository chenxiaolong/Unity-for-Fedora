#!/usr/bin/env bash

SPECFILE=gnome-screensaver-ubuntu.spec
MULTILIB=true
MULTILIB_PACKAGES=('gnome-screensaver-ubuntu')
DO_NOT_INSTALL=('gnome-screensaver-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
