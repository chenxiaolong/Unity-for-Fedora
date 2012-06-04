#!/usr/bin/env bash

#echo "Querying spec file..."

GENERATED_RPMS=$(rpmspec -q --rpms ${SPECFILE})
GENERATED_SRPM=$(rpmspec -q --srpm ${SPECFILE})
# Why would the srpm name have the arch in it??
GENERATED_SRPM="${GENERATED_SRPM%.*}.src"
# spectool doesn't like using just the filename
for i in $(spectool -l -A "$(dirname ${0})/${SPECFILE}" | awk '{print $2}'); do
  SOURCES+="${i##*/} "
done
FEDORA_VER="$(grep '%fedora' /etc/rpm/macros.dist | awk '{print $2}')"

##########################
# BEGIN: General options #
##########################
create_dirs() {
  # Create a directory structure simitlar to Arch Linux's PKGBUILD build
  # directory structure. This allow all the needed files to be contained
  # in a single directory, which prevents having duplicate copies of files
  # and allow the directories to be cleaned up easily.

  for i in SOURCES PACKAGES; do
    if [ ! -d ${i} ]; then
      mkdir ${i}
    fi
  done
  for i in SOURCES/BUILD SOURCES/BUILDROOT PACKAGES/RPMS PACKAGES/SRPMS; do
    if [ ! -d ${i} ]; then
      mkdir ${i}
    fi
  done
}

download_sources() {
  pushd SOURCES > /dev/null
  spectool -g "../${SPECFILE}"
  popd > /dev/null
}

symlink_sources() {
  for i in ${SOURCES}; do
    # For files included in git, symlink them in SOURCES/
    if [ -f "${i}" ]; then
      if [ ! -f "SOURCES/${i}" ]; then
        ln -s "$(cd $(dirname ${0}) && pwd)/${i}" SOURCES/
      fi
    fi
  done
}

rpmbuild_here() {
  # Build packages in source directory to prevent pollution of the regular
  # rpmbuild directories
  rpmbuild \
    --define "_builddir     $(pwd)/SOURCES/BUILD"     \
    --define "_buildrootdir $(pwd)/SOURCES/BUILDROOT" \
    --define "_rpmdir       $(pwd)/PACKAGES/RPMS"     \
    --define "_sourcedir    $(pwd)/SOURCES"           \
    --define "_specdir      $(pwd)"                   \
    --define "_srcrpmdir    $(pwd)/PACKAGES/SRPMS"    \
    ${@}
}

mock_here() {
  # Build packages in local mock directory
  if [ "x${1}" == "xi686" ]; then
    local CONFIG="fedora-${FEDORA_VER}-i386"
  else
    local CONFIG="fedora-${FEDORA_VER}-${1}"
  fi
  mock                                                    \
    -v                                                    \
    --configdir="$(dirname ${0})/../internal_mock/config" \
    -r "${CONFIG}"                                        \
    --target="${1}"                                       \
    "${2}"
  local RPM_COUNT=$(find \
    "$(dirname ${0})/../internal_mock/result/${CONFIG}/result/" \
     -maxdepth 1 -type f -name '*.rpm')
  if [ -z "${RPM_COUNT}" ]; then
    echo "Failed to build ${1} packages!"
    exit 1
  fi
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
  symlink_sources
  rpmbuild_here -bs "${SPECFILE}"
  if [ "${?}" != "0" ]; then
    show_deps_msg
    exit 1
  fi
}

copy_rpm() {
  if [ "x${1}" == "xi686" ]; then
    local MOCKARCH=i386
  else
    local MOCKARCH=${1}
  fi
  local FILEPATH="$(cd $(dirname ${0})/..; pwd)/internal_mock/result/fedora-${FEDORA_VER}-${MOCKARCH}/result/${2}"
  local ARCH=$(rpm -q --qf '%{arch}' -p "${FILEPATH}")
  if [ ! -d PACKAGES/RPMS/${ARCH} ]; then
    mkdir -p PACKAGES/RPMS/${ARCH}
  fi
  cp "${FILEPATH}" PACKAGES/RPMS/${ARCH}/
}

copy_rpm_mock() {
  # Copy RPM's to local repo
  if [ "x${1}" == "xmultilib" ]; then
    # If running in multilib mode, copy the RPM from the i386 repo to the x86_64 repo
    cp "$(dirname ${0})/../internal_mock/repo/i386/${2}" \
       "$(dirname ${0})/../internal_mock/repo/x86_64/"
    return
  else
    # In normal mode, copy RPM's from mock result directory to the appropriate repo
    if [ "x${1}" == "xi686" ]; then
      local MOCKARCH=i386
    else
      local MOCKARCH=${1}
    fi
    local FILEPATH=
    cp "$(cd $(dirname ${0})/..; pwd)/internal_mock/result/fedora-${FEDORA_VER}-${MOCKARCH}/result/${2}" \
       "$(dirname ${0})/../internal_mock/repo/${MOCKARCH}/"
  fi
}

update_repo() {
  if [ "x${1}" == "xi686" ]; then
    local MOCKARCH=i386
  else
    local MOCKARCH=${1}
  fi
  createrepo --update "$(dirname ${0})/../internal_mock/repo/${MOCKARCH}/"
}

make_rpm() {
  create_dirs
  download_sources
  symlink_sources
  if [ "x${USE_RPMBUILD}" == "xtrue" ]; then
    # If rpmbuild mode is used with a multilib package on x86_64, warn user
    # that i686 packages won't be created.
    if [[ "$(uname -m)" == "x86_64" ]] && [ "x${MULTILIB}" == "xtrue" ]; then
      echo "WARNING: rpmbuild mode cannot generate i686 packages for multilib packages"
    fi
    rpmbuild_here -bb "${SPECFILE}" || show_deps_msg
  else
    # Build source RPM for mock
    make_srpm

    # Build RPM's using mock for CPU architecture
    mock_here $(uname -m) "./PACKAGES/SRPMS/${GENERATED_SRPM}.rpm"

    # Copy the built RPM's to PACKAGES/RPMS and the local repo
    for i in ${GENERATED_RPMS[@]}; do
      copy_rpm $(uname -m) "${i}.rpm"
      copy_rpm_mock $(uname -m) "${i}.rpm"
    done

    # Update repo database
    update_repo $(uname -m)

    # If the package is multilib
    if [ "x$(uname -m)" == "xx86_64" ] && [ "x${MULTILIB}" == "xtrue" ]; then
      # Build the i686 packages
      mock_here i686 "./PACKAGES/SRPMS/${GENERATED_SRPM}.rpm"

      # Copy the i686 packages to the i686 repo
      for i in $(rpmspec --target i686 -q --queryformat        \
                 '%{name}-%{version}-%{release}.%{arch}.rpm\n' \
                 ${SPECFILE}); do
        copy_rpm_mock i686 "${i}"
      done

      # Update i686 repo database
      update_repo i686

      # Copy multilib packages to x86_64 repo and PACKAGES/RPMS/i686/
      local FILENAME=$(rpmspec --target=i686 -q                        \
                       --queryformat="%{version}-%{release}.%{arch}\n" \
                       ${SPECFILE} | grep -v 'noarch' | uniq)
      for i in ${MULTILIB_PACKAGES[@]}; do
        copy_rpm i686 "${i}-${FILENAME}.rpm"
        copy_rpm_mock multilib "${i}-${FILENAME}.rpm"
      done

      # Update x86_64 repo database
      update_repo x86_64
    fi
  fi
}

check_if_install() {
  for k in ${DO_NOT_INSTALL[@]}; do
    if [ "x${k}" == "x${1}" ]; then
      return 1
    fi
  done
  return 0
}

check_if_install_multilib() {
  check_if_install ${1} && for k in ${MULTILIB_DO_NOT_INSTALL[@]}; do
    if [ "x${k}" == "x${1}" ]; then
      return 1
    fi
  done
  return 0
}

get_rpms() {
  local MISSING_RPMS=""
  local AVAILABLE_RPMS=""
  for i in ${GENERATED_RPMS[@]}; do
    local FILE_ARCH="${i##*.}"
    #local FILE_LOCATION="$(find PACKAGES/RPMS/ -type f -mindepth 2 -maxdepth 2 \
    #                       -name ${i}.rpm)"
    #if [ -z "${FILE_LOCATION}" ]; then
    if [ ! -f PACKAGES/RPMS/${FILE_ARCH}/${i}.rpm ]; then
      MISSING_RPMS+="  ${i}.rpm\n"
    else
      check_if_install $(rpm -q --qf '%{name}' -p PACKAGES/RPMS/${FILE_ARCH}/${i}.rpm) \
        && AVAILABLE_RPMS+=" PACKAGES/RPMS/${FILE_ARCH}/${i}.rpm"
    fi
  done

  # Multilib packages
  if [ "x$(uname -m)" == "xx86_64" ] && [ "x${MULTILIB}" == "xtrue" ]; then
    local FILENAME=$(rpmspec --target=i686 -q                        \
                     --queryformat="%{version}-%{release}.%{arch}\n" \
                     ${SPECFILE} | grep -v 'noarch' | uniq)
    for i in ${MULTILIB_PACKAGES[@]}; do
      local RPM_NAME="${i}-${FILENAME}.rpm"
      if [ ! -f PACKAGES/RPMS/i686/${RPM_NAME} ]; then
        MISSING_RPMS+="  ${RPM_NAME}\n"
      else
        check_if_install_multilib ${i} && AVAILABLE_RPMS+=" PACKAGES/RPMS/i686/${RPM_NAME}"
      fi
    done
  fi

  if [ ! -z "${MISSING_RPMS}" ]; then
    echo "Cannot proceed; the following RPM's are missing:"
    echo -e "${MISSING_RPMS}"
    echo "Please rebuild the package."
    return
  fi

  echo ${AVAILABLE_RPMS}
}

install_rpms() {
  sudo yum install $(get_rpms)
}

#########################
#  END: General options #
#########################

########################
# BEGIN: Clean options #
########################
# Clean up build directory
clean_build() {
  rm -rvf SOURCES/BUILD{,ROOT}
}

# Remove entire source directory
clean_src() {
  clean_build

  # Remove source symlinks
  for i in ${SOURCES}; do
    if [ -e "SOURCES/${i}" ]; then
      rm "SOURCES/${i}"
    fi
  done
  # Only remove BUILD if there's no other files in it
  find . -maxdepth 1 -type d -name SOURCES -empty -delete
  if [ -d SOURCES ]; then
    echo "SOURCES directory not empty: not removing it"
  fi
}

# Remove RPM's
clean_rpm() {
  rm -rvf PACKAGES/RPMS
}

# Remove SRPM's
clean_srpm() {
  rm -rvf PACKAGES/SRPMS
}

# Remove build directories and (S)RPM's
clean_all() {
  clean_src
  clean_rpm
  clean_srpm
  # If PACKAGES is empty, then remove it too
  find . -maxdepth 1 -type d -name PACKAGES -empty -delete
  if [ -d PACKAGES ]; then
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
  for i in cache result config repo; do
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
  case $(uname -m) in
  x86_64)
    # Add 32 bit mock config, so that multilib packages can be built
    local CONFIG=("fedora-${FEDORA_VER}-x86_64" "fedora-${FEDORA_VER}-i386")
    ;;
  i686)
    local CONFIG=("fedora-${FEDORA_VER}-i386")
    ;;
  esac
  for i in ${CONFIG[@]}; do
    head -n -1 /etc/mock/${i}.cfg > config/${i}.cfg
    # Add local repo
    cat >> config/${i}.cfg << EOF

[unity-for-fedora]
name=unity-for-fedora
baseurl=file://$(pwd)/repo/${i##*-}
"""
EOF
    if [ ! -d repo/${i##*-}/ ]; then
      mkdir repo/${i##*-}/
    fi
    if [ ! -d repo/${i##*-}/repodata/ ]; then
      createrepo --database "$(dirname ${0})/../internal_mock/repo/${i##*-}/" &>/dev/null
    fi
  done
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

  # Problem: Missing local repo
  # Fix: Create it
  if [ ! -d repo ]; then
    echo ""
    echo "The local repo is missing."
    echo -n "Creating it..."
    mkdir repo
    echo "DONE"
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
      MISSING_CHROOTS+="${i}\n"
    fi
  done
  if [ ! -z "${MISSING_CHROOTS}" ]; then
    echo ""
    echo "The following mock chroots are missing:"
    echo -e "  ${MISSING_CHROOTS}"
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
  local BAD_SITE_DEFAULTS_CFG=false
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
    ORIGINAL_BASEDIR=$(grep 'config.*basedir' config/site-defaults.cfg | \
                       awk -F\' '{print $4}')
    ORIGINAL_CACHEDIR=$(grep 'config.*cache_topdir' config/site-defaults.cfg | \
                        awk -F\' '{print $4}')

    if [ "x$(cd ${ORIGINAL_BASEDIR} 2>/dev/null && pwd)" != "x$(pwd)/result" ]; then
      OUTPUT+="  Original base directory: ${ORIGINAL_BASEDIR}\n"
      OUTPUT+="  Actual base directory: $(pwd)/result\n"
      BAD_SITE_DEFAULTS_CFG=true
    fi
    if [ "x$(cd ${ORIGINAL_CACHEDIR} 2>/dev/null && pwd)" != "x$(pwd)/cache" ]; then
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
  case $(uname -m) in
  x86_64)
    local CONFIG=("fedora-${FEDORA_VER}-x86_64" "fedora-${FEDORA_VER}-i386")
    ;;
  i686)
    local CONFIG=("fedora-${FEDORA_VER}-i386")
    ;;
  esac
  local MISSING_CONFIG=""
  for i in ${CONFIG[@]}; do
    if [ ! -f config/${i}.cfg ]; then
      MISSING_CONFIG+="  config/${i}.cfg\n"
    fi
  done
  if [ ! -z "${MISSING_CONFIG}" ]; then
    echo ""
    echo "The following mock configuration files are missing:"
    echo -e "${MISSING_CONFIG}"
    echo -n "Copying default configuration files..."
    mock_config_copy_default
    echo "DONE"
  fi

  # Problem: Configuration files do not contain unity-for-fedora local repo
  # Fix: Run mock_config_copy_default
  case $(uname -m) in
  x86_64)
    local CONFIG=("fedora-${FEDORA_VER}-x86_64" "fedora-${FEDORA_VER}-i386")
    ;;
  i686)
    local CONFIG=("fedora-${FEDORA_VER}-i386")
    ;;
  esac
  local MISSING_REPO=""
  for i in ${CONFIG[@]}; do
    if ! $(grep "\[unity-for-fedora\]" config/${i}.cfg &>/dev/null); then
      MISSING_REPO+="  config/${i}.cfg\n"
    fi
  done
  if [ ! -z "${MISSING_REPO}" ]; then
    echo ""
    echo "The following mock configuration files are missing the local repo:"
    echo -e "${MISSING_REPO}"
    echo -n "Recreating configuration files..."
    mock_config_copy_default
    echo "DONE"
  fi

  # Problem: Missing local repo metadata
  # Fix: Run mock_config_copy_default
  local REPODATA="$(find repo/ -mindepth 2 -maxdepth 2 -type d -name repodata)"
  if [ -z "${REPODATA}" ]; then
    echo ""
    echo "The local repo for mock is missing the metadata/database."
    echo ""
    echo -n "Recreating configuration files and repo database..."
    mock_config_copy_default
    echo "DONE"
  fi
  
  # Problem: logging.ini configuration file symlink is missing
  # Fix: Run mock_config_symlink_logging
  if [ ! -e config/logging.ini ]; then
    echo ""
    echo "The config/logging.ini symlink is missing."
    echo ""
    echo -n "Recreating symlink..."
    mock_config_symlink_logging
    echo "DONE"
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
    echo "An error has occured. One of the following might have happened:"
    echo ""
    echo "- A previous build failed or was interrupted."
    echo "- Another build is currently running."
    echo ""
    echo "If you are absolutely sure that no other build is running and that a"
    echo "previous build did not fail, delete the lock file:"
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
  install)
    install_rpms
    ;;
  ## Clean options ##
  clean)
    clean_build
    ;;
  clean-src)
    clean_src
    ;;
  clean-build)
    clean_build
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
    echo "  srpm          - Generate SRPM"
    echo "  rpm           - Generate RPM's (SRPM generated during process)"
    echo "  builddep      - Install build dependencies"
    echo "  install       - Install generated RPM's"
    echo "  check         - Run rpmlint on generated RPM's and SRPM's"
    echo ""
    echo "Clean Options:"
    echo "  clean         - Same as clean-build"
    echo "  clean-src     - Remove entire source/build directory (SOURCES)"
    echo "  clean-build   - Remove build directories (SOURCES/BUILD{,ROOT})"
    echo "  clean-rpm     - Remove built RPM's (PACKAGES/RPMS)"
    echo "  clean-srpm    - Remove generated SRPM's (PACKAGES/SRPMS)"
    echo "  clean-all     - Run clean-src, clean-rpm, and clean-rpm"
    echo ""
    echo "Mock Options:"
    echo "  mock-init     - Intialize the mock build environment"
    echo "  mock-check    - Verify the mock build environment"
    echo ""
    echo "Help Options:"
    echo "  dirstructure  - Show directory structure information"
    echo "  mock-info     - Show information about mock"
    echo ""
    echo "This package generates the following RPM's:"
    for i in ${GENERATED_RPMS[@]}; do
      echo "  ${i}.rpm"
    done
    echo ""
    echo "and the following SRPM:"
    echo "  ${GENERATED_SRPM}.rpm"
    echo ""
    echo "Please use the 'install' option to install the RPM's. This ensures that"
    echo "the i686 multilib packages are installed on x86_64 systems. Also, extra"
    echo "packages, which may not be very useful to anyone, except for developers,"
    echo "will be skipped automatically."
    ;;
  esac

  rm "$(dirname ${0})/../internal.lock"
}
