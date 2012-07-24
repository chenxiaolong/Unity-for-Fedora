# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-asset-pool
Version:	0.8.23
Release:	1%{?dist}
Summary:	Design assets for Unity

Group:		User Interface/Desktops
License:	CC-BY-SA
URL:		https://launchpad.net/unity-asset-pool
Source0:	https://launchpad.net/unity-asset-pool/0.8/%{version}/+download/unity-asset-pool-%{version}.tar.gz

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
%dir %{_datadir}/icons/unity-icon-theme/
%{_datadir}/icons/unity-icon-theme/apps/128/*.svg
%{_datadir}/icons/unity-icon-theme/apps/48/*.png
%{_datadir}/icons/unity-icon-theme/index.theme
%{_datadir}/icons/unity-icon-theme/places/22/*.png
%{_datadir}/icons/unity-icon-theme/places/24/*.png
%{_datadir}/icons/unity-icon-theme/places/svg/*.svg
%{_datadir}/icons/unity-icon-theme/search/16/*.png
%{_datadir}/icons/unity-icon-theme/web/48/*.png
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/themes/*.png


%changelog
* Sun Jul 08 2012 Xiao-long Chen <chenxiaolong@cxl.epac.to> - 0.8.23-1
- Initial release
- Version 0.8.23
