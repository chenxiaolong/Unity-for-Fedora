#!/usr/bin/env bash

SPECFILE=gnome-control-center-ubuntu.spec
MULTILIB=true
MULTILIB_PACKAGES=('gnome-control-center-ubuntu'
                   'gnome-control-center-ubuntu-devel')
DO_NOT_INSTALL=('gnome-control-center-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
