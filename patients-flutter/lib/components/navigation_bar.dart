// Copyright 2019 The Flutter team. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:doctor/api/api.dart';
import 'package:doctor/api/storage.dart';
import 'package:doctor/home/home.dart';
import 'package:doctor/login/login.dart';
import 'package:doctor/patient/patient.dart';
import 'package:doctor/profile/change_password.dart';
import 'package:doctor/profile/profileEdit.dart';
import 'package:flutter/material.dart';

class Navbar extends StatefulWidget {
  const Navbar({Key? key, required this.title}) : super(key: key);

  final String title;
  @override
  State<Navbar> createState() => _NavbarState();
}

class _NavbarState extends State<Navbar>{
  String token = "";
  final ApiService _apiService = ApiService();

  @override
  void initState(){
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    const drawerHeader = UserAccountsDrawerHeader(
      accountName: Text(""),
      accountEmail: Text(""),
      currentAccountPicture: CircleAvatar(
        child: FlutterLogo(size: 42.0),
      ),
    );
    final drawerItems = ListView(
      children: [
        Container(
          height: 15,
        ),
        const CircleAvatar(
          child: FlutterLogo(size: 70.0),
            minRadius: 50
        ),
        ListTile(
          title: const Text(
              "Home"
          ),
          selected: widget.title == "Home",
          leading: const Icon(Icons.home),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => Home(title: "Home"),
              ),
            );
          },
        ),
        ListTile(
          title: const Text(
              "Patients"
          ),
          selected: widget.title == "Patients",
          leading: const Icon(Icons.supervisor_account),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => Patient(title: "Patients", type: "only"),
              ),
            );
          },
        ),
        ListTile(
          title: const Text(
              "All Patients"
          ),
          selected: widget.title == "All Patients",
          leading: const Icon(Icons.supervisor_account),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => Patient(title: "All Patients", type: "all"),
              ),
            );
          },
        ),
        ListTile(
          title: const Text(
              "About me"
          ),
          selected: widget.title == "About me",
          leading: const Icon(Icons.person_pin),
          onTap: () {
            _apiService.getProfile().then((response) {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ProfileEdit(title: "About me", profile: response),
                ),
              );
            });
          },
        ),
        ListTile(
          title: const Text(
              "Change Password"
          ),
          selected: widget.title == "Change Password",
          leading: const Icon(Icons.password),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const ChangePassword(title: "Change Password"),
              ),
            );
          },
        ),
        ListTile(
          title: const Text(
              "Logout"
          ),
          leading: const Icon(Icons.logout),
          onTap: () {
            Navigator.pop(context);
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(
                builder: (context) => const Login(),
              ),
              ModalRoute.withName("/login"),
            );
          },
        ),
      ],
    );
    return Drawer(
      child: drawerItems,
    );
  }
}

