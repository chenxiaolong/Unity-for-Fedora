# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		nux
Version:	2.12.0
Release:	1%{?dist}
# Summary from Ubuntu
Summary:	Visual rendering toolkit for real-time applications

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/nux
Source0:	https://launchpad.net/nux/2.0/2.12/+download/nux-%{version}.tar.gz
Source1:	50_check_unity_support

# GCC 4.6 required or else Unity will segfault
BuildRequires:	gcc46-devel
BuildRequires:	gcc46-static

BuildRequires:	doxygen
BuildRequires:	graphviz

BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	glew-devel
BuildRequires:	glib2-devel
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
BuildRequires:	ibus-devel
BuildRequires:	libpng-devel
BuildRequires:	libsigc++20-devel
BuildRequires:	libX11-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXtst-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	pango-devel
BuildRequires:	pciutils-devel
BuildRequires:	pcre-devel
BuildRequires:	utouch-geis-devel

Requires:	%{name}-common = %{version}-%{release}

# Satisfy obs conflict on gtk2: use gtk2
BuildRequires:  gtk2

# Satisfy obs conflict on gtk3 too (installed by build dependencies)
BuildRequires:  gtk3
BuildRequires:  gtk3-devel

# Satisfy obs conflict on desktop-notification-daemon (installed by
# notify-python, which is required by the build dependencies)
BuildRequires:	notification-daemon

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

# Description from Ubuntu
%description
Nux is a graphical user interface toolkit for applications that mixes OpenGL
hardware acceleration with high quality visual rendering.


%package devel
Summary:	Development files for the nux library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	boost-devel
Requires:	cairo-devel
Requires:	gdk-pixbuf2-devel
Requires:	glew-devel
Requires:	glib2-devel
Requires:	libpng-devel
Requires:	libsigc++20-devel
Requires:	libXxf86vm-devel
Requires:	mesa-libGL-devel
Requires:	pango-devel
Requires:	pcre-devel

%description devel
This package contains the development files for the nux library.


%package common
Summary:	Common files for the nux library
Group:		System Environment/Libraries

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description common
This package contains the architecture-independent files for the nux library.


%package tools
Summary:	Visual rendering toolkit for real-time applications - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains various tools for the nux library.


%prep
%setup -q

# Avoid rpmlint spurious-executable-perm error in debuginfo package
find -type f \( -name '*.h' -o -name '*.cpp' \) -exec chmod 644 {} \;


%build
# Remove '-gnu' from target triplet
%global _gnu %{nil}

CC=%{_bindir}/%{_target_platform}-gcc-4.6
CXX=%{_bindir}/%{_target_platform}-g++-4.6

CPP="%{_bindir}/cpp-4.6 -x c"
CXXCPP="%{_bindir}/cpp-4.6 -x c++"

export CC CXX CPP CXXCPP

%configure

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Ubuntu doesn't package the gputests
rm -rv $RPM_BUILD_ROOT%{_datadir}/nux/gputests/

# Avoid rpmlint zero-length error. Remove empty files.
find $RPM_BUILD_ROOT -type f -empty -delete

# Install X startup session file
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libnux-2.0.so.0
%{_libdir}/libnux-2.0.so.0.1200.0
%{_libdir}/libnux-core-2.0.so.0
%{_libdir}/libnux-core-2.0.so.0.1200.0
%{_libdir}/libnux-graphics-2.0.so.0
%{_libdir}/libnux-graphics-2.0.so.0.1200.0
%{_libdir}/libnux-image-2.0.so.0
%{_libdir}/libnux-image-2.0.so.0.1200.0


%files devel
%doc AUTHORS
%dir %{_includedir}/Nux-2.0/
%dir %{_includedir}/Nux-2.0/Nux
%dir %{_includedir}/Nux-2.0/Nux/ProgramFramework/
%dir %{_includedir}/Nux-2.0/NuxCore/
%dir %{_includedir}/Nux-2.0/NuxCore/Character/
%dir %{_includedir}/Nux-2.0/NuxCore/FileManager/
%dir %{_includedir}/Nux-2.0/NuxCore/Math/
%dir %{_includedir}/Nux-2.0/NuxCore/TinyXML/
%dir %{_includedir}/Nux-2.0/NuxGraphics/
%dir %{_includedir}/Nux-2.0/NuxImage/
%{_includedir}/Nux-2.0/Nux/Readme.txt
%{_includedir}/Nux-2.0/Nux/*.h
%{_includedir}/Nux-2.0/Nux/ProgramFramework/*.h
%{_includedir}/Nux-2.0/NuxCore/*.h
%{_includedir}/Nux-2.0/NuxCore/Character/*.h
%{_includedir}/Nux-2.0/NuxCore/FileManager/*.h
%{_includedir}/Nux-2.0/NuxCore/Math/*.h
%{_includedir}/Nux-2.0/NuxCore/TinyXML/*.h
%{_includedir}/Nux-2.0/NuxGraphics/*.h
%{_includedir}/Nux-2.0/NuxImage/*.h
%{_libdir}/libnux-2.0.so
%{_libdir}/libnux-core-2.0.so
%{_libdir}/libnux-graphics-2.0.so
%{_libdir}/libnux-image-2.0.so
%{_libdir}/pkgconfig/nux-2.0.pc
%{_libdir}/pkgconfig/nux-core-2.0.pc
%{_libdir}/pkgconfig/nux-graphics-2.0.pc
%{_libdir}/pkgconfig/nux-image-2.0.pc


%files common
%doc AUTHORS
%dir %{_datadir}/nux/
%dir %{_datadir}/nux/2.0/
%dir %{_datadir}/nux/2.0/Fonts/
%dir %{_datadir}/nux/2.0/UITextures/
%{_datadir}/nux/2.0/Fonts/*.txt
%{_datadir}/nux/2.0/Fonts/*.png
%{_datadir}/nux/2.0/UITextures/*.png
%{_datadir}/nux/2.0/UITextures/*.tga
%{_datadir}/nux/2.0/UITextures/Painter.xml
%{_datadir}/nux/2.0/UITextures/UIArchive.iar


%files tools
%doc AUTHORS
%{_libexecdir}/unity_support_test
%{_sysconfdir}/X11/xinit/xinitrc.d/50_check_unity_support


%changelog
* Tue Jul 10 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.12.0-1
- Initial release
- Version 2.12.0
