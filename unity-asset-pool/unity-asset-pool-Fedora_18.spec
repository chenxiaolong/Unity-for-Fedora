# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-asset-pool
Version:	0.8.24daily13.04.24
Release:	1%{?dist}
Summary:	Design assets for Unity

Group:		User Interface/Desktops
License:	CC-BY-SA
URL:		https://launchpad.net/unity-asset-pool
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/unity-asset-pool_%{version}.orig.tar.gz

BuildArch:	noarch

BuildRequires:	icon-naming-utils

Requires:	gnome-icon-theme
Requires:	hicolor-icon-theme

%description
This package contains icons and other images for Unity.


%prep
%setup -q


%build
# Nothing to build


%install
# Install Unity themes (use cp since there are symlinks)
install -dm755 $RPM_BUILD_ROOT%{_datadir}/unity/themes/
cp launcher/* $RPM_BUILD_ROOT%{_datadir}/unity/themes/
cp panel/* $RPM_BUILD_ROOT%{_datadir}/unity/themes/
chmod 644 $RPM_BUILD_ROOT%{_datadir}/unity/themes/*

# Install Unity icon theme
install -dm755 $RPM_BUILD_ROOT%{_datadir}/icons/
find unity-icon-theme/ -type f -exec install -Dm644 {} \
  $RPM_BUILD_ROOT%{_datadir}/icons/{} \;

# Remove Ubuntu branding icons
find $RPM_BUILD_ROOT -type f -name distributor-logo.png -delete

# From debian/rules
for i in $(find $RPM_BUILD_ROOT%{_datadir}/icons/ -mindepth 2 -maxdepth 2 -type d); do
  pushd ${i}
  for j in *; do
    icon-name-mapping -c ${j}
  done
  popd
done


%post
touch --no-create %{_datadir}/icons/unity-icon-theme/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/unity-icon-theme/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/unity-icon-theme/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/unity-icon-theme/ &>/dev/null || :


%files
%doc COPYRIGHT
%{_datadir}/icons/unity-icon-theme/
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/themes/*.png


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.24daily13.04.24-1
- Version 0.8.24daily13.04.24

* Thu Jan 31 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.24daily12.12.05-1
- Version 0.8.24daily12.12.05

* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.24-1
- Version 0.8.24

* Tue Aug 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.23-2
- Remove Ubuntu branding icons
- Fix directory ownership

* Sun Jul 08 2012 Xiao-long Chen <chenxiaolong@cxl.epac.to> - 0.8.23-1
- Initial release
- Version 0.8.23
