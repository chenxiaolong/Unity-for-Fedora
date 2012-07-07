#!/usr/bin/env bash

SPECFILE=gtk2-ubuntu.spec
MULTILIB=true
MULTILIB_PACKAGES=('gtk2-ubuntu' 'gtk2-ubuntu-devel' 'gtk2-ubuntu-immodule-xim'
                   'gtk2-ubuntu-immodules')
DO_NOT_INSTALL=('gtk2-ubuntu-debuginfo' 'gtk2-ubuntu-devel-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
