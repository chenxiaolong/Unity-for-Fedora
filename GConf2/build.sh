#!/usr/bin/env bash

SPECFILE=GConf2.spec
MULTILIB=true
MULTILIB_PACKAGES=('GConf2' 'GConf2-devel')
DO_NOT_INSTALL=('GConf2-debuginfo' 'GConf2-gtk')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
