%define lib_name_orig	libsword
%define lib_major	4
%define lib_name	%mklibname %{name} %{version}
%define develname	%mklibname -d %{name}

Summary:	The SWORD Project framework for manipulating Bible texts
Name:		sword
Version:	1.8.1
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.crosswire.org/sword/software/
Source0:	http://www.crosswire.org/ftpmirror/pub/sword/source/v1.8/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.zedz.net/pub/crypto/crypto/LIBS/sapphire/sapphire.zip
Source2:	sword_icons.tar.bz2
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	icu-devel
BuildRequires:	icu
Requires:	%{lib_name} = %{version}-%{release}
Requires:	curl


%description
The SWORD Project is an effort to create an ever expanding software package 
for research and study of God and His Word.  The SWORD Framework 
allows easy manipulation of Bible texts, commentaries, lexicons, dictionaries, 
etc.  Many frontends are build using this framework.  An installed module 
set may be shared between any frontend using the framework.

#main package (contains *.so.[major].* only)
%package -n %{lib_name}
Summary:	Main library for sword #(!) summary for main lib RPM only
Group:		System/Libraries

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with sword.

%package -n %{develname}
Summary:	Include files for developing sword applications
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use the SWORD Bible Framework.

%prep
%setup -q -a2
%apply_patches

unzip -d sapphire %{SOURCE1}
cp -a sapphire/SAPPHIRE.H include/sapphire.h
cp -a sapphire/SAPPHIRE.CPP src/modules/common/sapphire.cpp

%build
NOCONFIGURE=1 ./autogen.sh
export CXXFLAGS="%{optflags} -DU_USING_ICU_NAMESPACE=1"

#export CC=gcc
#export CXX=g++
%configure2_5x \
	--disable-dependency-tracking \
	--enable-utilities \
	--with-curl \
	--disable-debug \
	--enable-shared \
	--with-conf
%make

%install
%makeinstall_std

install -m 0755 utilities/{mkfastmod,mod2vpl,vpl2mod} %{buildroot}%{_bindir}

%files
%doc README AUTHORS NEWS INSTALL LICENSE ChangeLog
%doc samples doc/*.*
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sword.conf

%files -n %{lib_name}
%{_libdir}/*%{name}-*.so

%files -n %{develname}
%attr(0755,root,root) %dir %{_includedir}/sword
%{_includedir}/sword/*.*
%{_libdir}/*%{name}.so
%{_libdir}/pkgconfig/*.pc

