import 'package:area_mobile/api/parse.dart';
import 'package:area_mobile/settings/settings.dart';
import 'package:email_validator/email_validator.dart';
import 'package:flutter/material.dart';

/// The class for reset password.
class ResetPage extends StatefulWidget {
  static const routeName = '/reset';
  @override
  _ResetPageState createState() => _ResetPageState();
}

class _ResetPageState extends State<ResetPage> {
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();

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
          if (!EmailValidator.validate(text)) {
            return '$label malformated !';
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
  final _loginKey = GlobalKey<FormState>();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
      ),
      body: Center(
          child: SingleChildScrollView(
        child: Form(
          key: _loginKey,
          child: Column(
            children: [
              _textInputField("Email", Icons.account_box, _login,
                  TextInputType.emailAddress, false, null),
              Container(
                margin: EdgeInsets.only(top: 65),
                width: MediaQuery.of(context).size.width * 0.6,
                child: RaisedButton(
                  onPressed: () async {
                    if (_loginKey.currentState.validate()) {
                      bool ok = await ParseAPI().resetPassword(_login.text);
                      if (ok) {
                        Navigator.of(context).pop();
                      }

                      _scaffoldKey.currentState.showSnackBar(SnackBar(
                          behavior: SnackBarBehavior.floating,
                          content: Text("Reset password failed !"),
                          duration: Duration(seconds: 2)));
                    }
                  },
                  child: Text("Reset Password"),
                ),
              )
            ],
          ),
        ),
      )),
    );
  }
}
