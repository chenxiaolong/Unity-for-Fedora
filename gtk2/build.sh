#!/usr/bin/env bash

SPECFILE=gtk2.spec
MULTILIB=true
MULTILIB_PACKAGES=('gtk2' 'gtk2-devel' 'gtk2-immodule-xim' 'gtk2-immodules')
DO_NOT_INSTALL=('gtk2-debuginfo' 'gtk2-devel-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
