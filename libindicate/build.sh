#!/usr/bin/env bash

SPECFILE=libindicate.spec
MULTILIB=true
MULTILIB_PACKAGES=('libindicate' 'libindicate-devel'
                   'libindicate-gtk3' 'libindicate-gtk3-devel'
                   'libindicate-gtk2' 'libindicate-gtk2-devel'
                   'libindicate-sharp-devel' 'libindicate-gtk2-sharp-devel')
DO_NOT_INSTALL=('libindicate-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
