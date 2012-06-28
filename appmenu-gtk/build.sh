#!/usr/bin/env bash

SPECFILE=appmenu-gtk.spec
NO_BASE_PACKAGE=true
MULTILIB=true
MULTILIB_PACKAGES=('appmenu-gtk2' 'appmenu-gtk3')
DO_NOT_INSTALL=('appmenu-gtk-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
