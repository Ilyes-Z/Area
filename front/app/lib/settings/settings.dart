import 'package:flutter/material.dart';
import 'package:area_mobile/api/parse.dart';

class SettingsPage extends StatefulWidget {
  static const routeName = '/settings';
  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  ParseAPI _api;
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();

  Widget _textInputField(String label) {
    return Container(
      margin: EdgeInsets.only(top: 20),
      width: MediaQuery.of(context).size.width * 0.98,
      child: Form(
        key: _formKey,
        child: TextFormField(
          validator: (text) {
            if (text == null || text.isEmpty) {
              return '$label can\'t be empty !';
            }
            return null;
          },
          initialValue: _api.domaine,
          onChanged: (value) {
            _api.domaine = value;
          },
          decoration: InputDecoration(
              border:
                  OutlineInputBorder(borderRadius: BorderRadius.circular(20.0)),
              labelText: label),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    var args = ModalRoute.of(context).settings.arguments as dynamic;
    _api = args["api"];

    return Scaffold(
        key: _scaffoldKey,
        appBar: AppBar(
          leading: IconButton(
            icon: Icon(Icons.arrow_back_ios),
            onPressed: () {
              if (_api.domaine.endsWith("/")) {
                _api.domaine = _api.domaine.substring(0, _api.domaine.length - 1);

              }
              Navigator.of(context).pop();
            },
          ),
        ),
        body: SingleChildScrollView(
            child: Center(
          child: Column(
            children: [_textInputField("Hostname")],
          ),
        )));
  }
}