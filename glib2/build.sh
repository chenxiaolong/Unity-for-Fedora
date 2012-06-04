#!/usr/bin/env bash

SPECFILE=glib2.spec
MULTILIB=true
MULTILIB_PACKAGES=('glib2' 'glib2-devel')
DO_NOT_INSTALL=('glib2-debuginfo' 'glib2-static')
# The maintainer of the Fedora glib2 package thinks that multilib devel packages
# are unnecessary and doesn't split off files in non-arch-dependent paths. This
# will only hurt users.
MULTILIB_DO_NOT_INSTALL=('glib2-devel')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
