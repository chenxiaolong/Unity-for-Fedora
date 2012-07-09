# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-files
Version:	5.10.0
Release:	1%{?dist}
Summary:	Unity files lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-files
Source0:	https://launchpad.net/unity-lens-files/5.0/%{version}/+download/unity-lens-files-%{version}.tar.gz

Patch0:		vala-0.16_fix.patch

BuildRequires:	gettext

BuildRequires:	dee-devel
BuildRequires:	glib2-devel
BuildRequires:	libgee06-devel
BuildRequires:	libunity-devel
BuildRequires:	libzeitgeist-devel
BuildRequires:	vala-tools

%description
This package contains the files lens which can be used to browse recent
documents and other files.


%prep
%setup -q

%patch0 -p1 -b .vala016fix


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libexecdir}/unity-files-daemon
%{_datadir}/dbus-1/services/unity-lens-files.service
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.FilesLens.gschema.xml
%dir %{_datadir}/unity/lenses/files/
%{_datadir}/unity/lenses/files/files.lens
%{_datadir}/unity/themes/files.png


%changelog
* Fri Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.10.0-1
- Initial release
- Version 5.10.0
