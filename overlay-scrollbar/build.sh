#!/usr/bin/env bash

SPECFILE=overlay-scrollbar.spec
NO_BASE_PACKAGE=true
MULTILIB=true
MULTILIB_PACKAGES=('overlay-scrollbar-gtk2' 'overlay-scrollbar-gtk2-devel'
                   'overlay-scrollbar-gtk3' 'overlay-scrollbar-gtk3-devel')
DO_NOT_INSTALL=('overlay-scrollbar-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
