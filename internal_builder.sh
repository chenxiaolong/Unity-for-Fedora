#!/usr/bin/env bash

#echo "Querying spec file..."

GENERATED_RPMS=$(rpmspec -q --rpms ${SPECFILE})
GENERATED_SRPM=$(rpmspec -q --srpm ${SPECFILE})
FEDORA_VER="$(grep '%fedora' /etc/rpm/macros.dist | awk '{print $2}')"

##########################
# BEGIN: General options #
##########################
create_dirs() {
  # Create a directory structure simitlar to Arch Linux's PKGBUILD build
  # directory structure. This allow all the needed files to be contained
  # in a single directory, which prevents having duplicate copies of files
  # and allow the directories to be cleaned up easily.

  for i in BUILD PACKAGES; do
    if [ ! -d ${i} ]; then
      mkdir ${i}
    fi
  done
  for i in BUILD/BUILD BUILD/BUILDROOT PACKAGES/RPMS PACKAGES/SRPMS; do
    if [ ! -d ${i} ]; then
      mkdir ${i}
    fi
  done
}

download_sources() {
  spectool -g "${SPECFILE}"
}

rpmbuild_here() {
  # Build packages in source directory to prevent pollution of the regular
  # rpmbuild directories
  rpmbuild \
    --define "_builddir     $(pwd)/BUILD/BUILD" \
    --define "_buildrootdir $(pwd)/BUILD/BUILDROOT" \
    --define "_rpmdir       $(pwd)/PACKAGES/RPMS" \
    --define "_sourcedir    $(pwd)" \
    --define "_specdir      $(pwd)" \
    --define "_srcrpmdir    $(pwd)/PACKAGES/SRPMS" \
    ${@}
}

install_deps() {
  echo "Installing build dependencies..."
  sudo yum-builddep "${SPECFILE}"
}

show_deps_msg() {
  echo "If rpmbuild complained about missing dependencies, run:"
  echo "  ${0} builddep"
}

make_srpm() {
  create_dirs
  download_sources
  rpmbuild_here -bs "${SPECFILE}"
  if [ "${?}" != "0" ]; then
    show_deps_msg
  fi
}

make_rpm() {
  create_dirs
  download_sources
  rpmbuild_here -bb "${SPECFILE}" || show_deps_msg
  if [[ "$(uname -m)" == "x86_64" ]] && [[ "${MULTILIB}" == true ]]; then
    mock_here --taget=i686 -r 
  fi
}

make_all() {
  make_srpm
  make_rpm
}

#########################
#  END: General options #
#########################

########################
# BEGIN: Clean options #
########################
# Clean up build directory
clean_src() {
  rm -rvf "$(dirname ${0})"/BUILD/BUILD{,ROOT}
  # Only remove BUILD if there's no other files in it
  find "$(dirname ${0})" -maxdepth 1 -type d -name BUILD -empty -delete
  if [ -d "$(dirname ${0})/BUILD" ]; then
    echo "BUILD directory not empty: not removing it"
  fi
}

# Remove RPM's
clean_rpm() {
  rm -rvf "$(dirname ${0})"/PACKAGES/RPMS
}

# Remove SRPM's
clean_srpm() {
  rm -rvf "$(dirname ${0})"/PACKAGES/SRPMS
}

# Remove build directories and (S)RPM's
clean_all() {
  clean_src
  clean_rpm
  clean_srpm
  # If PACKAGES is empty, then remove it too
  find "$(dirname ${0})" -maxdepth 1 -type d -name PACKAGES -empty -delete
  if [ -d "$(dirname ${0})/PACKAGES" ]; then
    echo "PACKAGES directory not empty: not removing it"
  fi
}
########################
#  END: Clean options  #
########################

#######################
# BEGIN: Mock options #
#######################
mock_create_directories() {
  # Create cache, result, and configuration directories
  for i in cache result config; do
    if [ ! -d "${i}" ]; then
      mkdir "${i}"
    fi
  done
}

mock_set_permissions() {
  # Set proper permissions
  sudo chown :mock cache result
  sudo chmod g+rws cache result
}

mock_config_set_dirs() {
  # Set mock directories
  sed \
    -e "s|BASEDIR|$(pwd)/result|" \
    -e "s|CACHEDIR|$(pwd)/cache|" \
    < config.in/site-defaults.cfg.in \
    > config/site-defaults.cfg
}

mock_config_copy_default() {
  # Copy default mock configuration files
  cp /etc/mock/fedora-${FEDORA_VER}-{i386,x86_64}.cfg config/
}

mock_config_symlink_logging() {
  # Symlink /etc/mock/logging.ini to config/
  if [ ! -e config/logging.ini ]; then
    ln -s /etc/mock/logging.ini config/
  fi
}

mock_initialize() {
  pushd "$(dirname ${0})/../internal_mock/" > /dev/null
  
  mock_create_directories

  mock_set_permissions

  mock_config_set_dirs

  mock_config_copy_default

  mock_config_symlink_logging

  case $(uname -m) in
  x86_64)
    # Add 32 bit mock config, so that multilib packages can be built
    local CONFIG=("fedora-${FEDORA_VER}-x86_64" "fedora-${FEDORA_VER}-i386")
    ;;
  i686)
    local CONFIG=("fedora-${FEDORA_VER}-i386")
    ;;
  esac

  # Initialize chroots if caches don't exist
  for i in ${CONFIG[@]}; do
    if [ ! -d "cache/${i}" ]; then
      mock -v --init --configdir=config -r ${i}
    fi
  done

  popd > /dev/null
}

mock_verify() {
  pushd "$(dirname ${0})/../internal_mock/" > /dev/null

  # Problem: Missing directories
  # Fix: Run mock_initialize
  local MISSING_DIRS=""
  for i in cache result config; do
    if [ ! -d "${i}" ]; then
      MISSING_DIRS+="${i}"
    fi
  done
  if [ ! -z "${MISSING_DIRS}" ]; then
    echo ""
    echo "The following directories required for mock are missing:"
    echo "(in $(pwd))"
    echo "  ${MISSING_DIRS}"
    echo ""
    echo -n "Reinitializing mock..."
    mock_initialize
    echo "DONE"
    # Return, since reinitialization will fix all the other problems
    return
  fi
  
  # Problem: Missing chroots
  # Fix: Run mock_initialize
  case $(uname -m) in
  x86_64)
    # Add 32 bit mock config, so that multilib packages can be built
    local CONFIG=("fedora-${FEDORA_VER}-x86_64" "fedora-${FEDORA_VER}-i386")
    ;;
  i686)
    local CONFIG=("fedora-${FEDORA_VER}-i386")
    ;;
  esac
  local MISSING_CHROOTS=""
  for i in ${CONFIG[@]}; do
    if [ ! -d "cache/${i}" ]; then
      MISSING_CHROOTS+="${i}"
    fi
  done
  if [ ! -z "${MISSING_CHROOTS}" ]; then
    echo ""
    echo "The following mock chroots are missing:"
    echo "  ${MISSING_CHROOTS}"
    echo ""
    echo -n "Reinitializing mock..."
    mock_initialize
    echo "DONE"
    # Return, since reinitialization will fix all the other problems
    return
  fi

  # Problem: Wrong permissions
  # Fix: Run mock_set_permissions
  BAD_PERMISSIONS=""
  for i in cache result; do
    if [ "x$(stat --format="%G" ${i})" != "xmock" ]; then
      BAD_PERMISSIONS+="${i}"
    fi
  done
  if [ ! -z "${BAD_PERMISSIONS}" ]; then
    echo ""
    echo "The permissions of the following directories are incorrect:"
    echo "(in $(pwd))"
    echo "  ${BAD_PERMISSIONS}"
    echo ""
    echo -n "Fixing permissions..."
    mock_set_permissions
    echo "DONE"
  fi

  # Problem: Incorrect/Missing directories in site-defaults.cfg
  # Fix: Run mock_config_set_dirs
  BAD_SITE_DEFAULTS_CFG=false
  if [ ! -f config/site-defaults.cfg ]; then
    echo ""
    echo "The mock directories configuration file is missing:"
    echo "(site-defaults.cfg in $(pwd)/config)"
    echo ""
    BAD_SITE_DEFAULTS_CFG=true
  else
    OUTPUT="The directories in the mock configuration file is incorrect:\n"
    OUTPUT+="(site-defaults.cfg in $(pwd)/config)\n"
    # We need to change to the directory first and then run pwd to ensure
    # that there are no extra '.' or '..'
    ORIGINAL_BASEDIR=$(cd $(grep 'config.*basedir' site-defaults.cfg | \
                       awk -F\' '{print $4}'); pwd)
    ORIGINAL_CACHEDIR=$(cd $(grep 'config.*cache_topdir' site-defaults.cfg | \
                        awk -F\' '{print $4}'); pwd)

    if [ "x${ORIGINAL_BASEDIR}" != "x$(pwd)/result" ]; then
      OUTPUT+="  Original base directory: ${ORIGINAL_BASEDIR}\n"
      OUTPUT+="  Actual base directory: $(pwd)/result\n"
      BAD_SITE_DEFAULTS_CFG=true
    elif [ "x${ORIGINAL_CACHEDIR}" != "x$(pwd)/cache" ]; then
      OUTPUT+="  Original cache directory: ${ORIGINAL_CACHEDIR}\n"
      OUTPUT+="  Actual cache directory: $(pwd)/cache\n"
      BAD_SITE_DEFAULTS_CFG=true
    fi
    
    if [ "x${BAD_SITE_DEFAULTS_CFG}" == "xtrue" ]; then
      echo -e "${OUTPUT}"
    fi
  fi
  if [ "x${BAD_SITE_DEFAULTS_CFG}" == "xtrue" ]; then
    echo -n "Recreating site-defaults.cfg..."
    mock_config_set_dirs
    echo "DONE"
  fi
  
  # Problem: Missing configuration files
  # Fix: Run mock_config_copy_default
  if [ ! -f config/fedora-${FEDORA_VER}-i386.cfg ] || \
    [ ! -f config/fedora-${FEDORA_VER}-x86_64.cfg ]; then
    echo "The mock configuration files are missing."
    echo -n "Copying default configuration files..."
    mock_config_copy_default
    echo "DONE"
  fi
  
  # Problem: logging.ini configuration file symlink is missing
  # Fix: Run mock_config_symlink_logging
  if [ ! -e config/logging.ini ]; then
    mock_config_symlink_logging
  fi
  
  # After all the checks...
  echo ""
  echo "Everything should be okay!"
  popd > /dev/null
}
#######################
#  END: Mock options  #
#######################

dir_structure() {
  local FILES="$(find . -maxdepth 1 -type f ! -name '.*' | sort)"
  echo "Directory structure:"
  echo "  Unity-for-Fedora"
  echo "  \`-- ${PWD##*/}"
  for i in ${FILES}; do
    echo "      |-- ${i##*/}"
  done
  #echo "      |-- build.sh"
  #echo "      |-- compare_versions.sh"
  #echo "      |-- Package1.spec"
  if [ -f "${PWD##*/}.rpmlintrc" ]; then
    echo "      |-- ${PWD##*/}.rpmlintrc (configuration file for rpmlint)"
  fi
  echo "      |-- PACKAGES"
  echo "      |    |-- RPMS"
  echo "      |    |   \`-- (generated RPM's are in here)"
  echo "      |    \`-- SRPMS"
  echo "      |        \`-- (generated SRPM is in here)"
  echo "      \`-- SOURCES"
  echo "           |-- BUILD"
  echo "           |   \`-- (source code build directory is in here)"
  echo "           \`-- BUILDROOT"
  echo "               \`-- (source code install directory is in here)"
}

build() {
  if [ -f "$(dirname ${0})/../internal.lock" ]; then
    echo "Another build is currently running. Please wait for it to finish."
    echo "If you are absolutely sure that no other build is running, delete"
    echo "the following file:"
    echo ""
    echo "  $(cd $(dirname ${0})/..; pwd)/internal.lock"
    exit 1
  fi

  touch "$(dirname ${0})/../internal.lock"

  case "${1}" in
  ## General options ##
  srpm|srpms)
    make_srpm
    ;;
  rpm|rpms)
    make_rpm
    ;;
  builddep)
    install_deps
    ;;
  all)
    make_all
    ;;
  install)
    echo "Not implemented yet :("
    ;;
  ## Clean options ##
  clean)
    clean_src
    ;;
  clean-src)
    clean_src
    ;;
  clean-rpm)
    clean_rpm
    ;;
  clean-srpm)
    clean_srpm
    ;;
  clean-all)
    clean_all
    ;;
  ## Mock options ##
  mock-init)
    mock_initialize
    ;;
  mock-check)
    mock_verify
    ;;
  check)
    echo "Not implemented yet :("
    ;;
  ## Help options ##
  dirstructure)
    dir_structure
    ;;
  mock-info)
    echo "Not written yet :("
    ;;
  ## Info menu ##
  *)
    echo "Unity-for-Fedora build tool"
    echo ""
    echo "Usage: ${0} [OPTION...]"
    echo ""
    echo "Options:"
    echo "  srpm         - Generate SRPM"
    echo "  rpm          - Generate RPM's"
    echo "  builddep     - Install build dependencies"
    echo "  all          - Generate SRPM and RPM's"
    echo "  install      - Install generated RPM's"
    echo "  check        - Run rpmlint on generated RPM's and SRPM's"
    echo ""
    echo "Clean Options:"
    echo "  clean        - Same as clean-src"
    echo "  clean-src    - Remove build directories (BUILD)"
    echo "  clean-rpm    - Remove built RPM's (PACKAGES/RPMS)"
    echo "  clean-srpm   - Remove generated SRPM's (PACKAGES/SRPMS)"
    echo "  clean-all    - Run clean-src, clean-rpm, and clean-rpm"
    echo ""
    echo "Mock Options:"
    echo "  mock-init    - Intialize the mock build environment"
    echo "  mock-check   - Verify the mock build environment"
    echo ""
    echo "Help Options:"
    echo "  dirstructure - Show directory structure information"
    echo "  mock-info    - Show information about mock"
    echo ""
    echo "This package generates the following RPM's:"
    for i in ${GENERATED_RPMS[@]}; do
      echo "  ${i}"
    done
    echo ""
    echo "and the following SRPM:"
    echo "  ${GENERATED_SRPM}"
    echo ""
    echo "DO NOT manually install the RPM's (unless you know what you are doing)."
    echo "Use the 'install' option instead. The Unity-for-Fedora build scripts"
    echo "create packages using mock, which builds packages cleanly inside a chroot."
    echo "The 'install' option will install the packages both inside the chroot and"
    echo "directly on the computer."
    ;;
  esac

  rm "$(dirname ${0})/../internal.lock"
}
