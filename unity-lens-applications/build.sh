#!/usr/bin/env bash

SPECFILE=unity-lens-applications.spec
MULTILIB=false
DO_NOT_INSTALL=('unity-lens-applications-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
