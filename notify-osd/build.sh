#!/usr/bin/env bash

SPECFILE=notify-osd.spec
MULTILIB=false
DO_NOT_INSTALL=('notify-osd-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
