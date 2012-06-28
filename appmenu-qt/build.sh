#!/usr/bin/env bash

SPECFILE=appmenu-qt.spec
MULTILIB=true
MULTILIB_PACKAGES=('appmenu-qt')
DO_NOT_INSTALL=('appmenu-qt-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
