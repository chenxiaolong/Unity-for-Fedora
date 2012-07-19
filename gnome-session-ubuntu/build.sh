#!/usr/bin/env bash

SPECFILE=gnome-session-ubuntu.spec
MULTILIB=false
DO_NOT_INSTALL=('gnome-session-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
