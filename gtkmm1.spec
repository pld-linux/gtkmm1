Summary:	A C++ interface for the GTK+ (a GUI library for X)
Summary(pl):	Wrapper C++ dla GTK
Name:		gtkmm1
%define		src_name	gtkmm
Version:	1.2.10
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/gtkmm/%{src_name}-%{version}.tar.gz
# Source0-md5:	a3816bef91a2796c3984b12954cc7fc9
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	automake
BuildRequires:	gtk+1-devel
BuildRequires:	imlib-devel
BuildRequires:	libsigc++1-devel >= 1.0.4
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
Requires:	cpp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	Gtk--

%description
This package provides a C++ interface for GTK+ (the Gimp ToolKit) GUI
library. The interface provides a convenient interface for C++
programmers to create GUIs with GTK+'s flexible object-oriented
framework. Features include type safe callbacks, widgets that are
extensible using inheritance and over 110 classes that can be freely
combined to quickly create complex user interfaces.

%description -l pl
GTK-- jest wrapperem C++ dla Gimp ToolKit (GTK+). GTK jest bibliotek±
s³u¿±c± do tworzenia graficznych interfejsów. W pakiecie znajduje siê
tak¿e biblioteka GDK-- - wrapper C++ dla GDK (General Drawing Kit).

%package devel
Summary:	GTK-- and GDK-- header files, development documentation
Summary(pl):	Pliki nag³ówkowe GTK-- i GDK--, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk+-devel
Requires:	libstdc++-devel
Requires:	libsigc++1-devel
Obsoletes:	Gtk---devel

%description devel
Header files and development documentation for GTK-- library.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja dla programistów do biblioteki GTK--.

%package static
Summary:	GTK-- and GDK-- static libraries
Summary(pl):	Biblioteki statyczne GTK-- i GDK--
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	Gtk---static

%description static
GTK-- and GDK-- static libraries.

%description static -l pl
Biblioteki statyczne GTK-- i GDK--.

%prep
%setup -q -n %{src_name}-%{version}

%build
CXXFLAGS="%{rpmcflags} -fno-exceptions"
cp -f /usr/share/automake/config.sub scripts/
%configure2_13 \
	--enable-static=yes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/src/examples/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

cp -dpr examples/* $RPM_BUILD_ROOT/usr/src/examples/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgdkmm*.so.*.*
%attr(755,root,root) %{_libdir}/libgtkmm*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS NEWS
%doc /usr/src/examples/%{name}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%attr(755,root,root) %{_bindir}/*

%{_includedir}/*

%dir %{_libdir}/gtkmm
%{_libdir}/gtkmm/include
%dir %{_libdir}/gtkmm/proc
%{_libdir}/gtkmm/proc/*.m4
%attr(755,root,root) %{_libdir}/gtkmm/proc/gtkmmproc

%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
