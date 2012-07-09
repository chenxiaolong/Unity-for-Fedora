#!/usr/bin/env bash

SPECFILE=unity-lens-music.spec
MULTILIB=false
DO_NOT_INSTALL=('unity-lens-music-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
