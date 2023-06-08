import 'dart:convert';

import 'package:doctor/patient/patient.dart';
import 'package:doctor/profile/profileEdit.dart';
import 'package:flutter/material.dart';
import 'package:doctor/api/api.dart';
import 'package:doctor/signup/signup.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../api/storage.dart';
import '../home/home.dart';
import '../main.dart';
import '../model/storage_item.dart';
import '../storeage/storeage.dart';

class Login extends StatefulWidget {
  const Login({Key? key}) : super(key: key);

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login>{
  bool _isLoading = false;
  bool _isFieldEmailValid = false;
  bool _isFieldPasswordValid = false;
  final TextEditingController _controllerEmail = TextEditingController();
  final TextEditingController _controllerPassword = TextEditingController();

  ApiService _apiService = ApiService();

  @override
  getToken() async{
    final Future<SharedPreferences> _prefs = SharedPreferences.getInstance();
    final SharedPreferences prefs = await _prefs;
    return prefs.getString('token') ?? "";
  }

  @override
  void initState() {
    setState(() {
      _isLoading = false;
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // key: _scaffoldState,
      appBar: AppBar(
        iconTheme: const IconThemeData(color: Colors.white),
        title: const Text(
          "Login Form",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body:  _isLoading ? Center(
          child : Column(
            mainAxisAlignment: MainAxisAlignment.center,//Center Column contents vertically,
            children: const [
              CircularProgressIndicator(),
              Text(
                'Loading . . .',
              ),
            ],
          )
      ) :  Stack(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                _buildTextFieldEmail(),
                _buildTextFieldPassword(),
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: FloatingActionButton.extended(
                    label: Text(
                      "login".toUpperCase(),
                      style: const TextStyle(
                        color: Colors.white,
                      ),
                    ),
                    onPressed: () {
                      if (
                          !_isFieldEmailValid ||
                          !_isFieldPasswordValid) {
                        return;
                      }
                      setState(() => _isLoading = true);
                      String email = _controllerEmail.text;
                      String password = _controllerPassword.text;
                      _apiService.login(email, password).then((response) async {
                        setState(() {
                          _isLoading = false;
                        });
                        if(response["status"] == "success"){
                          Navigator.pop(context);
                          Navigator.pushAndRemoveUntil(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const Home(title: 'Home'),
                            ),
                            ModalRoute.withName("/patients"),
                          );
                          final snackBar = const SnackBar(
                            content: Text('Login Successfully!'),
                          );

                          // Find the ScaffoldMessenger in the widget tree
                          // and use it to show a SnackBar.
                          ScaffoldMessenger.of(context).showSnackBar(snackBar);
                        }
                        if(response["status"] == "error"){
                          final snackBar = const SnackBar(
                            content: Text('Your credentials is wrong!'),
                          );
                          ScaffoldMessenger.of(context).showSnackBar(snackBar);
                        }
                      });
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: FloatingActionButton.extended(
                    label: Text(
                      "sign up".toUpperCase(),
                      style: const TextStyle(
                        color: Colors.white,
                      ),
                    ),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => Signup(),
                        ),
                      );
                    },
                  ),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextFieldEmail() {
    return TextField(
      controller: _controllerEmail,
      keyboardType: TextInputType.emailAddress,
      decoration: InputDecoration(
        labelText: "Email",
        errorText: _isFieldEmailValid
            ? null
            : "Email is required",
      ),
      onChanged: (value) {
        bool isFieldValid = value.trim().isNotEmpty;
        if (isFieldValid != _isFieldEmailValid) {
          setState(() => _isFieldEmailValid = isFieldValid);
        }
      },
    );
  }

  Widget _buildTextFieldPassword() {
    return TextField(
      controller: _controllerPassword,
      keyboardType: TextInputType.visiblePassword,
      obscureText: true,
      decoration: InputDecoration(
        labelText: "Password",
        errorText: _isFieldPasswordValid
            ? null
            : "Password is required",
      ),
      onChanged: (value) {
        bool isFieldValid = value.trim().isNotEmpty;
        if (isFieldValid != _isFieldPasswordValid) {
          setState(() => _isFieldPasswordValid = isFieldValid);
        }
      },
    );
  }
 }