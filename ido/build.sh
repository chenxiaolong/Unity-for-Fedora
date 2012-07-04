#!/usr/bin/env bash

SPECFILE=ido.spec
MULTILIB=true
MULTILIB_PACKAGES=('ido'  'ido-devel'
                   'ido3' 'ido3-devel')
DO_NOT_INSTALL=('ido-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
