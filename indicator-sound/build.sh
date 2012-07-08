#!/usr/bin/env bash

SPECFILE=indicator-sound.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-sound-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
