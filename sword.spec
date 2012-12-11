%define lib_name_orig	libsword
%define lib_major	4
%define lib_name	%mklibname %{name} %{version}
%define develname	%mklibname -d %{name}
%define staticname	%mklibname -d -s %{name}

Summary:	The SWORD Project framework for manipulating Bible texts
Name:		sword
Version:	1.6.2
Release:	5
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.crosswire.org/sword/software/
Source0:	http://www.crosswire.org/ftpmirror/pub/sword/source/v1.6/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.zedz.net/pub/crypto/crypto/LIBS/sapphire/sapphire.zip
Source2:	sword_icons.tar.bz2
Patch0:		sword-1.6.2-curl.patch
Patch1:		sword-1.6.2-gcc4.7.patch
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

%package -n %{staticname}
Summary:	Static libs for developing sword applications
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n %{staticname}
This package contains the static libraries that programmers will need to
develop applications which will use the SWORD Bible Framework.

%prep
%setup -q -a2
%patch0 -p0
%patch1 -p1
unzip -d sapphire %{SOURCE1}
cp -a sapphire/SAPPHIRE.H include/sapphire.h
cp -a sapphire/SAPPHIRE.CPP src/modules/common/sapphire.cpp

%build
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
%{_libdir}/sword/%{version}_icu_*/translit_*.res
%config(noreplace) %{_sysconfdir}/sword.conf

%files -n %{lib_name}
%{_libdir}/*%{name}-*.so

%files -n %{develname}
%attr(0755,root,root) %dir %{_includedir}/sword
%{_includedir}/sword/*.*
%{_libdir}/*%{name}.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%{_libdir}/*.a

%changelog
* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.2-4mdv2011.0
+ Revision: 686324
- avoid pulling 32 bit libraries on 64 bit arch

* Sun Jun 05 2011 Funda Wang <fwang@mandriva.org> 1.6.2-3
+ Revision: 682818
- rebuild for new icu

* Mon Mar 14 2011 Funda Wang <fwang@mandriva.org> 1.6.2-2
+ Revision: 644601
- cleanup old language section
- rebuild for new icu

* Mon Oct 25 2010 Buchan Milne <bgmilne@mandriva.org> 1.6.2-1mdv2011.0
+ Revision: 589290
- New version 1.6.2
- fix the icu transliteration file paths to not embed version numbers

* Mon Sep 06 2010 Buchan Milne <bgmilne@mandriva.org> 1.6.1-1mdv2011.0
+ Revision: 576291
- Buildrequires icu and icu-devel
- New version 1.6.1

* Sat Jun 06 2009 Frederik Himpe <fhimpe@mandriva.org> 1.6.0-1mdv2010.0
+ Revision: 383327
- Update to new version 1.6.0

* Fri Aug 15 2008 Buchan Milne <bgmilne@mandriva.org> 1.5.11-1mdv2009.0
+ Revision: 272232
- update to new version 1.5.11

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 07 2007 Funda Wang <fwang@mandriva.org> 1.5.10-1mdv2008.1
+ Revision: 116226
- New version 1.5.10


* Sat Jan 06 2007 David Walluck <walluck@mandriva.org> 1.5.9-1mdv2007.0
+ Revision: 104737
- 1.5.9

* Sat Jan 06 2007 David Walluck <walluck@mandriva.org> 1.5.8-3mdv2007.1
+ Revision: 104726
- Import sword

* Thu Sep 07 2006 Buchan Milne <bgmilne@mandriva.org> 1.5.8-3mdv2007.0
- rebuild

* Fri Nov 25 2005 Buchan Milne <bgmilne@mandriva.org> 1.5.8-2mdk
- rebuild to provide missing srpm

* Wed Sep 14 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.5.8-1mdk
- New release 1.5.8
- make it build on x86_64 (use %%configure)
- cleanups
- use %%mkrel (since it can do everything the excess macros were doing)
- rpmbuildupdate-able
- drop p0

* Thu Aug 26 2004 Buchan Milne<bgmilne@linux-mandrake.com> 1.5.7a-1mdk
- bump lib major
- changes from Lonnie Borntreger <cooker@borntreger.com>
  - rework patch0 for new source snapshot
  - remove patch1, merged upstream

* Wed Jul 28 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5.7-4mdk
- lowerize optimization level thus preventing some segfaults in libsword3

* Wed Jul 28 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5.7-3mdk
- rebuild

* Sat Jul 17 2004 Buchan Milne <bgmilne@linux-mandrake.com> 1.5.7-3mdk
- rebuild for curl, fix requires/buildrequires

* Wed Jun 16 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.5.7-2mdk
- Rebuild

