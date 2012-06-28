#!/usr/bin/env bash

SPECFILE=libappindicator.spec
MULTILIB=true
MULTILIB_PACKAGES=('libappindicator'             'libappindicator-devel'
                   'libappindicator-gtk3'        'libappindicator-gtk3-devel'
                   'libappindicator-sharp-devel')
DO_NOT_INSTALL=('libappindicator-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
