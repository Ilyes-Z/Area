import 'package:area_mobile/api/parse.dart';
import 'package:area_mobile/auth/reset.dart';
import 'package:area_mobile/home.dart';
import 'package:area_mobile/auth/register.dart';
import 'package:area_mobile/settings/settings.dart';
import 'package:flutter/material.dart';
import 'dart:ui' as ui;

/// The class for the login page.
class LoginPage extends StatefulWidget {
  static const routeName = '/';
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  bool _isVisible = false;
  ParseAPI _api = ParseAPI();
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();

  void _onPressedIcon() {
    setState(() {
      _isVisible = !_isVisible;
    });
  }

  Widget _textInputField(
      String label,
      IconData icon,
      TextEditingController controller,
      TextInputType inputType,
      bool obscure,
      Function onPress) {
    return Container(
      margin: EdgeInsets.only(top: 20),
      width: MediaQuery.of(context).size.width * 0.98,
      child: TextFormField(
        validator: (text) {
          if (text == null || text.isEmpty) {
            return '$label can\'t be empty !';
          }
          return null;
        },
        obscureText: obscure,
        controller: controller,
        keyboardType: inputType,
        decoration: InputDecoration(
            border:
                OutlineInputBorder(borderRadius: BorderRadius.circular(20.0)),
            suffixIcon: IconButton(icon: Icon(icon), onPressed: onPress),
            labelText: label),
      ),
    );
  }

  TextEditingController _login = TextEditingController();
  TextEditingController _password = TextEditingController();
  bool _isLoading = false;
  final _loginKey = GlobalKey<FormState>();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        actions: [
          IconButton(
              icon: Icon(Icons.settings),
              onPressed: () {
                Navigator.of(context).pushNamed(SettingsPage.routeName,
                    arguments: {"api": _api});
              })
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
            child: Form(
          key: _loginKey,
          child: Column(
            children: [
              Text("AREA",
                  style: TextStyle(
                      fontSize: MediaQuery.of(context).size.height * 0.05)),
              _textInputField("Login", Icons.account_box, _login,
                  TextInputType.emailAddress, false, null),
              _textInputField(
                  "Password",
                  _isVisible ? Icons.visibility : Icons.visibility_off,
                  _password,
                  TextInputType.text,
                  !_isVisible,
                  _onPressedIcon),
              Container(
                margin: EdgeInsets.only(top: 25),
                child: _isLoading
                    ? CircularProgressIndicator()
                    : Material(
                        elevation: 1.5,
                        color: Colors.blueGrey[400],
                        borderRadius: BorderRadius.circular(30),
                        child: MaterialButton(
                          minWidth: MediaQuery.of(context).size.width * 0.85,
                          onPressed: () async {
                            if (_loginKey.currentState.validate()) {
                              setState(() {
                                _isLoading = true;
                              });
                              bool isLog = await _api.loginUser(
                                  _login.text, _password.text);
                              setState(() {
                                _isLoading = false;
                              });
                              if (isLog) {
                                Navigator.of(context).popAndPushNamed(
                                    HomePage.routeName,
                                    arguments: _api);
                              }
                              _scaffoldKey.currentState.showSnackBar(SnackBar(
                                  behavior: SnackBarBehavior.floating,
                                  content: Text("Connexion failed !"),
                                  duration: Duration(seconds: 2)));
                            }
                          },
                          child: Text("Sign in"),
                        ),
                      ),
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Text("Not register ?"),
                FlatButton(
                    shape: new RoundedRectangleBorder(
                        borderRadius: new BorderRadius.circular(30.0)),
                    splashColor: Colors.transparent,
                    onPressed: () async {
                      Navigator.of(context)
                          .popAndPushNamed(RegisterPage.routeName);
                    },
                    child: Text(
                      "Register",
                      style: TextStyle(
                          fontSize: 14,
                          foreground: Paint()
                            ..shader = ui.Gradient.linear(
                              const Offset(0, 0),
                              const Offset(200, 0),
                              <Color>[
                                Colors.grey,
                                Colors.blueGrey[400],
                              ],
                            )),
                    ))
              ]),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Text("Reset password ?"),
                FlatButton(
                    shape: new RoundedRectangleBorder(
                        borderRadius: new BorderRadius.circular(30.0)),
                    splashColor: Colors.transparent,
                    onPressed: () async {
                      Navigator.of(context)
                          .pushNamed(ResetPage.routeName);
                    },
                    child: Text(
                      "Reset",
                      style: TextStyle(
                          fontSize: 14,
                          foreground: Paint()
                            ..shader = ui.Gradient.linear(
                              const Offset(0, 0),
                              const Offset(200, 0),
                              <Color>[
                                Colors.grey,
                                Colors.blueGrey[400],
                              ],
                            )),
                    ))
              ])
            ],
          ),
        )),
      ),
    );
  }
}
