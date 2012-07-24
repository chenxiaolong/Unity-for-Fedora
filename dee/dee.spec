# written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This package uses the same structure as the official (outdated) Fedora
# package. Feel free to merge it :)

%define _ubuntu_rel 0ubuntu1

Name:		dee
Version:	1.0.10
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Library for creating Model-View-Controller programs across DBus

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/dee
Source0:	https://launchpad.net/dee/1.0/%{version}/+download/dee-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/dee_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	autoconf
BuildRequires:	automake

BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	libicu-devel
BuildRequires:	python
BuildRequires:	vala-tools

%description
Libdee is a library that uses DBus to provide objects allowing you to create
Model-View-Controller type programs across DBus. It also consists of utility
objects which extend DBus allowing for peer-to-peer discoverability of known
objects without needing a central registrar.


%package devel
Summary:	Development files for dee
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	glib2-devel

%description devel
This package contains the development files for the dee library.


%package tools
Summary:	Library for creating Model-View-Controller programs across DBus - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains some tools from the dee library.


%package docs
Summary:	Documentation for dee
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the dee library.


%prep
%setup -q

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1

autoreconf -vfi


%build
%configure --enable-gtk-doc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libdee-1.0.so.4
%{_libdir}/libdee-1.0.so.4.1.1
%{_libdir}/girepository-1.0/Dee-1.0.typelib
%{python_sitearch}/gi/overrides/Dee.py*


%files devel
%doc AUTHORS
%dir %{_includedir}/dee-1.0/
%{_includedir}/dee-1.0/dee-analyzer.h
%{_includedir}/dee-1.0/dee-client.h
%{_includedir}/dee-1.0/dee-file-resource-manager.h
%{_includedir}/dee-1.0/dee-filter-model.h
%{_includedir}/dee-1.0/dee-filter.h
%{_includedir}/dee-1.0/dee-hash-index.h
%{_includedir}/dee-1.0/dee-icu.h
%{_includedir}/dee-1.0/dee-index.h
%{_includedir}/dee-1.0/dee-model-reader.h
%{_includedir}/dee-1.0/dee-model.h
%{_includedir}/dee-1.0/dee-peer.h
%{_includedir}/dee-1.0/dee-proxy-model.h
%{_includedir}/dee-1.0/dee-resource-manager.h
%{_includedir}/dee-1.0/dee-result-set.h
%{_includedir}/dee-1.0/dee-sequence-model.h
%{_includedir}/dee-1.0/dee-serializable-model.h
%{_includedir}/dee-1.0/dee-serializable.h
%{_includedir}/dee-1.0/dee-server.h
%{_includedir}/dee-1.0/dee-shared-model.h
%{_includedir}/dee-1.0/dee-term-list.h
%{_includedir}/dee-1.0/dee-text-analyzer.h
%{_includedir}/dee-1.0/dee-transaction.h
%{_includedir}/dee-1.0/dee-tree-index.h
%{_includedir}/dee-1.0/dee.h
%{_libdir}/libdee-1.0.so
%{_libdir}/pkgconfig/dee-1.0.pc
%{_libdir}/pkgconfig/dee-icu-1.0.pc
%{_datadir}/gir-1.0/Dee-1.0.gir
%{_datadir}/vala/vapi/dee-1.0.deps
%{_datadir}/vala/vapi/dee-1.0.vapi


%files tools
%doc AUTHORS
%{_bindir}/dee-tool


%files docs
%{_datadir}/gtk-doc/html/dee-1.0/DeeAnalyzer.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeClient.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeFileResourceManager.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeFilterModel.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeHashIndex.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeIndex.html
%{_datadir}/gtk-doc/html/dee-1.0/DeePeer.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeProxyModel.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeSequenceModel.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeSerializableModel.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeServer.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeSharedModel.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeTermList.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeTextAnalyzer.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeTransaction.html
%{_datadir}/gtk-doc/html/dee-1.0/DeeTreeIndex.html
%{_datadir}/gtk-doc/html/dee-1.0/annotation-glossary.html
%{_datadir}/gtk-doc/html/dee-1.0/api-index-full.html
%{_datadir}/gtk-doc/html/dee-1.0/ch01.html
%{_datadir}/gtk-doc/html/dee-1.0/ch02.html
%{_datadir}/gtk-doc/html/dee-1.0/ch03.html
%{_datadir}/gtk-doc/html/dee-1.0/ch04.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-Dee-ICU-Extensions.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-DeeModel.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-DeeResourceManager.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-DeeResultSet.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-DeeSerializable.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-Filters.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0-Model-Readers.html
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0.devhelp2
%{_datadir}/gtk-doc/html/dee-1.0/home.png
%{_datadir}/gtk-doc/html/dee-1.0/index.html
%{_datadir}/gtk-doc/html/dee-1.0/index.sgml
%{_datadir}/gtk-doc/html/dee-1.0/left.png
%{_datadir}/gtk-doc/html/dee-1.0/object-tree.html
%{_datadir}/gtk-doc/html/dee-1.0/right.png
%{_datadir}/gtk-doc/html/dee-1.0/style.css
%{_datadir}/gtk-doc/html/dee-1.0/up.png


%changelog
* Tue Jul 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.10-1.0ubuntu1
- Initial release
- Version 1.0.10
- Ubuntu release 0ubuntu1
