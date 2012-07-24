# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libgdu
Version:	3.0.2
Release:	1%{?dist}
Summary:	GNOME library for dealing with storage devices

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://git.gnome.org/cgit/gnome-disk-utility
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-disk-utility/3.0/gnome-disk-utility-3.0.2.tar.xz

Patch0:		0001_Build_library_only.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gnome-common
BuildRequires:	intltool

BuildRequires:	avahi-ui-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libatasmart-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	udisks-devel

%if 0%{?opensuse_bs}
# Satisfy OBS conflict on gtk2
BuildRequires:	gtk2
BuildRequires:	gtk2-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel
%endif

%description
This package contains the GNOME Disk Utility libraries from GNOME 3.0.


%package devel
Summary:	Development files for libgdu
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the GNOME Disk Utility library.


%package tools
Summary:	GNOME library for dealing with storage devices - Tools
Group:		Applications/System

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package currently contains gdu-format-tool needed by Unity.


%prep
%setup -q -n gnome-disk-utility-%{version}

%patch0 -p1 -b .libonly

# Remove unused source code
rm -rvf \
  data/ \
  doc/ \
  help/ \
  src/nautilus-extension \
  src/notification \
  src/palimpsest

autoreconf -vfi


%build
%configure --disable-scrollkeeper --disable-nautilus --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS NEWS README
%{_libdir}/libgdu.so.0
%{_libdir}/libgdu.so.0.0.0
%{_libdir}/libgdu-gtk.so.0
%{_libdir}/libgdu-gtk.so.0.0.0


%files devel
%doc AUTHORS NEWS README
%dir %{_includedir}/gnome-disk-utility/
%dir %{_includedir}/gnome-disk-utility/gdu/
%dir %{_includedir}/gnome-disk-utility/gdu-gtk/
%{_includedir}/gnome-disk-utility/gdu/gdu-adapter.h
%{_includedir}/gnome-disk-utility/gdu/gdu-callbacks.h
%{_includedir}/gnome-disk-utility/gdu/gdu-device.h
%{_includedir}/gnome-disk-utility/gdu/gdu-drive.h
%{_includedir}/gnome-disk-utility/gdu/gdu-error.h
%{_includedir}/gnome-disk-utility/gdu/gdu-expander.h
%{_includedir}/gnome-disk-utility/gdu/gdu-hub.h
%{_includedir}/gnome-disk-utility/gdu/gdu-known-filesystem.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-lvm2-volume-group.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-lvm2-volume-hole.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-lvm2-volume.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-md-drive.h
%{_includedir}/gnome-disk-utility/gdu/gdu-machine.h
%{_includedir}/gnome-disk-utility/gdu/gdu-pool.h
%{_includedir}/gnome-disk-utility/gdu/gdu-port.h
%{_includedir}/gnome-disk-utility/gdu/gdu-presentable.h
%{_includedir}/gnome-disk-utility/gdu/gdu-process.h
%{_includedir}/gnome-disk-utility/gdu/gdu-types.h
%{_includedir}/gnome-disk-utility/gdu/gdu-util.h
%{_includedir}/gnome-disk-utility/gdu/gdu-volume-hole.h
%{_includedir}/gnome-disk-utility/gdu/gdu-volume.h
%{_includedir}/gnome-disk-utility/gdu/gdu.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-add-component-linux-md-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-add-pv-linux-lvm2-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-ata-smart-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-button-element.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-button-table.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-confirmation-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-connect-to-server-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-create-linux-lvm2-volume-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-create-linux-md-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-create-partition-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-details-element.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-details-table.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-disk-selection-widget.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-drive-benchmark-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-edit-linux-lvm2-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-edit-linux-md-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-edit-name-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-edit-partition-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-error-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-format-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-gtk-enums.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-gtk-enumtypes.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-gtk-types.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-gtk.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-partition-dialog.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-pool-tree-model.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-pool-tree-view.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-size-widget.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-time-label.h
%{_includedir}/gnome-disk-utility/gdu-gtk/gdu-volume-grid.h
%{_libdir}/libgdu.so
%{_libdir}/libgdu-gtk.so
%{_libdir}/pkgconfig/gdu.pc
%{_libdir}/pkgconfig/gdu-gtk.pc


%files tools
%doc AUTHORS NEWS README
%{_libexecdir}/gdu-format-tool


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.2-1
- Initial release
- Version 3.0.2
