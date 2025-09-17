%define devname %mklibname -d papers

%bcond_without test
%define major_ver 4
%define api_ver %{major_ver}_0
%define plugin_ver 6
%define minor 5

%define appid org.gnome.Papers
Name:           papers
Version:        49.0
Release:        1
Summary:        GNOME Document Viewer
License:        GPL-2.0-or-later
URL:            https://gitlab.gnome.org/GNOME/Incubator/papers
Source0:        https://download.gnome.org/sources/papers/48/papers-%{version}.tar.xz
Source1:        vendor.tar.xz
BuildRequires:  rust-packaging
BuildRequires:	rustfmt
BuildRequires:	clippy
BuildRequires:	desktop-file-utils
BuildRequires:  gsettings-desktop-schemas
BuildRequires:	gettext
BuildRequires:  meson >= 0.53.0
BuildRequires:  pkgconfig(libnautilus-extension-4)
BuildRequires:  python-gi
BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(blueprint-compiler)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(ddjvuapi)
BuildRequires:  pkgconfig(exempi-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk4) >= 4.17.1
BuildRequires:	pkgconfig(harfbuzz-gobject)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libspectre)
BuildRequires:  pkgconfig(libspelling-1)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(poppler-glib)
Requires: typelib(Poppler)
Requires: poppler

%description
Papers is a document viewer capable of displaying single-page and multi-page
document formats like PDF and PostScript.

%package -n %{devname}
Summary:        Header files for the Papers Document Viewer
Requires:       %{name} = %{EVRD}

%description -n %{devname}
Papers is a document viewer capable of displaying single-page and multi-page
document formats like PDF and PostScript.

This package contains the header files for building additional plugins.

%prep
%autosetup -a1
%cargo_prep -v vendor

cat >>Cargo.toml <<EOF

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%meson \
	--libexecdir=%{_libexecdir}/%{name} \
	-D documentation=false \
	-D user_doc=false \
	-D tests=false \
	-D sysprof=disabled \
    %{nil}
%meson_build

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS* README.md
%{_bindir}/papers
%{_bindir}/papers-previewer
%{_bindir}/papers-thumbnailer
%{_mandir}/man?/*
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/applications/%{appid}-previewer.desktop
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{appid}*
%{_datadir}/thumbnailers
%{_libdir}/libppsdocument-%{major_ver}.0.so.%{plugin_ver}*
%{_libdir}/libppsview-%{major_ver}.0.so.%{minor}*
%{_libdir}/girepository-1.0/PapersDocument-%{major_ver}.0.typelib
%{_libdir}/girepository-1.0/PapersView-%{major_ver}.0.typelib
%dir %{_libdir}/papers/
%dir %{_libdir}/papers/%{plugin_ver}
%dir %{_libdir}/papers/%{plugin_ver}/backends
%{_datadir}/metainfo/papers-comicsdocument.metainfo.xml
%{_libdir}/papers/%{plugin_ver}/backends/comicsdocument.papers-backend
%{_libdir}/papers/%{plugin_ver}/backends/libcomicsdocument.so

%{_datadir}/metainfo/papers-djvudocument.metainfo.xml
%{_libdir}/papers/%{plugin_ver}/backends/djvudocument.papers-backend
%{_libdir}/papers/%{plugin_ver}/backends/libdjvudocument.so

%{_datadir}/metainfo/papers-pdfdocument.metainfo.xml
%{_libdir}/papers/%{plugin_ver}/backends/pdfdocument.papers-backend
%{_libdir}/papers/%{plugin_ver}/backends/libpdfdocument.so

%{_datadir}/metainfo/papers-tiffdocument.metainfo.xml
%{_libdir}/papers/%{plugin_ver}/backends/tiffdocument.papers-backend
%{_libdir}/papers/%{plugin_ver}/backends/libtiffdocument.so

%{_libdir}/nautilus/extensions-4/libpapers-document-properties.so

%files -n %{devname}
%{_includedir}/papers
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir
%{_libdir}/pkgconfig/papers*.pc
