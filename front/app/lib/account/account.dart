import 'package:area_mobile/account/webviewContainer.dart';
import 'package:area_mobile/api/parse.dart';
import 'package:area_mobile/auth/login.dart';
import 'package:area_mobile/settings/settings.dart';
import 'package:flutter/material.dart';

/// The Account class for service registration.
class AccountPage extends StatefulWidget {
  static const routeName = '/account';
  AccountPage({Key key}) : super(key: key);

  @override
  _AccountPageState createState() => _AccountPageState();
}

class _AccountPageState extends State<AccountPage> {
  @override
  void initState() {
    super.initState();
  }

  Widget _serviceConnexion(BuildContext context, Map<String, dynamic> serv) {
    return GestureDetector(
      onTap: () async {
        try {
          if (!serv['connected']) {
            Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (context) => WebViewContainer(
                      serv['auth_parameter']['url'], serv['name'], _api)),
            );
          } else {
            bool ok = await _api.revokeToken(serv["name"]);
            print('Ok: $ok');
            if (ok) {
              setState(() {});
            }
          }
        } catch (err) {
          print("Error: $err");
        }
      },
      child: Container(
        margin: EdgeInsets.only(top: 10),
        decoration: BoxDecoration(
            border: Border.all(color: Colors.black, width: 1.5),
            borderRadius: BorderRadius.circular(20)),
        height: 80,
        child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          Text(
              "${serv['connected'] ? "Unlink" : "Link"} with your ${serv['name']} account")
        ]),
      ),
    );
  }

  ParseAPI _api;
  @override
  Widget build(BuildContext context) {
    _api = ModalRoute.of(context).settings.arguments as ParseAPI;
    return Scaffold(
      appBar: AppBar(
        title: Text('${_api.username} account'),
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, size: 25),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        actions: [
          IconButton(
              icon: Icon(Icons.power_settings_new),
              onPressed: () {
                Navigator.of(context).pushNamedAndRemoveUntil(
                    LoginPage.routeName, (Route<dynamic> route) => false);
              })
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.of(context)
              .pushNamed(SettingsPage.routeName, arguments: {"api": _api});
        },
        child: Icon(Icons.settings),
      ),
      body: FutureBuilder<List<dynamic>>(
          future: _api.getServices(),
          builder:
              (BuildContext context, AsyncSnapshot<List<dynamic>> snapshot) {
            if (!snapshot.hasData) {
              return Center(child: Text('Please wait its loading...'));
            } else {
              List<dynamic> services = snapshot.data;
              return NotificationListener<OverscrollIndicatorNotification>(
                onNotification: (notif) {
                  notif.disallowGlow();
                  return;
                },
                child: SingleChildScrollView(
                  child: Container(
                    height: MediaQuery.of(context).size.height,
                    child: ListView.builder(
                      itemCount: services.length,
                      itemBuilder: (BuildContext context, int index) {
                        if (services[index]["auth_required"] as bool) {
                          return _serviceConnexion(context, services[index]);
                        }
                        return Container();
                      },
                    ),
                  ),
                ),
              );
            }
          }),
    );
  }
}
