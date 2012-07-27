#!/usr/bin/env bash

SPECFILE=frame.spec
MULTILIB=true
MULTILIB_PACKAGES=('frame' 'frame-devel')
DO_NOT_INSTALL=('frame-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
