#!/usr/bin/env bash

SPECFILE=gsettings-desktop-schemas-ubuntu.spec
MULTILIB=true
MULTILIB_PACKAGES=('gsettings-desktop-schemas-ubuntu'
                   'gsettings-desktop-schemas-ubuntu-devel')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
