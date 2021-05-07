import 'package:area_mobile/auth/login.dart';
import 'package:area_mobile/home.dart';
import 'package:email_validator/email_validator.dart';
import 'package:flutter/material.dart';
import 'package:area_mobile/api/parse.dart';
import 'dart:ui' as ui;

/// The class for the register page.
class RegisterPage extends StatefulWidget {
  static const routeName = '/register';
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  bool _isVisible = false;

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
          if (label == "Email" && !EmailValidator.validate(text)) {
            return '$label malformated';
          }
          if (label == "Confirm" &&
              (text.toString() == _password1.text.toString()) == false) {
            return 'The password does not match';
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

  TextEditingController _pseudo = TextEditingController();
  TextEditingController _login = TextEditingController();
  TextEditingController _password1 = TextEditingController();
  TextEditingController _password2 = TextEditingController();
  bool _isLoading = false;
  ParseAPI _api = ParseAPI();
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();
  final _loginKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      body: Center(
        child: SingleChildScrollView(
            child: Form(
          key: _loginKey,
          child: Column(
            children: [
              Text("AREA",
                  style: TextStyle(
                      fontSize: MediaQuery.of(context).size.height * 0.05)),
              _textInputField("Pseudo", Icons.account_box, _pseudo,
                  TextInputType.emailAddress, false, null),
              _textInputField("Email", Icons.account_box, _login,
                  TextInputType.emailAddress, false, null),
              _textInputField(
                  "Password",
                  _isVisible ? Icons.visibility : Icons.visibility_off,
                  _password1,
                  TextInputType.text,
                  !_isVisible,
                  _onPressedIcon),
              _textInputField(
                  "Confirm",
                  _isVisible ? Icons.visibility : Icons.visibility_off,
                  _password2,
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
                              bool isLog = await _api.registerUser(
                                  _login.text, _password1.text, _pseudo.text);
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
                                  content: Text("Register failed !"),
                                  duration: Duration(seconds: 2)));
                            }
                          },
                          child: Text("Register"),
                        ),
                      ),
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Text("Already register ?"),
                FlatButton(
                    shape: new RoundedRectangleBorder(
                        borderRadius: new BorderRadius.circular(30.0)),
                    splashColor: Colors.transparent,
                    onPressed: () async {
                      Navigator.of(context)
                          .popAndPushNamed(LoginPage.routeName);
                    },
                    child: Text(
                      "Sign in",
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
