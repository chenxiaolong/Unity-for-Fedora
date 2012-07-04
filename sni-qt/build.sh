#!/usr/bin/env bash

SPECFILE=sni-qt.spec
MULTILIB=true
MULTILIB_PACKAGES=('sni-qt')
DO_NOT_INSTALL=('sni-qt-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
