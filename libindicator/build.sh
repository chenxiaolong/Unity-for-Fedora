#!/usr/bin/env bash

SPECFILE=libindicator.spec
MULTILIB=true
MULTILIB_PACKAGES=('libindicator'            'libindicator-devel'
                   'libindicator-tools'      'libindicator-gtk3'
                   'libindicator-gtk3-devel' 'libindicator-gtk3-tools')
DO_NOT_INSTALL=('libindicator-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
