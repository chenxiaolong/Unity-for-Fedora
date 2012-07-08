#!/usr/bin/env bash

SPECFILE=gnome-menus301.spec
MULTILIB=true
MULTILIB_PACKAGES=('gnome-menus301' 'gnome-menus301-devel')
DO_NOT_INSTALL=('gnome-menus301-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
