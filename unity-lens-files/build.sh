#!/usr/bin/env bash

SPECFILE=unity-lens-files.spec
MULTILIB=false
DO_NOT_INSTALL=('unity-lens-files-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
