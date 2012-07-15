#!/usr/bin/env bash

SPECFILE=gnome-settings-daemon-ubuntu.spec
MULTILIB=true
MULTILIB_PACKAGES=('gnome-settings-daemon-ubuntu'
                   'gnome-settings-daemon-ubuntu-devel')
DO_NOT_INSTALL=('gnome-settings-daemon-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
