# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based on Fedora 18's spec file

# Released ABI versions. Must keep in sync with the source.
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 13
%global videodrv_minor 1
%global xinput_major 18
%global xinput_minor 0
%global extension_major 7
%global extension_minor 0

Name:		xorg-x11-server
Version:	1.13.3
Release:	100%{?dist}
Summary:	X.Org X11 X server

Group:		User Interface/X
License:	MIT
URL:		http://www.x.org/
Source0:	http://ftp.x.org/pub/individual/xserver/xorg-server-%{version}.tar.bz2
Source1:	fedora_gitignore
Source2:	fedora_xserver.pamd
Source3:	fedora_10-quirks.conf
Source4:	fedora_xserver-sdk-abi-requires.release
Source5:	http://svn.exactcode.de/t2/trunk/package/xorg/xorg-server/xvfb-run.sh

Patch0:		fedora_xserver-1.4.99-ssh-isnt-local.patch
Patch1:		fedora_xserver-1.6.0-less-acpi-brokenness.patch
Patch2:		f18_xserver-1.6.99-right-of.patch
Patch3:		fedora_xserver-1.12-Xext-fix-selinux-build-failure.patch
Patch4:		f18_xserver-1.12.2-xorg-touch-test.patch
Patch5:		fedora_0001-linux-Refactor-xf86-En-Dis-ableIO.patch
Patch6:		fedora_0002-linux-Make-failure-to-iopl-non-fatal.patch
Patch7:		fedora_0003-xfree86-Change-the-semantics-of-driverFunc-GET_REQUI.patch
Patch8:		fedora_0001-Always-install-vbe-and-int10-sdk-headers.patch
Patch9:		fedora_xserver-autobind-hotplug.patch
Patch10:	fedora_0001-xf86-return-NULL-for-compat-output-if-no-outputs.patch
Patch11:	fedora_0001-xf86-Fix-build-against-recent-Linux-kernel.patch
Patch12:	fedora_0001-linux-Prefer-ioctl-KDSKBMUTE-1-over-ioctl-KDSKBMODE-.patch
Patch13:	fedora_0001-mieq-Bump-default-queue-size-to-512.patch
Patch14:	fedora_0001-xfree86-hotplug-cleanup-properly-if-the-screen-fails.patch
Patch15:	fedora_0001-xf86crtc-don-t-use-display-for-vx-vy-for-gpu-screens.patch
Patch16:	fedora_0001-dix-allow-pixmap-dirty-helper-to-be-used-for-non-sha.patch
Patch17:	fedora_0001-xserver-call-CSR-for-gpus.patch
Patch18:	fedora_0001-xf86-actually-set-the-compat-output-in-the-failure-c.patch
Patch19:	fedora_0001-autoconfig-fixup-tell-changed-so-randr-clients-can-t.patch
Patch20:	fedora_0001-os-use-libunwind-to-generate-backtraces.patch
Patch21:	fedora_0001-xf86-fix-flush-input-to-work-with-Linux-evdev-device.patch
# From Ubuntu's packaging version 1.13.0 and release 0ubuntu4
#Patch90:	500_pointer_barrier_thresholds.diff
Source90:	500_pointer_barrier_thresholds.diff

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	git-core
BuildRequires:	libtool
#BuildRequires:	kernel-headers
BuildRequires:	pkgconfig
BuildRequires:	xorg-x11-font-utils
BuildRequires:	xorg-x11-util-macros

BuildRequires:	pkgconfig(dmx)
BuildRequires:	pkgconfig(fontenc)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xfont)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xres)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtrans)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xv)

BuildRequires:	audit-libs-devel
BuildRequires:	systemtap-sdt-devel
BuildRequires:	xorg-x11-proto-ubuntu-devel
# libunwind is Exclusive for the following arches
%ifarch %{arm} hppa ia64 mips ppc ppc64 %{ix86} x86_64
# pre-1.0.1-5 is missing pkg-config
BuildRequires:	libunwind-devel >= 1.0.1-5
%endif

%description
X.Org X11 X server

# Fedora's Xorg policy:
#
# All server subpackages have a virtual provide for the name of the server they
# deliver. The Xorg one is versioned, the others are intentionally unversioned.


%package common
Summary:	Xorg server common files
Group:		User Interface/X

Requires:	pixman >= 0.21.8
Requires:	xkbcomp
Requires:	xkeyboard-config

Provides:	xorg-x11-server-ubuntu-common = %{version}-%{release}

%description common
Common files shared among all X servers.


%package Xorg
Summary:	Xorg X server
Group:		User Interface/X

Requires:	xorg-x11-server-common >= %{version}-%{release}
Requires:	system-setup-keyboard

Provides:	Xorg = %{version}-%{release}
Provides:	Xserver
# Xorg ABI versions
Provides:	xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides:	xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides:	xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides:	xserver-abi(extension-%{extension_major}) = %{extension_minor}
# The following input drivers were dropped in Fedora 17
Obsoletes:	xorg-x11-drv-acecad <= 1.5.0-2.fc16
Obsoletes:	xorg-x11-drv-aiptek <= 1.4.1-2.fc16
Obsoletes:	xorg-x11-drv-elographics <= 1.3.0-2.fc16
Obsoletes:	xorg-x11-drv-fpit <= 1.4.0-2.fc16
Obsoletes:	xorg-x11-drv-hyperpen <= 1.4.1-2.fc16
Obsoletes:	xorg-x11-drv-mutouch <= 1.3.0-2.fc16
Obsoletes:	xorg-x11-drv-penmount <= 1.5.0-3.fc16
%if 0%{?fedora} > 17
# Ths following legacy video drivers were dopped in Fedora 18
Obsoletes:	xorg-x11-drv-ark <= 0.7.3-15.fc17
Obsoletes:	xorg-x11-drv-chips <= 1.2.4-8.fc18
Obsoletes:	xorg-x11-drv-s3 <= 0.6.3-14.fc17
Obsoletes:	xorg-x11-drv-tseng <= 1.2.4-12.fc17
%endif

Provides:	xorg-x11-server-ubuntu-Xorg = %{version}-%{release}

%description Xorg
X.org X11 is an open source implementation of the X Window System. It provides
the basic low level functionality which full fledged graphical user interfaces
(GUIs) such as GNOME and KDE are designed upon.


%package Xnest
Summary:	A nested server.
Group:		User Interface/X

Requires:	xorg-x11-server-common >= %{version}-%{release}

Provides:	Xnest
Obsoletes:	xorg-x11-Xnest

Provides:	xorg-x11-server-ubuntu-Xnest = %{version}-%{release}

%description Xnest
Xnest is an X server, which has been implemented as an ordinary X application.
It runs in a window just like other X applications, but it is an X server itself
in which you can run other software. It is a very useful tool for developers who
wish to test their applications without running them on their real X server.


%package Xdmx
Summary:	Distributed Multihead X Server and utilities
Group:		User Interface/X

Requires:	xorg-x11-server-common >= %{version}-%{release}

Provides:	Xdmx
Obsoletes:	xorg-x11-Xdmx

Provides:	xorg-x11-server-ubuntu-Xdmx = %{version}-%{release}

%description Xdmx
Xdmx is proxy X server that provides multi-head support for multiple displays
attached to different machines (each of which is running a typical X server).
When Xinerama is used with Xdmx, the multiple displays on multiple machines are
presented to the user as a single unified screen.  A simple application for Xdmx
would be to provide multi-head support using two desktop machines, each of which
has a single display device attached to it.  A complex application for Xdmx
would be to unify a 4 by 4 grid of 1280x1024 displays (each attached to one of
16 computers) into a unified 5120x4096 display.


%package Xvfb
Summary:	A X Windows System virtual framebuffer X server.
Group:		User Interface/X
# xvfb-run is GPLv2
License:	GPLv2 and MIT

Requires:	xorg-x11-server-common >= %{version}-%{release}
# For xvfb-run
Requires:	xorg-x11-xauth

Provides:	Xvfb
Obsoletes:	xorg-x11-Xvfb

Provides:	xorg-x11-server-ubuntu-Xvfb = %{version}-%{release}

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on machines
with no display hardware and no physical input devices. Xvfb simulates a dumb
framebuffer using virtual memory. Xvfb does not open any devices, but behaves
otherwise as an X display. Xvfb is normally used for testing servers.


%package Xephyr
Summary:	A nested server.
Group:		User Interface/X

Requires:	xorg-x11-server-common >= %{version}-%{release}

Provides:	Xephyr

Provides:	xorg-x11-server-ubuntu-Xephyr = %{version}-%{release}

%description Xephyr
Xephyr is an X server, which has been implemented as an ordinary X application.
It runs in a window just like other X applications, but it is an X server itself
in which you can run other software. It is a very useful tool for developers who
wish to test their applications without running them on their real X server.
Unlike Xnest, Xephyr renders to an X image rather than relaying the X protocol,
and therefore supports the newer X extensions like Render and Composite.


%package devel
Summary:	SDK for X server driver module development
Group:		User Interface/X

Requires:	pkgconfig
Requires:	pkgconfig(pciaccess)
Requires:	pkgconfig(pixman-1)

Requires:	xorg-x11-proto-devel
Requires:	xorg-x11-util-macros

Provides:	xorg-x11-server-ubuntu-devel = %{version}-%{release}

%description devel
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules outside of
the standard X11 source code tree. Developers writing video drivers, input
drivers, or other X modules should install this package.


%package source
Summary:	Xserver source code required to build VNC server (Xvnc)
Group:		Development/Libraries

BuildArch:	noarch

Provides:	xorg-x11-server-ubuntu-source = %{version}-%{release}

%description source
Xserver source code needed to build VNC server (Xvnc)


%prep
%setup -q -n xorg-server-%{version}

git init

if [ -z "$GIT_COMMITTER_NAME" ]; then
  #git config user.email "x@fedoraproject.org"
  #git config user.name "Fedora X Ninjas"

  # This is not the official Fedora package, so contact me instead
  git config user.email "chenxiaolong@cxl.epac.to"
  git config user.name "Xiao-Long Chen"
fi

cp %{SOURCE1} .gitignore

git add .
git commit -a -q -m "%{version} baseline."

# Apply patches
git am -p1 %{patches} < /dev/null

patch -Np1 -i %{SOURCE90}

# Verify ABI versions
getmajor() {
  grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
    tr '(),' '   ' | awk '{ print $4 }'
}

getminor() {
  grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
    tr '(),' '   ' | awk '{ print $5 }'
}

test `getmajor ansic` == %{ansic_major}
test `getminor ansic` == %{ansic_minor}
test `getmajor videodrv` == %{videodrv_major}
test `getminor videodrv` == %{videodrv_minor}
test `getmajor xinput` == %{xinput_major}
test `getminor xinput` == %{xinput_minor}
test `getmajor extension` == %{extension_major}
test `getminor extension` == %{extension_minor}

autoreconf -vfi


%build
%global default_font_path "catalogue:/etc/X11/fontpath.d,built-ins"

%configure \
  --enable-maintainer-mode       \
  --enable-xvfb                  \
  --enable-xnest                 \
  --enable-kdrive                \
  --enable-xephyr                \
  --disable-xfake                \
  --disable-xfbdev               \
  --enable-xorg                  \
  --disable-static               \
  --with-pic                     \
  --with-int10=x86emu            \
  --with-default-font-path=%{default_font_path} \
  --with-module-dir=%{_libdir}/xorg/modules \
  --with-builderstring="Build ID: %{name} %{version}-%{release}" \
  --with-os-name="$(hostname -s) $(uname -r)" \
  --with-xkb-output=%{_localstatedir}/lib/xkb \
  --with-dtrace                  \
  --enable-xselinux              \
  --enable-record                \
  --enable-config-udev           \
  --with-dri-driver-path=%{_libdir}/dri \
  --with-vendor-name="GNOME:Ayatana Project"

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} moduledir=%{_libdir}/xorg/modules

rm -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/libxf8_16bpp.so
rm -rv $RPM_BUILD_ROOT%{_libdir}/xorg/modules/multimedia/
install -dm755 $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}/

install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/xserver

install -dm755 $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/10-quirks.conf

# Make sure /etc/X11/xorg.conf.d/ exists. system-setup-keyboard needs it.
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/

install -dm755 $RPM_BUILD_ROOT%{_bindir}/
install -m755 %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires

# Install xvfb-run
install -m755 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/xvfb-run

# Create the source package
%global xserver_source_dir %{_datadir}/xorg-x11-server-source
%global inst_srcdir %{buildroot}/%{xserver_source_dir}
install -dm755 %{inst_srcdir}/{Xext,xkb,GL,hw/{xquartz/bundle,xfree86/common}}
install -dm755 %{inst_srcdir}/{hw/dmx/doc,man,doc,hw/dmx/doxygen}
install -m644 {,%{inst_srcdir}/}hw/xquartz/bundle/cpprules.in
install -m644 {,%{inst_srcdir}/}man/Xserver.man
install -m644 {,%{inst_srcdir}/}doc/smartsched
install -m644 {,%{inst_srcdir}/}hw/dmx/doxygen/doxygen.conf.in
install -m644 {,%{inst_srcdir}/}xserver.ent.in
install -m644 xkb/README.compiled %{inst_srcdir}/xkb
install -m644 hw/xfree86/xorgconf.cpp %{inst_srcdir}/hw/xfree86

find . -type f | egrep '.*\.(c|h|am|ac|inc|m4|h.in|pc.in|man.pre|pl|txt)$' |
  xargs tar cf - | (cd %{inst_srcdir} && tar xf -)

# SLEDGEHAMMER
find %{inst_srcdir}/hw/xfree86 -name \*.c -delete

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%files common
%doc COPYING
%{_mandir}/man1/Xserver.1.gz
%{_libdir}/xorg/protocol.txt
%dir %{_localstatedir}/lib/xkb/
%{_localstatedir}/lib/xkb/README.compiled


%global Xorgperms %attr(4755, root, root)

%files Xorg
%config %attr(0644,root,root) %{_sysconfdir}/pam.d/xserver
%{_bindir}/X
%{Xorgperms} %{_bindir}/Xorg
%{_bindir}/cvt
%{_bindir}/gtf
%dir %{_libdir}/xorg/
%dir %{_libdir}/xorg/modules/
%dir %{_libdir}/xorg/modules/drivers/
%dir %{_libdir}/xorg/modules/extensions/
%dir %{_libdir}/xorg/modules/input/
%{_libdir}/xorg/modules/extensions/libglx.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libfbdevhw.so
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libvbe.so
%{_libdir}/xorg/modules/libwfb.so
%dir %{_sysconfdir}/X11/xorg.conf.d/
%dir %{_datadir}/X11/xorg.conf.d/
%{_datadir}/X11/xorg.conf.d/10-evdev.conf
%{_datadir}/X11/xorg.conf.d/10-quirks.conf
%{_mandir}/man1/Xorg.1.gz
%{_mandir}/man1/cvt.1.gz
%{_mandir}/man1/gtf.1.gz
%{_mandir}/man4/exa.4.gz
%{_mandir}/man4/fbdevhw.4.gz
%{_mandir}/man5/xorg.conf.5.gz
%{_mandir}/man5/xorg.conf.d.5.gz


%files Xnest
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.1.gz


%files Xdmx
%{_bindir}/Xdmx
%{_bindir}/dmxaddinput
%{_bindir}/dmxaddscreen
%{_bindir}/dmxinfo
%{_bindir}/dmxreconfig
%{_bindir}/dmxresize
%{_bindir}/dmxrminput
%{_bindir}/dmxrmscreen
%{_bindir}/dmxtodmx
%{_bindir}/dmxwininfo
%{_bindir}/vdltodmx
%{_bindir}/xdmxconfig
%{_mandir}/man1/Xdmx.1.gz
%{_mandir}/man1/dmxtodmx.1.gz
%{_mandir}/man1/vdltodmx.1.gz
%{_mandir}/man1/xdmxconfig.1.gz


%files Xvfb
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.1.gz


%files Xephyr
%{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1.gz


%files devel
%doc COPYING
%dir %{_includedir}/xorg/
%{_includedir}/xorg/*.h
%{_libdir}/pkgconfig/xorg-server.pc
%{_bindir}/xserver-sdk-abi-requires
%{_datadir}/aclocal/xorg-server.m4
%dir %{_docdir}/xorg-server/
%{_docdir}/xorg-server/Xserver-DTrace.xml


%files source
%{_datadir}/xorg-x11-server-source/


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.13.3-100
- Version 1.13.3
- Merge Fedora's changes:
  - 1.13.2-4: Fix scrolling for Evoluent Vertical Mouse 3 (#612140#c20)
  - 1.13.2.902-2: use libunwind for backtraces
  - 1.13.3-2: libunwind is exists only on selected arches
  - 1.13.3-3: CVE-2013-1940: Fix xf86FlushInput() to drain evdev events
              (#950438, #952949)

* Tue Jan 29 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.13.2-100
- Version 1.13.2
- Merge Fedora's changes:
  - 1.13.0-7: Fix build issues on new kernels caused by removal of _INPUT_H
  - 1.13.0-8: Fix for non-PCI configuration-less setups
  - 1.13.0-9: Fix server crash when a XI 1.x device grab is activated on a
              disabled synaptics touchpad is disabled
  - 1.13.0-10: Fix VT switch key handling
  - 1.13.0-11: Bump default EQ length to reduce the number of unhelpful abrt
               reports
  - 1.13.0-12: backout non-pci configuration less patch, its breaks multi-GPU
  - 1.13.0-13: fix hotplug issue with usb devices and large screens
  - 1.13.0-14: add events for autoconfig of gpus devices, allow usb devices to
               notify gnome
  - 1.13.0-15: Cherry-pick a fix for selection for TouchBegin from multiple
               clients
  - 1.13.1-2: fix bugs with autobinding output/offload slave from same driver
  - 1.13.1-3: fixes for reverse optimus support
  - 1.13.1-4: fix bug on server shutdown + valgrind warnings (#891140)
  - 1.13.1-5: Add quirk for Evoluent Vertical Mouse 3, button mapping is quirky
              (#612140)
  - 1.13.2-2: Fix differing sizeof XGCValues in xdmxconfig (#903986)

* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.13.0-102
- Merge Fedora's changes:
  - Add touchscreen fixes (including pointer emulation) #871064

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.13.0-101
- Update xserver-autobind-hotplug.patch from fedpkg

* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.13.0-100
- Initial release for Fedora 18
- Version 1.13.0

* Sun Aug 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.12.2-1
- Initial release
- Based on Fedora 17's spec file
- Version 1.12.2
- Patch from Ubuntu version 1.12.1.902 and release 1ubuntu1
