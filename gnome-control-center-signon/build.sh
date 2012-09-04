#!/usr/bin/env bash

SPECFILE=gnome-control-center-signon.spec
MULTILIB=true
MULTILIB_PACKAGES=('libaccount-plugin' 'libaccount-plugin-devel')
DO_NOT_INSTALL=('libaccount-plugin-debuginfo' 'libaccount-plugin-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
